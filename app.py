"""Flight: one guided commerce story with optional technical workspaces."""
from pathlib import Path
import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from flightlab.story import STEPS,contribution,incremental_contribution,teaching_experiment
from flightlab.ui import workspace_links,detail
from flightlab.organisation import inventory,retrieve

ROOT=Path(__file__).parent
st.set_page_config(page_title='Flight · Ein Einkauf, verständlich erklärt',page_icon='☕',layout='wide')
st.markdown('''<style>
.stApp{background:#0b1220;color:#e8edf6}[data-testid="stSidebar"]{background:#111e31}
h1,h2,h3{letter-spacing:-.025em}.stButton button{border-radius:10px}
[data-testid="stMetric"]{background:#142238;padding:14px;border-radius:12px}
</style>''',unsafe_allow_html=True)
CHAPTERS=[s[0] for s in STEPS]
if 'story_step' not in st.session_state:st.session_state.story_step=CHAPTERS[0]
def move(delta):
 index=CHAPTERS.index(st.session_state.story_step)
 st.session_state.story_step=CHAPTERS[max(0,min(len(CHAPTERS)-1,index+delta))]
with st.sidebar:
 st.markdown('## FLIGHT')
 st.caption('Annas Einkauf. Die Entscheidungen dahinter.')
 chapter=st.radio('Die Geschichte Schritt für Schritt',CHAPTERS,key='story_step')
 st.divider()
 with st.expander('Ich möchte ein Werkzeug ausprobieren'):
  workspace_links()
 st.caption('Portfolio von Amit Steinberg')
idx=CHAPTERS.index(chapter)
st.progress((idx+1)/len(CHAPTERS),text=f'Schritt {idx+1} von {len(CHAPTERS)}')
st.title(chapter.split(' · ',1)[1])
st.write(STEPS[idx][1])

if idx==0:
 image=ROOT/'assets/story_hero.jpg'
 if image.exists():st.image(str(image),width='stretch')
 st.subheader('Anna möchte eine kleine Kaffeemaschine kaufen.')
 st.write('Sie hat wenig Platz in der Küche und höchstens 150 € Budget. Der Shop möchte ihr helfen und dabei wirtschaftlich arbeiten. An diesem einen Einkauf erklären wir, wo Daten, maschinelles Lernen und Sprachmodelle nützlich sind.')
 st.write('**Du begleitest sechs Entscheidungen:**')
 st.dataframe(pd.DataFrame([
  ['Finden','Welches Produkt passt zu Annas Wunsch?'],
  ['Empfehlen','Was könnte als Nächstes sinnvoll sein?'],
  ['Rechnen','Wie viel bleibt nach den Kosten übrig?'],
  ['Rabatt entscheiden','Ändert der Gutschein den Kauf wirklich?'],
  ['Abstimmen','Kann der Shop sein Versprechen erfüllen?'],
  ['Prüfen','Hat die Änderung tatsächlich geholfen?'],
 ],columns=['Schritt','Die Frage']),hide_index=True,width='stretch')
 st.info('**So liest du die Geschichte:** Erst kommt ein konkretes Beispiel. Geschäftsbegriffe und Technik kannst du bei Bedarf aufklappen. Für den Einstieg brauchst du keine KI-Vorkenntnisse.')
 st.caption('Der Shop und seine Zahlen sind erfunden. Die Rechenwege funktionieren. Reale Datenexperimente sind separat dokumentiert.')
 st.write('☕ Anna möchte Kaffee. Sie muss dafür keinen Kurs in neuronalen Netzen belegen.')

