import unittest
from flightlab.organisation import USE_CASES,inventory,retrieve,agent_run
from flightlab.llm import draft
class OrganisationTests(unittest.TestCase):
 def test_inventory(self):
  r=inventory(10,0,5,20)
  self.assertEqual(r['reorder_point'],50);self.assertEqual(r['suggested_units'],30)
 def test_workflow(self):
  r=agent_run(USE_CASES[0],dict(orders=100,basket=100,returns=.1,cogs=.5,handling=5,ad_budget=1000,daily=10,demand_std=2,lead=5,stock=10))
  self.assertEqual(r['contribution'],3000);self.assertEqual(len(r['trace']),4);self.assertEqual(r['trace'][-1]['Ergebnis']['external_actions'],0)
 def test_knowledge(self):
  r=retrieve('Lieferverzögerung Zustelltag Versandstatus')
  self.assertEqual(r[0]['id'],'SERVICE-01');self.assertEqual(len(USE_CASES),12)
 def test_llm_validation(self):
  with self.assertRaises(ValueError):draft('OpenAI','',{})
