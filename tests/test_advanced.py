import unittest
import numpy as np
from flightlab.advanced import TOPICS,plot_data,figure,graph_figure
class AdvancedTests(unittest.TestCase):
 def test_attention_is_normalized_and_causal(self):
  d=plot_data(2)
  np.testing.assert_allclose(d['matrix'].sum(axis=1),1)
  self.assertEqual(np.triu(d['matrix'],1).sum(),0)
 def test_every_chapter_has_technical_evidence(self):
  self.assertEqual(len(TOPICS),8)
  for i in range(8):
   self.assertTrue(TOPICS[i]['tech']);self.assertTrue(TOPICS[i]['limit'])
   if i<7:self.assertIsNotNone(figure(i,180 if i==5 else 10 if i==4 else 1))
 def test_cost_surface_and_cosine(self):
  self.assertEqual(plot_data(3)['matrix'][0,0],32)
  np.testing.assert_allclose(np.diag(plot_data(1)['matrix']),1)