elif idx==1:
 st.subheader('„Klein, schwarz und nicht teurer als 150 €.“')
 st.write('Die Aufgabe der Suche: Annas Beschreibung mit den Produktangaben abgleichen und ihr Budget einhalten.')
 query=st.text_input('Annas Wunsch','klein schwarz kaffee')
 budget=st.slider('Ihr Budget (€)',20,400,150,10)
 products=pd.DataFrame([
  ['Mokka Mini',89,'klein schwarz kaffee kompakt'],
  ['Barista Pro',349,'groß silber kaffee premium'],
  ['Reisebecher',25,'klein schwarz becher unterwegs'],
  ['Crema Refurbished',149,'schwarz kaffee gebraucht kompakt'],
 ],columns=['Produkt','Preis (€)','Produktwörter'])
 words=set(query.lower().split())
 products['Passende Wörter']=products['Produktwörter'].map(lambda s:len(words.intersection(s.split())))
 eligible=products[products['Preis (€)']<=budget].sort_values(['Passende Wörter','Preis (€)'],ascending=[False,True])
 st.dataframe(eligible[['Produkt','Preis (€)','Passende Wörter']],hide_index=True,width='stretch')
 if len(eligible) and eligible.iloc[0]['Passende Wörter']>0:
  st.success(f'Im Beispiel steht **{eligible.iloc[0]["Produkt"]}** oben: innerhalb des Budgets und mit passenden Produktwörtern.')
 else:st.info('Kein überzeugender Treffer. Dann sollte die Suche nachfragen oder ehrlich weniger Ergebnisse zeigen.')
 st.write('**Was wir gelernt haben:** Ein preislich unpassendes Produkt wird durch einen schönen Beschreibungstext nicht passend.')
 detail('Das Geschäftsziel heißt Produktauffindbarkeit: Kunden sollen mit ihrem Wunsch passende Artikel erreichen. Ob das mehr Käufe bewirkt, muss ein Experiment zeigen.',
        'Hier zählt ein einfacher Wortabgleich Treffer. Sentence Transformers können später sinngleiche Texte näher zusammenbringen. CLIP vergleicht Texte mit Bildern. Bildgenerierung erstellt dagegen ein neues Motiv. Diese Aufgaben sind verschieden.',
        'Regelbasierte Suche in einem fiktiven Minikatalog. Keine geladenen Sprach- oder Bildmodelle.')
 st.page_link('pages/2_Suchstudio.py',label='Vertiefen: Text- und Bildsuche ausprobieren')

elif idx==2:
 st.subheader('Anna schaut sich eine Maschine an. Was zeigen wir danach?')
 st.write('Suche reagiert auf eine Frage. Empfehlungen können auch dann helfen, wenn Anna keine neue Suchanfrage eingibt.')
 focus=st.selectbox('Annas letzter Produktkontakt',['Mokka Mini · Kaffeemaschine','Mahlzeit · Kaffeemühle','Bohnenliebe · Kaffeebohnen'])
 logic=st.radio('Welche Empfehlung möchten wir sehen?',['Was alle häufig kaufen','Was zum letzten Kontakt passt'],horizontal=True)
 neighbors={
  'Mokka Mini · Kaffeemaschine': [('Mahlzeit · Kaffeemühle','Ergänzt die Zubereitung mit frisch gemahlenen Bohnen.'),('Crema Refurbished','Eine andere Maschine zum Vergleichen.')],
  'Mahlzeit · Kaffeemühle':[('Bohnenliebe · Kaffeebohnen','Bohnen werden mit der Mühle verarbeitet.'),('Mokka Mini','Eine mögliche Ergänzung für die Zubereitung.')],
  'Bohnenliebe · Kaffeebohnen':[('Mahlzeit · Kaffeemühle','Zum Mahlen der Bohnen.'),('Reisebecher','Ein Zubehörartikel zum Kaffee unterwegs.')],
 }
 recommendations=[('Bohnenliebe · Kaffeebohnen','Im Beispiel der Bestseller.'),('Reisebecher','Im Beispiel ebenfalls häufig gekauft.')] if logic=='Was alle häufig kaufen' else neighbors[focus]
 st.dataframe(pd.DataFrame(recommendations,columns=['Vorschlag','Warum er hier steht']),hide_index=True,width='stretch')
 st.write('**Was wir gelernt haben:** Eine alternative Maschine hilft beim Vergleichen. Eine Mühle ergänzt den Einkauf. Das sind zwei unterschiedliche Aufgaben.')
 detail('Empfehlungen unterstützen Produktauswahl und ergänzende Käufe. Relevanz, Vielfalt und wirtschaftliche Wirkung sind getrennte Kennzahlen.',
        'BERT4Rec und SASRec lernen aus Artikelreihenfolgen. LightGCN lernt Beziehungen in einem Netz aus Kunden und Artikeln. Im Trainingslabor werden sie gegen einfache Verfahren verglichen. Das ersetzt keine Online-Wirkungsmessung.',
        'Manuell definierte Beispiele. Der Wechsel zeigt die Logik, keine gemessene Modellqualität.')
 st.write('☕ Ein zweiter Kaffee ist manchmal sinnvoll. Eine zweite Kaffeemaschine braucht eine bessere Begründung.')
 st.page_link('pages/1_Trainingslabor.py',label='Vertiefen: Empfehlungsverfahren trainieren und vergleichen')

