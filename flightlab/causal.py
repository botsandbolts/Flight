"""Honest split T-learner for randomized treatment data. Never use exposure as treatment."""
import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

def uplift_benchmark(df,seed=42):
 features=[c for c in df if c.startswith('f') and c[1:].isdigit()]
 if not features or not {'treatment','conversion'}.issubset(df):raise ValueError('Criteo-Schema: f0…f11, treatment, conversion.')
 d=df[features+['treatment','conversion']].apply(pd.to_numeric,errors='coerce').dropna()
 if not d.treatment.isin([0,1]).all() or not d.conversion.isin([0,1]).all():raise ValueError('Treatment und Conversion müssen 0/1 sein.')
 train,test=train_test_split(d,test_size=.3,random_state=seed,stratify=d.treatment)
 models=[]
 for treatment in [0,1]:
  group=train[train.treatment==treatment]
  if len(group)<50 or group.conversion.nunique()<2:raise ValueError('Je Trainingsarm mindestens 50 Zeilen und beide Outcomes erforderlich.')
  model=HistGradientBoostingClassifier(max_iter=80,max_leaf_nodes=15,l2_regularization=10,random_state=seed).fit(group[features],group.conversion);models.append(model)
 p0=models[0].predict_proba(test[features])[:,1];p1=models[1].predict_proba(test[features])[:,1];uplift=p1-p0
 # Propensity estimated from TRAIN randomization ratio, not individual exposure.
 e=train.treatment.mean();t=test.treatment.to_numpy();y=test.conversion.to_numpy()
 pseudo=t*y/e-(1-t)*y/(1-e);order=np.argsort(-uplift);curve=np.r_[0,np.cumsum(pseudo[order])]/len(test);fraction=np.linspace(0,1,len(curve));random=fraction*curve[-1]
 area=float(np.trapezoid(curve-random,fraction))
 out=pd.DataFrame({'Anteil':fraction,'Modell':curve,'Zufall':random})
 return {'test_rows':len(test),'train_rows':len(train),'treatment_rate_train':float(e),'AUUC_above_random':area,'ATE_IPW':float(pseudo.mean()),'caveat':'Kein individueller Effektbeweis. Criteo wurde nichtuniform subsampelt; kein Geschäftsuplift des Originalwerbetreibenden.'},out,pd.DataFrame({'p0':p0,'p1':p1,'uplift':uplift})
