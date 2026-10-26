from pathlib import Path
import pandas as pd
import streamlit as st
from flightlab.organisation import retrieve,HANDBOOK
st.set_page_config(page_title='Flight · Wissensstudio',layout='wide',page_icon='📚')
st.title('📚 Unternehmenswissen statt KI-Gedächtnistheater')
st.write('Ein Kunde fragt nach seiner verspäteten Bestellung. Die KI darf eine Antwort vorbereiten. Einen erfundenen Zustelltag darf sie nicht mit Geschenkband versehen.')
query=st.text_input('Frage an das fiktive Handbuch','Was tun bei Lieferverzögerung und fehlendem Zustelltermin?')
if st.button('Quellen suchen'):
 results=retrieve(query)
 if not results:st.info('Keine passende Quelle gefunden. Eine Rückfrage ist besser als eine erfundene Regel.')
 for r in results:
  with st.container(border=True):st.subheader(r['id']+' · '+r['title']);st.write(r['text']);st.caption(f'TF-IDF-Retrievalscore {r["retrieval_score"]:.3f}, keine Wahrheitswahrscheinlichkeit.')
 st.caption('Aktiv ist Quellenretrieval, keine generierte Antwort. Das kleine synthetische Handbuch dient der Mechanik, nicht realen Serviceentscheidungen.')
with st.expander('Das vollständige fiktive Unternehmenshandbuch'):
 for d in HANDBOOK:st.write('**'+d['id']+' · '+d['title']+'**');st.write(d['text'])
st.divider();st.subheader('🎨 Content-Fabrik: Kreativität mit Faktenanschluss')
product=st.text_input('Fiktiver Produktname','Mokka Mini');attribute=st.text_input('Bestätigte Eigenschaft','kompakte Bauform');price=st.number_input('Angenommener Nettopreis (€)',min_value=0.,value=89.)
if st.button('Drei deterministische Textvarianten erstellen'):
 variants=[f'{product}: {attribute}. Mehr Platz für deinen Morgenkaffee. Nettopreis im Szenario: {price:.2f} €.',f'Deine Küche ist klein. Dein Kaffeewunsch nicht. {product} mit {attribute}. Szenariopreis netto {price:.2f} €.',f'{product}. {attribute.capitalize()}. Für einen Morgen mit weniger Suchen und mehr Kaffee. Nettopreis im Szenario {price:.2f} €.']
 for i,v in enumerate(variants,1):st.write(f'**Variante {i}:** '+v)
 st.caption('Vorlagen, keine LLM-Generierung. Claims sind eingegebene Demoannahmen und wurden nicht gegen einen realen Katalog verifiziert. Live-Modellentwürfe sind separat im Agentencockpit verfügbar.')
st.write('**Testidee:** Varianten randomisiert gegeneinander testen. Klickrate allein reicht nicht, wenn zusätzliche Bestellungen keinen Beitrag liefern. Eine Bild-KI erzeugt ein Motiv, aber keine neue Produkteigenschaft.')
