from flightlab.ui import lab_header
import pandas as pd
import streamlit as st
from flightlab.search import text_search,image_search
st.set_page_config(page_title='Flight · Suchstudio',page_icon='🔎',layout='wide')
lab_header('Produkte mit Text oder Bildern suchen', 'Prüfe, welche Katalogprodukte zu einer Beschreibung passen. Beginne mit dem kleinen Beispielkatalog und dem Wortvergleich.', 'Eine sortierte Trefferliste. Sprach- und Bildmodelle sind optionale Vertiefungen mit zusätzlichem Download.', 'Schritt 2 · Das passende Produkt finden')
mode=st.radio('Werkzeug',['TF-IDF: schnelle Textbaseline','Sentence Transformer: semantischer Text','CLIP: Text findet Bilder'])
query=st.text_input('Suchwunsch','kompakte schwarze Kaffeemaschine für eine kleine Küche')
if mode.startswith('CLIP'):
 st.caption('CLIP vergleicht Text und Bild. Es erzeugt kein neues Bild. Das englische CLIP-Modell versteht englische Suchanfragen zuverlässiger.')
 images=st.file_uploader('Katalogbilder',type=['jpg','jpeg','png'],accept_multiple_files=True)
 if st.button('Bilder nach Textwunsch sortieren',disabled=not images):
  try:
   from PIL import Image
   pictures=[Image.open(f).convert('RGB') for f in images]
   with st.spinner('CLIP lädt das Modell und berechnet Bildvektoren …'):scores=image_search(pictures,query)
   for i in scores.argsort()[::-1][:8]:st.image(pictures[i],caption=f'{images[i].name} · Kosinusähnlichkeit {scores[i]:.3f}',width=250)
  except ImportError:st.error('Bitte requirements-ml.txt installieren.')
  except Exception as e:st.error(str(e))
else:
 file=st.file_uploader('Katalog-CSV mit Spalte text, optional title und price',type=['csv'])
 catalog=pd.read_csv(file,nrows=10000) if file else pd.DataFrame({'title':['Mokka Mini','Barista Pro','Reisebecher'],'text':['Kleine schwarze Kaffeemaschine für Espresso in kleinen Küchen','Große silberne Premium-Espressomaschine mit Milchaufschäumer','Thermobecher für Kaffee unterwegs'],'price':[89,349,25]})
 if not file:st.caption('Synthetischer Minikatalog. Für echte Suche eigene Metadaten aus einem zulässigen öffentlichen Katalog laden.')
 if 'text' not in catalog:st.error('Spalte text fehlt.')
 elif st.button('Passende Produkte finden'):
  try:
   with st.spinner('Suchvektoren werden berechnet …'):catalog['Ähnlichkeit']=text_search(catalog.text.fillna('').astype(str),query,mode.startswith('Sentence'))
   st.dataframe(catalog.sort_values('Ähnlichkeit',ascending=False).head(10),hide_index=True)
  except ImportError:st.error('Bitte requirements-ml.txt installieren.')
  except Exception as e:st.error(str(e))
st.info('Semantische Modelle laden beim ersten Einsatz Gewichte aus dem Modell-Hub. Der erste Start braucht Netzwerk und Speicher. Preise und Bestand brauchen zusätzliche harte Filter. Ähnlichkeit ist keine Kaufwahrscheinlichkeit.')
