from pathlib import Path
import pandas as pd
import streamlit as st
from flightlab.organisation import USE_CASES
st.set_page_config(page_title='Flight · KI im Unternehmen',layout='wide',page_icon='🏢')
st.title('🏢 Staffel 2: Die KI bekommt einen Firmenausweis')
st.write('Anna wollte nur Kaffee. Jetzt will die Geschäftsführung wissen, wie KI dem ganzen Unternehmen hilft. Zwölf Episoden zeigen konkrete Probleme, passende Werkzeuge und verantwortliche Menschen.')
p=Path(__file__).resolve().parents[1]/'assets/organisation_poster.jpg'
if p.exists():st.image(str(p),width='stretch')
case=st.selectbox('Episode auswählen',[x['name'] for x in USE_CASES]);c=next(x for x in USE_CASES if x['name']==case)
st.caption(c['role']+' · '+c['agent']);st.header(c['problem'])
a,b,d=st.tabs(['🧑 Ohne Fachchinesisch','💼 Business Case','🔬 Maschinenraum'])
a.write(c['simple']);b.write(c['business']);d.write(c['tech'])
st.success('**Die nächste Entscheidung:** '+c['decision']);st.info('**Kaffeepause:** '+c['joke'])
x,y=st.columns(2)
with x:st.subheader('Welche Daten brauchen wir?');st.write(c['data'])
with y:st.subheader('Woran merken wir den Nutzen?');st.write(c['kpi'])
st.divider();st.subheader('KI, Copilot, Agent: Wer macht eigentlich was?')
st.dataframe(pd.DataFrame([
 ['KI / AI','Oberbegriff für Verfahren, die Aufgaben wie Erkennen, Vorhersagen oder Generieren übernehmen.','Ein Nachfrage- oder Sprachmodell'],
 ['Generative KI','Erzeugt Texte, Bilder oder Code.','Antwortentwurf oder Kampagnenvariante'],
 ['Copilot','Hilft einem Menschen innerhalb einer Aufgabe.','Serviceantwort mit Quellen vorbereiten'],
 ['Agent','Verfolgt ein Ziel über Schritte und nutzt erlaubte Werkzeuge.','Bestand prüfen, Beitrag rechnen, Vorschlag dokumentieren'],
 ['Workflow','Festgelegte Abfolge, deren Schritte der Entwickler bestimmt.','Der lokale Flight-Agentenablauf'],
 ['Multi-Agent-System','Mehrere Rollen tauschen strukturierte Ergebnisse aus.','Controller, Einkauf und Qualitätsprüfer'],
 ['RAG','Sucht passende Dokumente vor dem Formulieren einer Antwort.','Antwort mit Handbuch-ID statt Gedächtnistheater']
],columns=['Begriff','Einfach erklärt','Im Unternehmen']),hide_index=True)
st.subheader('ChatGPT, Claude & Co. im Arbeitsalltag')
st.write('ChatGPT und Claude sind auch Endnutzerprodukte. Die optionalen Flight-Anbindungen verwenden die separaten OpenAI- beziehungsweise Anthropic-APIs. Ein Chat-Abonnement ist keine Zusage eines API-Guthabens.')
st.dataframe(pd.DataFrame([
 ['ChatGPT / OpenAI','Analyseentwürfe, Ideen, Code und belegte Zusammenfassungen','Optionaler Responses-API-Adapter; Modell-ID und Server-Key erforderlich'],
 ['Claude / Anthropic','Dokumentarbeit, Schreiben, Analyse und werkzeuggestützte Abläufe','Optionaler Messages-API-Adapter; Modell-ID und Server-Key erforderlich'],
 ['Gemini / Google','Weitere mögliche Modellfamilie für denselben Evaluationsprozess','Architekturoption, kein Adapter implementiert'],
 ['Lokale offene Modelle','Eigener Betrieb kann Anforderungen an Kontrolle und Infrastruktur erfüllen','Architekturoption, kein lokaler Modellserver implementiert']
],columns=['Produktfamilie','Mögliche Aufgaben, kein Qualitätsranking','Flight-Status']),hide_index=True)
st.caption('Den Anbieter anhand eigener Testfälle, Kosten, Latenz, Datenanforderungen und Fehlern auswählen. Modellnamen und Verfügbarkeit verändern sich.')
with st.expander('Der innovative Teil: Ein Unternehmensgedächtnis für Entscheidungen'):
 st.write('Jeder Vorschlag bekommt Geschäftsfrage, Datenstand, Rechenweg, Quellen, verantwortliche Person und spätere Messung. So wird aus einer hübschen KI-Antwort eine prüfbare Entscheidung. Ein zweiter Modellaufruf ist dabei kein unabhängiger Wahrheitsbeweis.')
 st.write('Beispiel: Einkauf meldet knappen Bestand. Marketing stoppt die Bewerbung im Vorschlag. Der Controller berechnet den DB-Effekt. Der Mensch entscheidet über Kampagne und Nachbestellung. Flight simuliert diesen Ablauf ohne ERP- oder Werbekonto-Zugriff.')
st.markdown('[OpenAI: Werkzeuge](https://developers.openai.com/api/docs/guides/tools) · [Anthropic: Tool-Use-Vertrag](https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works)')
