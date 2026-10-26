"""Smoke tests for all German story chapters and core controls."""
import unittest
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")

class FlightSmokeTest(unittest.TestCase):
    def test_all_chapters(self):
        for index in range(8):
            with self.subTest(chapter=index + 1):
                app = AppTest.from_file(APP, default_timeout=30).run()
                app.sidebar.radio[0].set_value(app.sidebar.radio[0].options[index]).run()
                self.assertEqual(len(app.exception), 0)
                if index == 0:
                    app.slider[2].set_value(40).run()
                elif index == 1:
                    app.button[0].click().run()
                    app.main.radio[0].set_value("Letzter Kontakt zählt").run()
                elif index == 2:
                    app.text_input[0].set_value("xyz").run()
                elif index == 4:
                    app.slider[0].set_value(0).run()
                elif index == 5:
                    app.main.radio[0].set_value("Erwarteter Deckungsbeitrag").run()
                self.assertEqual(len(app.exception), 0)

if __name__ == "__main__":
    unittest.main()
