from flightlab.ui import lab_header
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(page_title='Flight · KI Business Case',layout='wide',page_icon='💶')
lab_header('Lohnt sich der KI-Pilot wirtschaftlich?', 'Berechne ein Szenario aus Arbeitszeit, Prüfaufwand, tatsächlicher Nutzung und Kosten. Die Eingaben sind Annahmen, keine gemessenen Einsparungen.', 'Einen monatlichen Nettonutzen unter deinen Annahmen und die einfache Amortisationsdauer.', 'Schritt 8 · Den nächsten Pilot planen')
a,b=st.columns(2)
with a:
 tasks=st.slider('Vorgänge pro Monat',100,100000,10000,100)
 saved=st.slider('Brutto gesparte Minuten je Vorgang',0.,30.,4.,.5)
 reviewed=st.slider('Menschliche Prüfminuten je Vorgang',0.,20.,1.,.5)
 adoption=st.slider('Tatsächlich genutzter Anteil (%)',0,100,60)/100
 hourly=st.slider('Vollkosten je Arbeitsstunde (€)',10,150,45)
 realization=st.slider('Als wirtschaftlicher Nutzen realisierter Anteil (%)',0,100,40)/100
with b:
 calls=st.slider('Modellaufrufe je bearbeitetem Vorgang',1,10,2)
 input_tokens=st.number_input('Inputtokens je Aufruf',min_value=0,max_value=1000000,value=3000)
 output_tokens=st.number_input('Outputtokens je Aufruf',min_value=0,max_value=100000,value=600)
 pin=st.number_input('Angenommene Kosten je 1 Mio. Inputtokens (€)',min_value=0.,value=2.)
 pout=st.number_input('Angenommene Kosten je 1 Mio. Outputtokens (€)',min_value=0.,value=10.)
 fixed=st.number_input('Betrieb und Betreuung pro Monat (€)',min_value=0.,value=1500.)
 build=st.number_input('Einmalige Implementierung (€)',min_value=0.,value=12000.)
monthly=tasks*adoption;hours=monthly*(saved-reviewed)/60;capacity=hours*hourly;benefit=capacity*realization
api=monthly*calls*(input_tokens*pin+output_tokens*pout)/1e6;net=benefit-api-fixed
x,y,z=st.columns(3);x.metric('Freigesetzte Kapazität',f'{hours:,.0f} h/Monat');y.metric('Nutzen nach Realisierungsannahme',f'{benefit:,.0f} €/Monat');z.metric('Netto nach laufenden Kosten',f'{net:,.0f} €/Monat')
st.caption('Szenarioannahmen, keine aktuellen Anbieterpreise und keine gemessenen Einsparungen. Zeitgewinn wird nicht automatisch zu Budgeteinsparung. Prüfzeit kann den Bruttogewinn übersteigen.')
st.write('**Einfache Amortisationsdauer:** '+(f'{build/net:.1f} Monate' if net>0 else 'Unter diesen Annahmen nicht erreichbar.'))
rows=[]
for share in np.linspace(.1,1,10):
 n=tasks*share;value=n*(saved-reviewed)/60*hourly*realization-n*calls*(input_tokens*pin+output_tokens*pout)/1e6-fixed
 rows.append({'Nutzungsquote':share,'Nettonutzen pro Monat (€)':value})
st.plotly_chart(px.line(pd.DataFrame(rows),x='Nutzungsquote',y='Nettonutzen pro Monat (€)',markers=True),width='stretch')
st.subheader('Pilotplan mit überprüfbarem Nutzen')
st.write('**Woche 1:** Ausgangslage und Fehler erfassen. **Woche 2:** Begrenzte Aufgabe mit Quellen und lokalen Tools testen. **Woche 3:** Gegenprobe mit Kontrollgruppe oder geeignetem Vergleich. **Woche 4:** Gesamtkosten, Qualität und Akzeptanz prüfen. Eine Ausweitung folgt der Evidenz.')
st.info('Der beste Agent kann eine unnötige Aufgabe sehr schnell erledigen. Prozessverbesserung zuerst mitdenken.')
