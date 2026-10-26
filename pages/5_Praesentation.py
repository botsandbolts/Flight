from pathlib import Path
import json
import pandas as pd
import streamlit as st
st.set_page_config(page_title='Flight · Vorstellung',layout='wide')
st.title('✈️ Flight im Vorstellungsgespräch')
root=Path(__file__).resolve().parents[1]
if (root/'assets/flight_poster.jpg').exists():st.image(str(root/'assets/flight_poster.jpg'),width='stretch')
st.write('**Mein Ansatz:** Eine Kundenreise mit Produktsuche, Empfehlungen, Marketingwirkung und Deckungsbeitrag verbinden. Jede Methode bekommt eine klare Geschäftsfrage und ein prüfbares Protokoll.')
slides=sorted((root/'assets/slides').glob('*.jpg'))
if slides:
 number=st.slider('Folie',1,len(slides),1);st.image(str(slides[number-1]),width='stretch')
 deck=root/'assets/FLIGHT_Praesentation.pptx'
 if deck.exists():st.download_button('Präsentation herunterladen',deck.read_bytes(),deck.name,'application/vnd.openxmlformats-officedocument.presentationml.presentation')
st.subheader('Ausgeführte Experimente')
for path in sorted((root/'docs/benchmarks').glob('*.json')):
 with st.expander(path.stem):
  report=json.loads(path.read_text())
  if 'results' in report:st.dataframe(pd.DataFrame(report['results']),hide_index=True)
  st.json({k:v for k,v in report.items() if k!='results'})
st.caption('Kompakte Entwicklungsbenchmarks ersetzen weder Vollskalentraining noch ein Onlineexperiment. Das Projekt zeigt Code, Prüfungen und Grenzen gemeinsam.')

st.info('Neu: zwölf Unternehmensgeschichten und vier Arbeitsbereiche für KI, Agenten, Wissensarbeit und den Business Case. Die Szenarien ergänzen die ML-Labore.')
