"""Small trainable BERT4Rec-style/SASRec-style and LightGCN implementations.
Optional dependency: torch. CPU defaults, no claims of paper-exact reproduction.
"""
import numpy as np
import torch
from torch import nn
from .recommend import Popularity

class SequenceNet(nn.Module):
 def __init__(self,n,dim=32,length=30,causal=False):
  super().__init__();self.length=length;self.causal=causal
  self.emb=nn.Embedding(n+2,dim,padding_idx=0);self.pos=nn.Embedding(length,dim)
  layer=nn.TransformerEncoderLayer(dim,4,dim*2,dropout=.1,batch_first=True)
  self.encoder=nn.TransformerEncoder(layer,2,enable_nested_tensor=False);self.out=nn.Linear(dim,n+1)
 def forward(self,x):
  pad=x.eq(0);z=self.emb(x)+self.pos(torch.arange(x.shape[1],device=x.device))
  mask=torch.triu(torch.ones(x.shape[1],x.shape[1],device=x.device,dtype=torch.bool),diagonal=1) if self.causal else None
  return self.out(self.encoder(z,mask=mask,src_key_padding_mask=pad))

class TransformerRec(Popularity):
 def __init__(self,kind='bert',epochs=3,dim=32,length=30,seed=42):
  self.kind=kind;self.epochs=epochs;self.dim=dim;self.length=length;self.seed=seed
 def fit(self,seqs):
  torch.set_num_threads(2);torch.manual_seed(self.seed);super().fit(seqs)
  self.index={x:i+1 for i,x in enumerate(self.items)};n=len(self.items);self.net=SequenceNet(n,self.dim,self.length,self.kind=='sas')
  rng=np.random.default_rng(self.seed);examples=[]
  for s in seqs:
   ids=[self.index[i] for i in s]
   if self.kind=='sas':
    for t in range(1,len(ids)):examples.append((ids[max(0,t-self.length):t],ids[t]))
   else:
    # Random item reconstruction from training history only.
    for t in range(1,len(ids)):
     segment=ids[max(0,t-self.length+1):min(len(ids),t+4)][:self.length]
     p=int(rng.integers(len(segment)))
     label=segment[p];segment=segment.copy();segment[p]=n+1
     examples.append((segment,(p,label)))
  if not examples:raise ValueError('Zu wenige Trainingssequenzen.')
  opt=torch.optim.AdamW(self.net.parameters(),lr=.002,weight_decay=.01);self.losses=[]
  for epoch in range(self.epochs):
   order=rng.permutation(len(examples));total=[];self.net.train()
   for start in range(0,len(order),64):
    batch=[examples[i] for i in order[start:start+64]];x=torch.zeros((len(batch),self.length),dtype=torch.long);positions=[];labels=[]
    for j,(seq,target) in enumerate(batch):
     x[j,:len(seq)]=torch.tensor(seq)
     pos,label=(len(seq)-1,target) if self.kind=='sas' else target
     positions.append(pos);labels.append(label)
    logits=self.net(x)[torch.arange(len(batch)),positions];loss=nn.functional.cross_entropy(logits,torch.tensor(labels));opt.zero_grad();loss.backward();nn.utils.clip_grad_norm_(self.net.parameters(),1.);opt.step();total.append(loss.item())
   self.losses.append(float(np.mean(total)))
  self.net.eval();return self
 def scores(self,history):
  ids=[self.index[i] for i in history if i in self.index]
  if not ids:return super().scores(history)
  ids=ids[-(self.length-1):]+[len(self.items)+1] if self.kind=='bert' else ids[-self.length:]
  x=torch.zeros((1,self.length),dtype=torch.long);x[0,:len(ids)]=torch.tensor(ids)
  with torch.no_grad():return self.net(x)[0,len(ids)-1,1:].numpy()

class LightGCN(Popularity):
 def __init__(self,epochs=5,dim=32,seed=42):self.epochs=epochs;self.dim=dim;self.seed=seed
 def fit(self,seqs):
  torch.set_num_threads(2);torch.manual_seed(self.seed);super().fit(seqs);self.index={i:j for j,i in enumerate(self.items)};n=len(self.items);u=len(seqs);rng=np.random.default_rng(self.seed)
  pairs=[(a,self.index[b]) for a,s in enumerate(seqs) for b in set(s)];self.seen=[{self.index[b] for b in s} for s in seqs]
  rows=[];cols=[]
  for a,b in pairs:rows.extend([a,u+b]);cols.extend([u+b,a])
  deg=np.bincount(rows,minlength=u+n);weights=[1/np.sqrt(deg[a]*deg[b]) for a,b in zip(rows,cols)]
  adj=torch.sparse_coo_tensor(torch.tensor([rows,cols]),torch.tensor(weights,dtype=torch.float32),(u+n,u+n)).coalesce()
  emb=nn.Embedding(u+n,self.dim);nn.init.normal_(emb.weight,std=.1);opt=torch.optim.Adam(emb.parameters(),lr=.02)
  def propagate():
   z=emb.weight;all_z=[z]
   for _ in range(2):z=torch.sparse.mm(adj,z);all_z.append(z)
   return torch.stack(all_z).mean(0)
  usable=[(a,b) for a,b in pairs if len(self.seen[a])<n]
  if not usable:raise ValueError('Keine negativen Artikel verfügbar.')
  self.losses=[]
  for _ in range(self.epochs):
   losses=[]
   order=rng.permutation(len(usable))
   for start in range(0,len(usable),256):
    selected=[usable[i] for i in order[start:start+256]];a=np.array([x for x,_ in selected]);b=np.array([y for _,y in selected]);neg=[]
    for user in a:
     candidate=int(rng.integers(n))
     while candidate in self.seen[user]:candidate=int(rng.integers(n))
     neg.append(candidate)
    z=propagate();uv=z[a];pos=z[u+b];negative=z[u+np.array(neg)]
    loss=-nn.functional.logsigmoid((uv*(pos-negative)).sum(1)).mean()+1e-4*emb.weight.square().mean()
    opt.zero_grad();loss.backward();opt.step();losses.append(loss.item())
   self.losses.append(float(np.mean(losses)))
  with torch.no_grad():self.vectors=propagate()[u:].numpy()
  return self
 def scores(self,history):
  ids=[self.index[i] for i in history if i in self.index]
  return self.vectors @ self.vectors[ids[-10:]].mean(0) if ids else super().scores(history)
