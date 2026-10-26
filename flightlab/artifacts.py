"""Safe-format checkpoint exports; never load untrusted pickle uploads."""
import json
from pathlib import Path
import numpy as np
from scipy import sparse

def export_models(models,directory):
 root=Path(directory);root.mkdir(parents=True,exist_ok=True)
 for name,model in models.items():
  folder=root/name;folder.mkdir(exist_ok=True)
  meta={'class':type(model).__name__,'items':model.items,'note':'Nur eigene lokale Checkpoints verwenden. Keine Pickle-Uploads.'}
  np.savez_compressed(folder/'scores.npz',popularity=model.values)
  if hasattr(model,'net'):
   import torch
   torch.save(model.net.state_dict(),folder/'weights.pt');meta.update(kind=model.kind,dim=model.dim,length=model.length,epochs=model.epochs)
  if hasattr(model,'vectors'):np.savez_compressed(folder/'embeddings.npz',vectors=model.vectors)
  if hasattr(model,'matrix'):sparse.save_npz(folder/'item_matrix.npz',model.matrix)
  if hasattr(model,'transitions'):meta['transitions']={a:dict(b) for a,b in model.transitions.items()}
  (folder/'config.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2))
