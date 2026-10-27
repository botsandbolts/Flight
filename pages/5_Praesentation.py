from pathlib import Path
import json
import pandas as pd
import streamlit as st
from flightlab.ui import lab_header
st.set_page_config(page_title='Flight · Vollständige Präsentation',layout='wide')
lab_header('Business und Data Science: die vollständige Präsentation','Anna kauft online. Die acht Kapitel verbinden Entscheidungen mit technischen Demonstrationen und fortgeschrittenen Grafiken.','Die ausführliche PDF mit Methoden, Projektarchitektur, Quellen und Evidenzstatus.','Alle acht Kapitel')
root=Path(__file__).resolve().parents[1]
pdf=root/'assets/FLIGHT_Amit_Steinberg_Oktober_2026.pdf'
if pdf.exists():
 st.download_button('Vollständige PDF-Präsentation herunterladen',pdf.read_bytes(),pdf.name,'application/pdf',type='primary')
meta=root/'docs/pdf_manifest.json'
if meta.exists():
 data=json.loads(meta.read_text());st.write('**Amit Steinberg · Hamburg · Oktober 2026**')
 st.dataframe(pd.DataFrame({'Seite':range(1,len(data['pages'])+1),'Inhalt':data['pages']}),hide_index=True,width='stretch')
st.subheader('Echte Projektnachweise')
st.write('Die Grafiken unterscheiden Lehrrechnungen, synthetische Daten, trainierbare Implementierungen und gemessene Resultate. Ein kommerzieller Effekt ist bislang nicht nachgewiesen.')
for path in sorted((root/'docs/benchmarks').glob('*.json')):
 with st.expander('Messprotokoll: '+path.stem):st.json(json.loads(path.read_text()))
