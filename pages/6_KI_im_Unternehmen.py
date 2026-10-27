import pandas as pd
import streamlit as st
from flightlab.organisation import USE_CASES
from flightlab.ui import lab_header,detail
st.set_page_config(page_title='Flight · Weitere Anwendungen',layout='wide')
lab_header('Weitere Anwendungen im Unternehmen',
 'Die Hauptgeschichte folgt Annas Einkauf. Hier findest du weitere Einsatzideen, geordnet nach dem Problem einer Abteilung.',
 'Eine verständliche Fallkarte mit Datenbedarf, Entscheidung und Erfolgskriterium. Die Karten beschreiben mögliche Einsätze, keine zwölf fertig betriebenen Systeme.',
 'Schritt 6 · Das Unternehmen abstimmen')
labels=[c['role']+' · '+c['name'].split(' · ',1)[1] for c in USE_CASES]
selected=st.selectbox('Welcher Bereich interessiert dich?',labels)
c=USE_CASES[labels.index(selected)]
st.subheader('Das Problem');st.write(c['problem'])
st.subheader('Wie die Unterstützung helfen könnte');st.write(c['simple'])
st.subheader('Welche Entscheidung beim Team bleibt');st.write(c['decision'])
st.write('**Woran wir den Nutzen prüfen würden:** '+c['kpi'])
with st.expander('Welche Daten dafür nötig sind'):
 st.write(c['data'])
detail(c['business'],c['tech'],'Anwendungsfall zur Einordnung. Der zugehörige Datenzugriff und Produktionsbetrieb sind damit nicht nachgewiesen.')
st.caption('Eine passende Pointe: '+c['joke'])
with st.expander('Die Begriffe kurz erklärt'):
 st.dataframe(pd.DataFrame([
 ['KI / AI','Oberbegriff für Verfahren wie Erkennen, Vorhersagen und Generieren.'],
 ['Sprachmodell','Formuliert zum Beispiel einen Entwurf aus bereitgestellten Fakten.'],
 ['Copilot','Unterstützt einen Menschen bei einer Aufgabe.'],
 ['Agent','Kann ein Ziel über mehrere Schritte und Werkzeuge verfolgen.'],
 ['Fester Workflow','Der Entwickler legt die Schritte vorher fest. Das nutzt Flight aktuell.'],
 ['RAG','Passende Quellen suchen und sie beim Formulieren berücksichtigen.'],
 ],columns=['Begriff','Bedeutung']),hide_index=True,width='stretch')
with st.expander('ChatGPT, Claude und andere Anbieter einordnen'):
 st.write('OpenAI und Anthropic sind in Flight optional über ihre APIs für Textentwürfe angebunden. ChatGPT und Claude sind außerdem Endnutzerprodukte. Ein Chat-Abonnement ist keine Zusage eines API-Guthabens.')
 st.write('Wir würden Anbieter mit denselben eigenen Testaufgaben auf Antwortqualität, Belege, Laufzeit und Gesamtkosten prüfen. Gemini oder lokal betriebene Modelle sind mögliche Alternativen; dafür gibt es hier keine implementierte Anbindung.')
 st.markdown('[OpenAI: Werkzeuge](https://developers.openai.com/api/docs/guides/tools) · [Anthropic: Tool Use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)')
st.page_link('pages/7_Agenten_Kommandozentrale.py',label='Einen vorhandenen lokalen Arbeitsablauf ausprobieren')
