import json
import streamlit as st
from flightlab.organisation import USE_CASES,agent_run
from flightlab.llm import draft
from flightlab.ui import lab_header
st.set_page_config(page_title='Flight · Gemeinsamer Arbeitsauftrag',layout='wide',page_icon='🤝')
lab_header('Ein Arbeitsauftrag für Einkauf, Finanzen und Service',
 'Bevor der Shop eine Kampagne verstärkt, prüfen wir Beitrag und Bestand. Danach bereiten wir eine nachvollziehbare Antwort vor.',
 'Eine lokale Rechnung, passende Handbuchstellen und einen protokollierten Entwurf. Es werden keine Nachrichten, Bestellungen oder Buchungen ausgelöst.',
 'Schritt 6 · Das Unternehmen abstimmen')
st.write('**Ausgangslage:** 2.000 Beispielbestellungen zu je 100 € netto. Pro Bestellung fallen 50 € Ware sowie 14 € für Abwicklung und erwartete Retouren an. Werbekosten kommen hinzu.')
a,b=st.columns(2)
with a:ads=st.slider('Werbekosten für alle 2.000 Bestellungen (€)',0,120000,24000,1000)
with b:stock=st.slider('Verfügbarer Bestand (Stück)',0,500,180,10)
st.caption('Bestandsannahme: 40 Stück Tagesbedarf, sieben Tage Lieferzeit. Der Sicherheitsbestand nutzt 12 Stück tägliche Standardabweichung und z=1,65.')
inputs=dict(orders=2000,basket=100.,returns=0.,cogs=.5,handling=14.,ad_budget=ads,daily=40.,demand_std=12.,lead=7,stock=stock)
if st.button('Beitrag und Bestand gemeinsam prüfen',type='primary'):
 st.session_state['agent_report']=agent_run(USE_CASES[0],inputs)
if 'agent_report' in st.session_state:
 report=st.session_state['agent_report']
 st.subheader('Ergebnis des letzten ausgeführten Auftrags')
 st.caption('Nach Eingabeänderungen erneut prüfen. Die folgenden Werte stammen aus dem gespeicherten Lauf.')
 a,b=st.columns(2)
 with a:st.metric('Beitrag nach Werbung, insgesamt',f'{report["contribution"]:,.0f} €')
 with b:st.metric('Vorgeschlagene Auffüllmenge',f'{report["inventory"]["suggested_units"]} Stück')
 st.write('**Was bedeutet das?** Die Auffüllmenge gleicht den Bestand zum berechneten Meldebestand aus. Sie ist ein Vorschlag und keine Bestellung. Kosten, Mindestmengen und unsichere Lieferzeiten sind noch nicht berücksichtigt.')
 st.write('**Nächster Schritt:** '+('Kosten und Angebot prüfen, bevor die Kampagne mehr Bestellungen erzeugt.' if report['contribution']<0 else 'Bestand und Lieferfähigkeit beim Einkauf bestätigen lassen; dann über die Kampagne entscheiden.'))
 st.subheader('Welche Regel hilft dem Kundenservice?')
 evidence=next((d for d in report['evidence'] if d['id']=='SERVICE-01'),None)
 if not evidence:
  from flightlab.organisation import retrieve
  evidence=retrieve('Lieferverzögerung Zustelltag Versandstatus')[0]
 st.write(evidence['text']);st.caption('Fiktive Quelle: '+evidence['id'])
 st.info('**Einordnung:** Das ist ein fester, lokaler Ablauf mit Rechenwerkzeugen und Quellensuche. Ein autonomer Agent würde weitere Schritte selbst auswählen; das tut diese Demo nicht.')
 with st.expander('Rechenweg und vollständiges Entscheidungsprotokoll'):
  st.json(report)
 st.download_button('Protokoll herunterladen',json.dumps(report,ensure_ascii=False,indent=2),'flight_arbeitsauftrag.json','application/json')
 with st.expander('Optional: Ein Sprachmodell formuliert den Textentwurf'):
  st.write('OpenAI oder Anthropic erhält nur das angezeigte synthetische Szenarioprotokoll. Ein Aufruf kann API-Kosten verursachen. Schlüssel gehören in die Server-Umgebung, nicht ins Repository. Ohne Schlüssel funktioniert die lokale Rechnung trotzdem.')
  provider=st.selectbox('API-Anbieter',['OpenAI','Anthropic']);model=st.text_input('Verfügbare Modell-ID aus deinem API-Konto')
  agree=st.checkbox('Das sichtbare Szenarioprotokoll an diesen Anbieter senden')
  if st.button('Textentwurf anfordern',disabled=not agree or not model):
   try:
    with st.spinner('Entwurf wird formuliert …'):answer,usage=draft(provider,model,report)
    st.markdown(answer)
    with st.expander('Gemeldeter API-Verbrauch'):st.json(usage)
    st.caption('Ein KI-Textentwurf, keine ausgeführte Aktion. Diese Anbindung wurde ohne Zugangsschlüssel nicht live geprüft.')
   except Exception:st.error('Anfrage fehlgeschlagen. API-Zugang, Modell-ID und Serverkonfiguration prüfen.')
