from flightlab.ui import lab_header
from pathlib import Path
import pandas as pd
import streamlit as st
from flightlab.causal import uplift_benchmark
st.set_page_config(page_title='Flight · Marketinglabor',page_icon='🎯',layout='wide')
lab_header('Hat die Werbung zusätzliche Wirkung?', 'Ein Modell schätzt Kaufwahrscheinlichkeiten mit und ohne Werbung. Dafür brauchen wir Daten aus einer geeigneten Treatment- und Kontrollgruppe.', 'Ein auf getrennten Daten geprüftes Marketingmodell. Seine Schätzung ist kein individueller Wirkungsbeweis.', 'Schritt 5 · Einen Rabatt begründen')
with st.expander('🎨 Die Geschichte als Poster'):
 st.image(str(Path(__file__).resolve().parents[1]/'assets/marketing_poster.jpg'),width='stretch')
st.write('Der Gutschein soll Verhalten verändern. Er soll keine Treueprämie für ohnehin sichere Käufe sein.')
st.markdown('[Criteo Uplift: öffentliche Originaldaten](https://huggingface.co/datasets/criteo/criteo-uplift)')
st.caption('CC-BY-NC-SA-4.0. Lizenz vor Weiterverwendung beachten. Nichtuniformes Subsampling verhindert Rückschlüsse auf die ursprüngliche geschäftliche Inkrementalität.')
f=st.file_uploader('Criteo-CSV oder CSV.GZ hochladen',type=['csv','gz'])
limit=st.slider('Zeilenlimit',10000,500000,100000,10000)
if f and st.button('T-Learner trainieren und auf separaten Daten prüfen'):
 try:
  frame=pd.read_csv(f,nrows=limit,compression='gzip' if f.name.endswith('.gz') else None)
  with st.spinner('Zwei Modelle lernen: Treatment und Kontrolle. Keines bekommt die Testantworten.'):
   metrics,curve,pred=uplift_benchmark(frame)
  st.session_state['uplift_result']=(metrics,curve,pred)
 except Exception as e:st.error(str(e))
if 'uplift_result' in st.session_state:
 metrics,curve,pred=st.session_state['uplift_result']
 st.write('Die Kurve vergleicht die geschätzte Wirkung bei Modell-Auswahl mit zufälliger Auswahl. Ein höherer Verlauf ist unter diesem Prüfprotokoll günstiger.')
 with st.expander('Technische Kennzahlen und Laufprotokoll'):st.json(metrics)
 st.line_chart(curve.set_index('Anteil')[['Modell','Zufall']]);st.dataframe(pred.head(20).rename(columns={'p0':'Geschätzte Kaufchance ohne Werbung','p1':'Geschätzte Kaufchance mit Werbung','uplift':'Geschätzter Unterschied'}),hide_index=True)
 st.download_button('Vorhersagen exportieren',pred.to_csv(index=False).encode(),'flight_uplift.csv','text/csv')
 st.info('Kurve: kumuliertes IPW-Outcome je Testperson bei Auswahl der höchsten Uplifts. AUUC above random ist die Fläche oberhalb zufälliger Auswahl. Kein Beweis individueller Effekte und keine Prognose von Eurogewinn.')
with st.expander('Einfach / Geschäft / Technik'):
 st.write('Einfach: Vergleiche die Kaufchance mit und ohne Werbung. Geschäft: Ziel ist zusätzliche Wirkung statt bloßer Conversion. Technik: T-Learner aus zwei Histogram Gradient Boosting-Modellen, stratifizierter Train/Test-Split, randomisierte Treatmentquote aus dem Training und inverse Wahrscheinlichkeitsgewichtung. exposure ist nach Treatment entstanden und bleibt ausgeschlossen.')
