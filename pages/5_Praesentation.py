from pathlib import Path
import json
import pandas as pd
import streamlit as st
from flightlab.ui import lab_header
st.set_page_config(page_title='Flight · Folien und Nachweise',layout='wide')
lab_header('Die Geschichte als Präsentation',
 'Die Folien erzählen denselben Einkauf wie die Hauptansicht. Erst kommen die Entscheidungen, dann die Methoden und Daten im Anhang.',
 'Eine geführte Präsentation und getrennte Nachweise zum tatsächlichen Projektstand.',
 'Schritt 8 · Was Flight tatsächlich zeigt')
root=Path(__file__).resolve().parents[1]
meta=root/'docs/presentation.json'
content=json.loads(meta.read_text()) if meta.exists() else {'slides':[]}
slides=sorted((root/'assets/slides').glob('*.jpg'))
if slides:
 labels=[f'{i+1:02} · '+(content['slides'][i]['title'] if i<len(content['slides']) else f'Folie {i+1}') for i in range(len(slides))]
 selected=st.selectbox('Folie auswählen',labels)
 number=labels.index(selected)
 st.image(str(slides[number]),width='stretch')
 if number<len(content['slides']):st.write('**Worauf es hier ankommt:** '+content['slides'][number]['takeaway'])
 deck=root/'assets/FLIGHT_Praesentation.pptx'
 if deck.exists():st.download_button('Die gesamte Präsentation herunterladen',deck.read_bytes(),deck.name,'application/vnd.openxmlformats-officedocument.presentationml.presentation')
st.divider();st.subheader('Was die bisherigen Versuche belegen')
st.write('Die Codepfade laufen in lokalen Tests. Der kleine Amazon-Test hat noch keinen brauchbaren Empfehlungsgewinn gezeigt. Ein ungeeignetes Criteo-Dateipräfix wurde wegen fehlender Kontrollgruppe vor dem Training zurückgewiesen. Ein Geschäftseffekt ist damit nicht nachgewiesen.')
for path in sorted((root/'docs/benchmarks').glob('*.json')):
 with st.expander('Messprotokoll: '+path.stem):
  report=json.loads(path.read_text())
  if 'results' in report:st.dataframe(pd.DataFrame(report['results']),hide_index=True,width='stretch')
  st.json({k:v for k,v in report.items() if k!='results'})
st.caption('Die Story nutzt fiktive Annahmen. Diese Messprotokolle dokumentieren davon getrennte Entwicklungstests.')
