"""UI return values must not turn into documentation panels in the story."""
import unittest
from pathlib import Path
import tomllib
from streamlit import config
from streamlit.testing.v1 import AppTest

class RenderingTests(unittest.TestCase):
 def test_ui_objects_do_not_appear_as_help(self):
  root=Path(__file__).resolve().parents[1]
  settings=tomllib.loads((root/'.streamlit/config.toml').read_text())
  before_magic=config.get_option('runner.magicEnabled')
  before_last=config.get_option('magic.displayLastExprIfNoSemicolon')
  try:
   # Recreate the notebook-like setting that previously exposed DeltaGenerator.
   config.set_option('magic.displayLastExprIfNoSemicolon',True)
   config.set_option('runner.magicEnabled',settings['runner']['magicEnabled'])
   for path,expected in [('app.py','Sie hat wenig Platz'),('pages/6_KI_im_Unternehmen.py','Er zerlegt die Rechnung')]:
    with self.subTest(page=path):
     app=AppTest.from_file(str(root/'app.py'),default_timeout=30).run()
     if path!='app.py':app.switch_page(path).run()
     self.assertFalse(app.exception)
     self.assertFalse(app.get('help_info'))
     rendered='\n'.join(str(item.value) for item in app.markdown)
     self.assertIn(expected,rendered)
     self.assertNotIn('DeltaGenerator',rendered)
  finally:
   config.set_option('runner.magicEnabled',before_magic)
   config.set_option('magic.displayLastExprIfNoSemicolon',before_last)
