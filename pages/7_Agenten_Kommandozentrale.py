import json
import streamlit as st
from flightlab.organisation import USE_CASES,agent_run
from flightlab.llm import draft
st.set_page_config(page_title='Flight · Agenten',layout='wide',page_icon='🤖')
st.title('🤖 Die Agenten-Kommandozentrale')
st.write('Ein Controller, eine Einkäuferin und ein Wissensassistent betreten einen Shop. Diesmal rechnen sie, bevor jemand „Synergie“ sagt.')
st.info('Aktiv: fester lokaler Workflow mit echten Python-Rechenwerkzeugen und Dokument-Retrieval. Kein autonomer LLM-Agent, keine externen Aktionen. Optional kann ein Sprachmodell den belegten Ergebnisentwurf formulieren.')
case=st.selectbox('Geschäftslage',[c['name'] for c in USE_CASES]);c=next(x for x in USE_CASES if x['name']==case)
a,b=st.columns(2)
with a:
 orders=st.number_input('Bestellungen',min_value=1,max_value=100000,value=2000)
 basket=st.number_input('Netto-Warenkorb vor Retouren (€)',min_value=1.,max_value=10000.,value=100.)
 returns=st.slider('Retourenquote (%)',0,70,15)/100
 cogs=st.slider('Wareneinsatz (% des realisierten Erlöses)',0,95,48)/100
 handling=st.number_input('Abwicklung je Bestellung (€)',min_value=0.,max_value=200.,value=7.)
 ads=st.number_input('Werbebudget (€)',min_value=0.,max_value=1000000.,value=40000.)
with b:
 daily=st.number_input('Tagesnachfrage (Stück)',min_value=0.,max_value=10000.,value=40.)
 std=st.number_input('Standardabweichung der Tagesnachfrage',min_value=0.,max_value=5000.,value=12.)
 lead=st.number_input('Lieferzeit (Tage, konstant)',min_value=1,max_value=365,value=7)
 stock=st.number_input('Lagerbestand (Stück)',min_value=0,max_value=100000,value=180)
 st.caption('Meldebestand-Demo mit z=1,65. Keine Bestellkosten, Mindestbestellmenge oder Lieferzeitunsicherheit berücksichtigt. Vorschlag ist kein optimales Los.')
inputs=dict(orders=orders,basket=basket,returns=returns,cogs=cogs,handling=handling,ad_budget=ads,daily=daily,demand_std=std,lead=lead,stock=stock)
if st.button('▶ Auftrag als lokalen Workflow ausführen'):
 st.session_state['agent_report']=agent_run(c,inputs)
if 'agent_report' in st.session_state:
 report=st.session_state['agent_report'];st.subheader(report['case']);st.caption('Gespeicherter letzter Lauf; geänderte Eingaben erst mit erneutem Start übernehmen.')
 a,b,c1=st.columns(3);a.metric('DB nach Marketing',f'{report["contribution"]:,.0f} €');b.metric('Meldebestand',report['inventory']['reorder_point']);c1.metric('Vorgeschlagene Auffüllmenge',report['inventory']['suggested_units'])
 for n,step in enumerate(report['trace'],1):
  with st.expander(f'{n}. {step["Rolle"]} · {step["Werkzeug"]}',expanded=True):st.json(step['Ergebnis'])
 st.success(report['recommendation']);st.warning(report['status'])
 st.download_button('📥 Entscheidungsprotokoll',json.dumps(report,ensure_ascii=False,indent=2),'flight_agent_report.json','application/json')
 with st.expander('Optional: OpenAI oder Anthropic formuliert einen Ergebnisentwurf'):
  st.write('Der Klick sendet ausschließlich das angezeigte synthetische Laufprotokoll an den ausgewählten API-Anbieter und kann Kosten verursachen. Keine Kundendaten hochladen. Schlüssel nur als Codespace-Secret/Environment hinterlegen, niemals hier eingeben oder nach GitHub committen.')
  provider=st.selectbox('API-Anbieter',['OpenAI','Anthropic']);model=st.text_input('Modell-ID aus deinem API-Konto',placeholder='Aktuelle verfügbare Modell-ID')
  agree=st.checkbox('Dieses sichtbare Szenarioprotokoll an den gewählten Anbieter senden')
  if st.button('KI-Entwurf anfordern',disabled=not agree or not model):
   try:
    with st.spinner('Das Modell formuliert auf Grundlage des Protokolls …'):answer,usage=draft(provider,model,report)
    st.markdown(answer);st.json(usage);st.caption('KI-generierter Entwurf. Quellen und Rechnungen bleiben im Protokoll prüfbar. Keine Aktion wurde ausgelöst.')
   except Exception as e:st.error(type(e).__name__+': Anfrage fehlgeschlagen. Schlüssel, Modell-ID, API-Zugang und Serverprotokoll prüfen. Keine wiederholte automatische Anfrage.')
