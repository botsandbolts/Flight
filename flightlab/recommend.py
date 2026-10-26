"""CPU baselines with a common full-training-catalog ranking protocol."""
from collections import Counter,defaultdict
import numpy as np
from scipy import sparse
from sklearn.preprocessing import normalize

class Popularity:
 def fit(self, seqs):
  self.items=sorted({i for s in seqs for i in s});counts=Counter(i for s in seqs for i in s)
  self.values=np.array([counts[i] for i in self.items],float);return self
 def scores(self,history):return self.values.copy()

class ItemKNN(Popularity):
 def fit(self,seqs):
  super().fit(seqs);self.index={x:i for i,x in enumerate(self.items)};rows=[];cols=[]
  for u,s in enumerate(seqs):
   for item in set(s):rows.append(u);cols.append(self.index[item])
  matrix=sparse.csr_matrix((np.ones(len(rows)),(rows,cols)),shape=(len(seqs),len(self.items)))
  self.matrix=normalize(matrix.T).tocsr();return self
 def scores(self,history):
  ids=[self.index[i] for i in history if i in self.index]
  if not ids:return super().scores(history)
  # Avoid a dense item x item matrix.
  query=self.matrix[ids[-10:]].mean(axis=0)
  return np.asarray(self.matrix @ np.asarray(query).ravel()).ravel()

class Markov(Popularity):
 def fit(self,seqs):
  super().fit(seqs);self.index={x:i for i,x in enumerate(self.items)};self.transitions=defaultdict(Counter)
  for s in seqs:
   for a,b in zip(s,s[1:]):self.transitions[a][b]+=1
  return self
 def scores(self,history):
  scores=self.values/(max(self.values.sum(),1))*1e-3
  if history:
   for item,count in self.transitions[history[-1]].items():scores[self.index[item]]+=count
  return scores

def rank(model,history,k=20):
 scores=model.scores(history);indices=np.argsort(-scores,kind='stable')[:k]
 return [(model.items[i],float(scores[i])) for i in indices]

def evaluate(model,cases,k=10):
 hits=[];ndcg=[];unknown=0;covered=set()
 for history,target in cases:
  if target not in model.items:unknown+=1;continue
  recs=[i for i,_ in rank(model,history,k)];covered.update(recs)
  position=recs.index(target)+1 if target in recs else None
  hits.append(float(position is not None));ndcg.append(1/np.log2(position+1) if position else 0.)
 return {'Recall@'+str(k):float(np.mean(hits)) if hits else 0.,'NDCG@'+str(k):float(np.mean(ndcg)) if ndcg else 0.,'eligible_cases':len(hits),'cold_targets':unknown,'catalog_size':len(model.items),'coverage':len(covered)/max(1,len(model.items))}

def temporal_cases(train,test,max_cases=500):
 history={u:list(g.sort_values('time').item) for u,g in train.groupby('user')};cases=[]
 for r in test.sort_values('time',kind='stable').itertuples():
  h=history.get(r.user,[])
  if h:cases.append((h[-50:].copy(),r.item))
  history.setdefault(r.user,[]).append(r.item)
  if len(cases)>=max_cases:break
 return cases