elif idx==3:
 st.subheader('Eine Beispielbestellung bringt 100 € Umsatz.')
 st.write('Für diese separate Kostenrechnung nutzen wir eine runde Beispielbestellung von 100 €. Der **Deckungsbeitrag** ist der Betrag, der danach zur Deckung weiterer Kosten übrig bleibt.')
 discount=st.slider('Rabatt auf diese Bestellung (€)',0,30,0)
 with st.expander('Die angenommenen Kosten verändern'):
  goods=st.number_input('Wareneinsatz je Bestellung (€)',min_value=0.,value=50.)
  handling=st.number_input('Zahlung und Versand je Bestellung (€)',min_value=0.,value=6.)
  returns_cost=st.number_input('Erwartete Retourenkosten je Bestellung (€)',min_value=0.,value=8.)
  advertising=st.number_input('Zugerechnete Werbekosten je Bestellung (€)',min_value=0.,value=12.)
 margin=contribution(100.,goods,handling,returns_cost,advertising,discount)
 st.metric('Übrig nach diesen Kosten',f'{margin:.2f} €')
 components=[100.,-float(discount),-goods,-handling,-returns_cost,-advertising,0.]
 fig=go.Figure(go.Waterfall(x=['Umsatz','Rabatt','Ware','Versand/Zahlung','Retouren','Werbung','Übrig'],y=components,measure=['absolute']+['relative']*5+['total']))
 fig.update_layout(height=340,margin=dict(l=10,r=10,t=20,b=20),yaxis_title='€ je Beispielbestellung');st.plotly_chart(fig,width='stretch')
 st.write(f'**Die Entscheidung:** Mit {discount} € Rabatt bleiben unter diesen Annahmen {margin:.2f} € je Bestellung. Mehr Bestellungen allein beantworten noch nicht, ob der Rabatt sinnvoll ist.')
 detail('Hier ist der DB nach den aufgeführten variablen Kosten und Werbung definiert. Miete, Gehälter und andere Fixkosten sind noch nicht abgezogen.',
        'Deterministische Stückrechnung mit einer pauschalen erwarteten Retourenkostenposition. Die 100-€-Bestellung ist ein eigenes Rechenbeispiel und kein behaupteter Verkaufspreis der zuvor gezeigten Mokka Mini.',
        'Sichtbare Kostenannahmen, keine aus öffentlichen Klickdaten geschätzten Margen. Alle Beträge ohne Umsatzsteuer.')
 st.write('☕ Der CFO mag Umsatz. Er fragt nur gern, was davon noch da ist.')

elif idx==4:
 st.subheader('Wer braucht den Gutschein überhaupt?')
 st.write('Eine Kundin hätte vielleicht ohnehin gekauft. Bei einer anderen könnte das Angebot den Ausschlag geben. Wir vergleichen zwei erfundene Fälle mit bekannten Wahrscheinlichkeiten.')
 coupon=st.slider('Gutschein je Kauf (€)',0,20,10)
 rows=[]
 for name,p0,p1 in [('Fall A: kauft wahrscheinlich ohnehin',.60,.62),('Fall B: reagiert stärker auf das Angebot',.10,.25)]:
  rows.append({'Fall':name,'Kaufchance ohne Gutschein':f'{p0:.0%}','Kaufchance mit Gutschein':f'{p1:.0%}',
               'Zusätzlicher Beitrag je Kontakt (€)':round(incremental_contribution(p0,p1,coupon),2)})
 st.dataframe(pd.DataFrame(rows),hide_index=True,width='stretch')
 st.caption('Annahme: 40 € Beitrag je Kauf vor Gutschein, 0,20 € Kontaktkosten. Den Gutschein erhalten auch diejenigen, die ohnehin gekauft hätten.')
 st.write('**Die Entscheidung:** Unter diesen Annahmen lohnt sich der Kontakt nur bei einem positiven zusätzlichen Beitrag. Eine hohe Kaufchance allein reicht nicht.')
 detail('Die zusätzliche Wirkung einer Maßnahme heißt Uplift. Für den Business Case zählen zusätzliche Käufe abzüglich aller Gutschein- und Kontaktkosten.',
        'Formel: (p_mit − p_ohne) × 40 € − p_mit × Gutschein − 0,20 €. In echten Daten ist der individuelle Gegenfall unsichtbar. Randomisierte Treatment-/Kontrollgruppen helfen beim Schätzen. Der separate Criteo-Benchmark untersucht Werbung, keine gemessenen Gutschein-Effekte dieses Shops.',
        'Lehrsimulation mit bekannten Wahrscheinlichkeiten, kein trainiertes Uplift-Modell.')
 st.write('☕ Ein Gutschein an den ohnehin sicheren Käufer ist eine besonders teure Form der Höflichkeit.')
 st.page_link('pages/3_Marketinglabor.py',label='Vertiefen: Zusätzliche Werbewirkung auf geeigneten Daten untersuchen')

