import unittest
import numpy as np
import pandas as pd
from flightlab.data import demo_events,temporal_split,normalize,m2_sequences
from flightlab.benchmark import run,run_sessions
from flightlab.causal import uplift_benchmark
from flightlab.recommend import Popularity,evaluate

class ModelTests(unittest.TestCase):
 def test_split_and_metric(self):
  d=demo_events(20);a,b,_=temporal_split(d)
  self.assertLess(a.time.max(),b.time.min())
  model=Popularity().fit([['a','a','b']]);result=evaluate(model,[(['b'],'a'),(['b'],'new')],1)
  self.assertEqual(result['Recall@1'],1);self.assertEqual(result['cold_targets'],1)
 def test_models(self):
  report,models,cases=run(demo_events(25),max_cases=30)
  self.assertEqual(len(models),3)
  self.assertTrue(all(0<=r['NDCG@10']<=1 for r in report['results']))
 def test_neural(self):
  try:import torch
  except ImportError:self.skipTest('Optional torch nicht installiert')
  report,models,_=run(demo_events(20),['BERT4Rec','SASRec','LightGCN'],epochs=1,max_cases=10)
  for m in models.values():self.assertTrue(np.isfinite(m.scores(['0','1'])).all())
 def test_adapters(self):
  r=pd.DataFrame({'visitorid':[1],'itemid':[2],'timestamp':[1700000000000],'event':['view']})
  self.assertEqual(normalize(r,'Retailrocket').iloc[0]['item'],'2')
  reviews=pd.DataFrame({'user_id':['u'],'parent_asin':['i'],'timestamp':[pd.Timestamp('2024-01-01')]})
  self.assertEqual(len(normalize(reviews,'Amazon Reviews 2023')),1)
  m=m2_sequences(pd.DataFrame({'prev_items':["['A' 'B']"],'next_item':['C'],'locale':['DE']}))
  self.assertEqual(m,[['DE:A','DE:B','DE:C']])
 def test_uplift(self):
  rng=np.random.default_rng(42);n=1000
  df=pd.DataFrame({'f0':rng.normal(size=n),'treatment':rng.integers(2,size=n),'conversion':rng.integers(2,size=n)})
  report,curve,pred=uplift_benchmark(df)
  self.assertEqual(len(pred),report['test_rows']);self.assertAlmostEqual(curve.iloc[-1].Modell,report['ATE_IPW'])
 def test_sessions(self):
  report,_,_=run_sessions([['a','b','c'] for _ in range(20)])
  self.assertIn('Session-Holdout',report['protocol'])
if __name__=='__main__':unittest.main()
