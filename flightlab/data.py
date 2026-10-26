"""Independent public datasets, normalized without cross-store identity joins."""
import ast
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

SOURCES = {
 'Retailrocket': ('https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset','Ereignisse: timestamp, visitorid, itemid, event'),
 'REES46': ('https://rees46.com/en/datasets','Ereignisse: event_time, user_id, product_id, event_type'),
 'Amazon-M2': ('https://github.com/HaitaoMao/Amazon-M2-Session-Recommendation','Sessions: prev_items, next_item, locale; kein globaler Zeitstempel'),
 'Amazon Reviews 2023': ('https://amazon-reviews-2023.github.io/','JSONL: user_id, parent_asin, timestamp; Rezensionen sind keine Klicks'),
 'Amazon ESCI': ('https://github.com/amazon-science/esci-data','Suchrelevanz; separate query-product-Aufgabe'),
 'Criteo Uplift': ('https://huggingface.co/datasets/criteo/criteo-uplift','Randomisiertes Treatment, conversion, f0–f11; CC-BY-NC-SA-4.0'),
}

def fingerprint(frame):
 return hashlib.sha256(pd.util.hash_pandas_object(frame,index=True).values.tobytes()).hexdigest()

def demo_events(users=150, seed=42):
 rng=np.random.default_rng(seed);rows=[]
 # Deliberate category transitions plus noise; never sold as public evidence.
 for user in range(users):
  group=user%4
  for step in range(12):
   item=group*8+(step%8) if rng.random()>.18 else int(rng.integers(32))
   rows.append((str(user),str(item),pd.Timestamp('2025-01-01',tz='UTC')+pd.Timedelta(hours=step*users+user),'view'))
 return pd.DataFrame(rows,columns=['user','item','time','event'])

def normalize(frame,source):
 if source=='Retailrocket':
  d=frame.rename(columns={'visitorid':'user','itemid':'item','timestamp':'time'}).copy()
  d['time']=pd.to_datetime(pd.to_numeric(d['time'],errors='coerce'),unit='ms',utc=True,errors='coerce')
 elif source=='REES46':
  d=frame.rename(columns={'user_id':'user','product_id':'item','event_time':'time','event_type':'event'}).copy()
  d['time']=pd.to_datetime(d['time'],utc=True,errors='coerce')
 elif source=='Amazon Reviews 2023':
  d=frame.rename(columns={'user_id':'user','parent_asin':'item','timestamp':'time'}).copy();d['event']='review'
  d['time']=pd.to_datetime(d['time'],utc=True,errors='coerce') if pd.api.types.is_datetime64_any_dtype(d['time']) else pd.to_datetime(pd.to_numeric(d['time'],errors='coerce'),unit='ms',utc=True,errors='coerce')
 else:raise ValueError('Dieser Adapter verarbeitet Ereignisse, keine Session- oder Suchdaten.')
 required=['user','item','time','event']
 if not set(required).issubset(d):raise ValueError('Benötigte normalisierte Spalten: '+str(required))
 d=d.dropna(subset=required)[required];d[['user','item']]=d[['user','item']].astype(str)
 return d.sort_values(['time','user'],kind='stable').drop_duplicates().reset_index(drop=True)

def temporal_split(events, fraction=.8):
 times=np.sort(events.time.unique())
 if len(times)<3:raise ValueError('Mindestens drei verschiedene Zeitpunkte erforderlich.')
 cutoff=times[min(len(times)-1,max(1,int(len(times)*fraction)))]
 return events[events.time<cutoff].copy(),events[events.time>=cutoff].copy(),str(cutoff)

def sequences(events):
 return events.sort_values('time',kind='stable').groupby('user',sort=True).item.apply(list).tolist()

def m2_sequences(frame):
 if not {'prev_items','next_item','locale'}.issubset(frame):raise ValueError('Amazon-M2 benötigt prev_items, next_item und locale.')
 rows=[]
 for r in frame.itertuples():
  # Published files use NumPy-style string arrays, sometimes without commas.
  import re
  raw=str(r.prev_items)
  try:items=ast.literal_eval(raw) if ',' in raw else re.findall(r"['\"]([^'\"]+)['\"]",raw)
  except (ValueError,SyntaxError):items=re.findall(r"['\"]([^'\"]+)['\"]",raw)
  if not isinstance(items,(list,tuple)):raise ValueError('prev_items muss eine Liste sein.')
  rows.append([str(r.locale)+':'+str(x) for x in [*items,r.next_item]])
 return rows

def load_path(path,source,limit=200000):
 if source=='Amazon Reviews 2023':
  return normalize(pd.read_json(path,lines=True,nrows=limit),source)
 return normalize(pd.read_csv(path,nrows=limit),source)
