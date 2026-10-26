"""Train, measure and save provenance. No fitted model deserialization in the GUI."""
import time
import json
import platform
from pathlib import Path
from .data import demo_events,temporal_split,sequences,fingerprint
from .recommend import Popularity,ItemKNN,Markov,evaluate,temporal_cases

def run(events,models=('Popularität','ItemKNN','Markov'),epochs=2,max_cases=300,source='synthetisch',k=10):
 train,test,cutoff=temporal_split(events);seqs=sequences(train);cases=temporal_cases(train,test,max_cases);rows=[];fitted={}
 if not cases:raise ValueError('Keine auswertbaren Fälle nach dem Zeitsplit.')
 for name in models:
  if name=='Popularität':model=Popularity()
  elif name=='ItemKNN':model=ItemKNN()
  elif name=='Markov':model=Markov()
  else:
   from .neural import TransformerRec,LightGCN
   model=LightGCN(epochs=epochs) if name=='LightGCN' else TransformerRec(kind='bert' if name=='BERT4Rec' else 'sas',epochs=epochs)
  start=time.perf_counter();model.fit(seqs);train_seconds=time.perf_counter()-start;start=time.perf_counter();metrics=evaluate(model,cases,k)
  rows.append({'Modell':name,**metrics,'training_seconds':train_seconds,'evaluation_seconds':time.perf_counter()-start});fitted[name]=model
 manifest={'source':source,'fingerprint':fingerprint(events),'rows':len(events),'train_rows':len(train),'test_rows':len(test),'cutoff':cutoff,'protocol':'globaler Zeitsplit 80/20; erste max_cases vorwärts ausgewertet; Vollkatalog des Trainings; wiederholte Artikel erlaubt; kalte Ziele separat ausgeschlossen','max_cases':max_cases,'k':k,'seed':42,'epochs':epochs,'python':platform.python_version(),'results':rows}
 return manifest,fitted,cases

def save(manifest,path):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2))

def run_sessions(seqs,models=('Popularität','Markov'),epochs=2,source='Amazon-M2',seed=42):
 """Held-out sessions; never describe this as a temporal split."""
 import numpy as np
 import pandas as pd
 rng=np.random.default_rng(seed);order=rng.permutation(len(seqs));cut=int(.8*len(seqs));train=[seqs[i] for i in order[:cut]];test=[seqs[i] for i in order[cut:] if len(seqs[i])>=2]
 if not train or not test:raise ValueError('Mindestens zehn Sessions mit Historie und Ziel verwenden.')
 rows=[];fitted={};cases=[(s[:-1][-50:],s[-1]) for s in test[:500]]
 for name in models:
  if name in ['Popularität','ItemKNN','Markov']:model={'Popularität':Popularity,'ItemKNN':ItemKNN,'Markov':Markov}[name]()
  else:
   from .neural import TransformerRec,LightGCN
   model=LightGCN(epochs=epochs) if name=='LightGCN' else TransformerRec(kind='bert' if name=='BERT4Rec' else 'sas',epochs=epochs)
  start=time.perf_counter();model.fit(train);elapsed=time.perf_counter()-start;start=time.perf_counter();result=evaluate(model,cases,10)
  rows.append({'Modell':name,**result,'training_seconds':elapsed,'evaluation_seconds':time.perf_counter()-start});fitted[name]=model
 return {'source':source,'fingerprint':fingerprint(pd.DataFrame({'seq':[' '.join(s) for s in seqs]})),'rows':len(seqs),'protocol':'Randomisierter Session-Holdout 80/20. Keine globale Zeitgarantie. Potenzielle wiederholte Nutzer nicht identifizierbar. Lokales Entwicklungsprotokoll, kein offizieller Challenge-Score.','seed':seed,'results':rows},fitted,cases
