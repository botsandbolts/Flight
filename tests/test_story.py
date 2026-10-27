import unittest
from flightlab.story import contribution,incremental_contribution,teaching_experiment
class StoryTests(unittest.TestCase):
 def test_cost_and_marketing_examples(self):
  self.assertEqual(contribution(),24.)
  self.assertEqual(contribution(discount=10),14.)
  self.assertAlmostEqual(incremental_contribution(.6,.62,10),-5.6)
  self.assertAlmostEqual(incremental_contribution(.1,.25,10),3.3)
 def test_uncertainty_requires_more_than_a_small_count_difference(self):
  result=teaching_experiment(1000)
  self.assertEqual((result['control'],result['variant']),(25,29))
  self.assertLess(result['low_pp'],0)
  self.assertGreater(teaching_experiment(50000)['low_pp'],0)