elif idx==5:
 st.subheader('Anna fragt: „Ist die Maschine bis Freitag da?“')
 st.write('Jetzt müssen Einkauf, Finanzen und Service zusammenarbeiten. Eine freundliche Antwort genügt nicht, wenn der Liefertermin ungeklärt ist.')
 stock=st.slider('Verfügbarer Bestand (Stück)',0,500,180,10)
 daily=40;lead=7;needed=daily*lead;calculation=inventory(daily,12,lead,stock)
 st.dataframe(pd.DataFrame([
  ['Einkauf',f'{stock} Stück auf Lager; {needed} Stück erwarteter Bedarf in sieben Tagen.'],
  ['Finanzen','Die Beispielbestellung lässt vor einem Rabatt 24 € Beitrag übrig.'],
  ['Kundenservice','Die Handbuchregel verlangt einen bestätigten Termin vor einem Lieferversprechen.'],
 ],columns=['Wer liefert die Information?','Was wissen wir?']),hide_index=True,width='stretch')
 if stock<needed:st.warning(f'Beim angenommenen Bedarf fehlen {needed-stock} Stück für die sieben Tage. Der Einkauf sollte den Bestand prüfen.')
 else:st.success('Der Bestand deckt den angenommenen Bedarf während der Lieferzeit. Ein bestätigter individueller Liefertermin fehlt weiterhin.')
 st.write('**Antwortentwurf für Anna:** „Die Maschine passt zu deinen Angaben. Den konkreten Liefertermin prüfen wir noch und bestätigen ihn dir anschließend.“')
 st.caption('Vorlagenentwurf aus dem Beispiel, kein Live-Modellaufruf und keine versendete Nachricht.')
 detail('Ein Copilot bereitet Informationen für einen Menschen auf. Ein Agent kann Werkzeuge über mehrere Schritte einsetzen. Ein fester Workflow führt vorgegebene Schritte aus. Flight demonstriert derzeit diesen festen Ablauf.',
        'Das Bestandswerkzeug berechnet zusätzlich einen Sicherheitsbestand. Die Wissenssuche findet Handbuchstellen. OpenAI- und Anthropic-APIs können optional den Textentwurf formulieren. Sie wählen hier keine Tools autonom; ihre Live-Anbindung braucht eigene Schlüssel.',
        'Lokale Rechnung und synthetisches Handbuch. Kein ERP-, Versand- oder Kundensystem verbunden.')
 with st.expander('Wo ChatGPT und Claude hineinpassen'):
  st.write('Ein Sprachmodell kann aus geprüften Fakten eine verständliche Antwort machen. Die Rechnung bleibt beim Rechenwerkzeug, der bestätigte Liefertermin muss aus einem zuständigen System kommen. Wir vergleichen Anbieter anhand eigener Aufgaben statt anhand eines pauschalen Markenrankings.')
  st.write('Flight besitzt optionale OpenAI- und Anthropic-API-Adapter. ChatGPT und Claude sind außerdem eigenständige Chatprodukte. Gemini und lokale Modelle sind hier nur beschriebene Alternativen.')
 st.page_link('pages/7_Agenten_Kommandozentrale.py',label='Vertiefen: Den gemeinsamen Arbeitsauftrag ausführen')
 st.page_link('pages/6_KI_im_Unternehmen.py',label='Weitere Anwendungen in anderen Abteilungen ansehen')

