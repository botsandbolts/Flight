"""The guided story should remain understandable and navigable."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest
APP=str(Path(__file__).resolve().parents[1]/'app.py')
class FlightSmokeTest(unittest.TestCase):
 def test_all_chapters(self):
  for index in range(8):
   with self.subTest(chapter=index):
    app=AppTest.from_file(APP,default_timeout=30).run()
    app.sidebar.radio[0].set_value(app.sidebar.radio[0].options[index]).run()
    self.assertFalse(app.exception)
    self.assertFalse(app.get('help_info'))
    if index==1:app.text_input[0].set_value('klein schwarz').run()
    elif index==2:app.main.radio[0].set_value('Was zum letzten Kontakt passt').run()
    elif index==3:
     app.slider[0].set_value(10).run()
     self.assertEqual(app.metric[0].value,'14.00 €')
    elif index==4:app.slider[0].set_value(20).run()
    elif index==5:app.slider[0].set_value(500).run()
    elif index==6:app.select_slider[0].set_value(50000).run()
    self.assertFalse(app.exception)
 def test_next_and_previous(self):
  app=AppTest.from_file(APP,default_timeout=30).run()
  app.button[1].click().run()
  self.assertEqual(app.sidebar.radio[0].value,'01 · Das passende Produkt finden')
  app.button[0].click().run()
  self.assertEqual(app.sidebar.radio[0].value,'00 · Worum geht es?')
