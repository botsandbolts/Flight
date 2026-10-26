import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
class PageTests(unittest.TestCase):
 def test_pages(self):
  for p in sorted((Path(__file__).resolve().parents[1]/'pages').glob('*.py')):
   with self.subTest(page=p.name):
    a=AppTest.from_file(str(p),default_timeout=30).run()
    self.assertEqual(len(a.exception),0)
    if p.name.startswith(('1_','2_','7_','8_')):
     a.button[0].click().run();self.assertEqual(len(a.exception),0)