elif idx==6:
 st.subheader('Ist die neue Shopversion wirklich besser?')
 st.write('Das klingt besser. Aber ein kleiner Unterschied kann durch Zufall entstehen. Ein echter A/B-Test würde Personen zufällig auf die Varianten verteilen. Im folgenden Lehrbeispiel zeigen wir erfundene Zahlen für gleich große Gruppen.')
 n=st.select_slider('Personen je Gruppe',options=[1000,10000,50000],value=1000)
 result=teaching_experiment(n)
 st.dataframe(pd.DataFrame([
  ['Bisherige Version',result['control'],n,f'{result["control"]/n:.1%}'],
  ['Neue Version',result['variant'],n,f'{result["variant"]/n:.1%}'],
 ],columns=['Gruppe','Käufe','Personen','Kaufrate']),hide_index=True,width='stretch')
 st.write(f'Der Unterschied beträgt **{result["difference_pp"]:.2f} Prozentpunkte**. Das ungefähre 95-%-Intervall reicht von **{result["low_pp"]:.2f} bis {result["high_pp"]:.2f} Prozentpunkten**.')
 if result['low_pp']<=0:st.info('**Die Entscheidung:** Die Daten dieses Beispiels belegen noch keinen positiven Effekt. Wir brauchen mehr Information statt einer Siegesmeldung.')
 else:st.success('**Die Entscheidung:** Das Intervall liegt über null. Jetzt müssen wir zusätzlich Beitrag, Kosten und praktische Relevanz prüfen.')
 st.caption('Erfundene, gerundete Ereigniszahlen mit festgelegten Kaufraten; keine erhobene Studie und keine simulierte Zufallsstichprobe. Die Gruppengröße verändert die berechnete Unsicherheit.')
 detail('Ein A/B-Test vergleicht zufällig zugeteilte Varianten. Neben der Kaufrate sind Deckungsbeitrag, Retouren und Servicefolgen zu beachten.',
        'Gezeigt ist die approximative Wald-Unsicherheit einer Differenz zweier unabhängiger Anteile. Reale Experimente brauchen vorab definierte Zielmetriken, ausreichende Stichproben und passende Auswertungsverfahren. Beobachtungsdaten benötigen andere Annahmen; das Ökonometrie-Labor ist eine separate Vertiefung.',
        'Ein Rechenbeispiel zur Unsicherheit. Keine Behauptung einer Verbesserung durch Flight.')
 st.write('☕ Vier zusätzliche Käufe sind ein Anlass zum Nachrechnen. Die Konfettikanone kann noch warten.')
 st.page_link('pages/4_Suche_und_Oekonometrie.py',label='Vertiefen: Suchqualität und Kampagnenwirkung prüfen')

else:
 st.subheader('Die Geschichte verbindet einen Einkauf mit sechs Entscheidungen.')
 st.write('Du hast gesehen, wie Suche und Empfehlungen helfen können, warum Kosten und zusätzliche Wirkung zählen und weshalb das Team verlässliche Informationen braucht.')
 st.dataframe(pd.DataFrame([
  ['In der Geschichte','Fiktive Daten und einfache Rechenbeispiele.'],
  ['In den Laboren','Ausführbare Suche, Training, Marketing- und Ökonometrie-Werkzeuge.'],
  ['Bei den Sprachmodellen','Optionale API-Textentwürfe; ohne Schlüssel nicht live getestet.'],
  ['Bei den bisherigen Messungen','Noch kein belastbarer Qualitätsgewinn oder Geschäftseffekt nachgewiesen.'],
 ],columns=['Bereich','Was du daraus ableiten darfst']),hide_index=True,width='stretch')
 st.write('**Warum das ein Portfolio ist:** Es zeigt, wie ich eine Geschäftsfrage in Datenarbeit, Software und überprüfbare Entscheidungen übersetze. Der nächste Produktionsschritt wäre ein begrenzter, gemessener Pilot.')
 with st.expander('Welche öffentlichen Daten beantworten welche Frage?'):
  st.dataframe(pd.DataFrame([
   ['Retailrocket / REES46','Welche Artikel werden nacheinander angesehen oder gekauft?'],
   ['Amazon-M2','Welcher Artikel folgt in einer Einkaufssitzung?'],
   ['Amazon Reviews 2023','Was lässt sich aus Rezensionen und Produktinformationen lernen?'],
   ['Amazon ESCI','Welches Produkt passt zu einer Suchanfrage?'],
   ['Criteo Uplift','Wie unterscheidet sich Werbung von keiner Werbung?'],
  ],columns=['Quelle','Ihre eigene Aufgabe']),hide_index=True,width='stretch')
  st.write('Die Quellen bleiben getrennt. Sie beschreiben keinen gemeinsamen Kunden und liefern keine echten Margen oder Lagerbestände dieses Beispielshops.')
 st.page_link('pages/5_Praesentation.py',label='Die Folien und die bisherigen Nachweise ansehen')
 st.page_link('pages/9_KI_Business_Case.py',label='Den wirtschaftlichen Nutzen eines KI-Piloten durchrechnen')
 with st.expander('Alle vertiefenden Werkzeuge'):
  workspace_links()

st.divider()
left,right=st.columns(2)
with left:st.button('← Vorheriger Schritt',disabled=idx==0,on_click=move,args=(-1,),width='stretch')
with right:st.button('Nächster Schritt →',disabled=idx==len(CHAPTERS)-1,on_click=move,args=(1,),width='stretch',type='primary')
st.caption('FLIGHT · Amit Steinberg · Fiktiver Shop, sichtbare Annahmen, getrennte Projektnachweise.')
