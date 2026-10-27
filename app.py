"""Commerce Flight Deck: German interactive commerce decision laboratory."""
from pathlib import Path
import io
import json
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Flight · Kaufrausch & Kassensturz', page_icon='✈️', layout='wide')
st.markdown('''<style>
.stApp {background:#0b1220;color:#e8edf6} h1,h2,h3 {letter-spacing:-.035em}
[data-testid="stSidebar"] {background:#111e31} .hero {padding:32px;border:1px solid #294463;border-radius:22px;background:linear-gradient(120deg,#132c46,#152034);margin-bottom:22px}
.eyebrow {color:#56ddc0;letter-spacing:.15em;font-size:12px;font-weight:700}.hero h1 {font-size:42px;margin:8px 0}.hero p {max-width:850px;color:#c1d0e1;font-size:18px}
[data-testid="stMetric"] {background:#142238;border:1px solid #263d56;padding:16px;border-radius:14px}
.stButton button {border-radius:10px} footer {visibility:hidden}
</style>''', unsafe_allow_html=True)

CHAPTERS=['01 · Der Gewinn ist verschwunden','02 · Annas Einkaufsreise','03 · Finden statt verzweifeln','04 · Der geheime Produktclub','05 · Rabatt oder Ruhe?','06 · Der CFO übernimmt','07 · Beweise statt Bauchgefühl','08 · Daten & Maschinenraum']
PRODUCTS=pd.DataFrame([
 ['Mokka Mini','Kaffeemaschine',89,43,'kompakt klein günstig schwarz kaffee küche', '☕'],
 ['Barista Pro','Kaffeemaschine',349,145,'premium espresso silber groß milch barista', '☕'],
 ['Crema Refurbished','Kaffeemaschine',149,71,'refurbished nachhaltig espresso günstig schwarz', '♻️'],
 ['Mahlzeit Mühle','Mühle',59,26,'kaffee bohnen mahlen kompakt schwarz mühle', '⚙️'],
 ['Bohnenliebe','Bohnen',19,8,'kaffee bohnen espresso aroma bio', '🫘'],
 ['Milchwolke','Zubehör',39,15,'milch schaum cappuccino weiß zubehör', '🥛'],
 ['Filterfreund','Zubehör',12,4,'filter papier kaffee günstig klein', '📦'],
 ['Reisebecher','Zubehör',25,11,'becher unterwegs klein schwarz nachhaltig', '🥤'],
],columns=['Produkt','Kategorie','Preis','Wareneinsatz','Text','Symbol'])

def chart(fig):
 fig.update_layout(template='plotly_dark',paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font_family='sans-serif',margin=dict(l=15,r=15,t=35,b=20))
 st.plotly_chart(fig,width='stretch')

def explain(simple,business,tech,joke):
 plain_tab,business_tab,technical_tab=st.tabs(['🧑 Einfach erklärt','💼 Geschäftlich','🔬 Technisch'])
 with plain_tab:
  st.write(simple)
 with business_tab:
  st.write(business)
 with technical_tab:
  st.write(tech)
 st.info('☕ Kaffeepause: '+joke)

def cards(frame):
 cols=st.columns(min(3,len(frame)))
 for n,(_,r) in enumerate(frame.iterrows()):
  with cols[n%len(cols)]:
   with st.container(border=True):
    st.subheader(f"{r.Symbol} {r.Produkt}")
    st.write(r.Kategorie);st.metric('Preis',f'{r.Preis:.0f} €')
    if 'Score' in r: st.caption(f'Demo-Relevanz: {r.Score:.2f}')

with st.sidebar:
 st.markdown('## ✈️ FLIGHT')
 st.caption('DAS E-COMMERCE ENTSCHEIDUNGSLABOR')
 chapter=st.radio('Deine Mission',CHAPTERS)
 st.divider()
 st.write('**Kaufrausch & Kassensturz**')
 st.caption('Ein fiktiver Shop. Echte Rechenwege. Keine erfundenen Forschungserfolge.')
 st.warning('DEMO · synthetische Szenarien')
 st.caption('Entwickelt als Portfolio von Amit Steinberg')

idx=CHAPTERS.index(chapter)
if idx==0 and (Path(__file__).parent/'assets/flight_poster.jpg').exists():
 st.image(str(Path(__file__).parent/'assets/flight_poster.jpg'),width='stretch')
st.caption('Weitere Arbeitsbereiche in der Seitennavigation: Trainingslabor · Suchstudio · Marketinglabor · Evidenzstudio. Neu: KI im Unternehmen · Agenten-Kommandozentrale · Wissen & Content · KI-Business-Case. Die folgenden Story-Kapitel bleiben nachvollziehbare Simulationen.')
st.progress((idx+1)/len(CHAPTERS),text=f'Kapitel {idx+1} von 8 · Vom Klick zum belastbaren Geschäftsmodell')
st.markdown('<div class="hero"><div class="eyebrow">COMMERCE FLIGHT DECK / KAUFRAUSCH & KASSENSTURZ</div><h1>'+chapter.split(' · ')[1]+'</h1><p>Anna sucht Kaffee. Das Marketing sucht Wachstum. Der CFO sucht sein Geld. Du bringst die drei zusammen.</p></div>',unsafe_allow_html=True)

if idx==0:
 st.write('### Montag, 09:00 Uhr. Die Bestellungen steigen. Die Stimmung beim CFO sinkt.')
 st.write('Deine Aufgabe: Erkläre, warum Umsatz kein Synonym für Gewinn ist. Verändere die Annahmen und rette den Deckungsbeitrag – bevor jemand „mehr Budget“ ruft.')
 l,r=st.columns([1,2])
 with l:
  orders=st.slider('Bestellungen',100,10000,2000,100)
  basket=st.slider('Warenkorb netto (€)',20,300,100)
  discount=st.slider('Durchschnittlicher Rabatt (%)',0,40,10)
  returns=st.slider('Retourenquote (%)',0,50,15)
  acquisition=st.slider('Werbekosten je Bestellung (€)',0,70,18)
  goods=st.slider('Wareneinsatz (% des Listenwerts)',10,85,48)
 net=orders*basket*(1-discount/100)*(1-returns/100)
 cogs=orders*basket*goods/100*(1-returns/100)
 fulfil=orders*6+orders*returns/100*8
 ads=orders*acquisition
 contribution=net-cogs-fulfil-ads
 with r:
  a,b,c=st.columns(3);a.metric('Nettoerlös nach Retouren',f'{net:,.0f} €');b.metric('DB nach variablen Kosten',f'{net-cogs-fulfil:,.0f} €');c.metric('DB nach Marketing',f'{contribution:,.0f} €')
  chart(go.Figure(go.Waterfall(x=['Nettoerlös','Ware','Versand & Retouren','Werbung','DB nach Marketing'],y=[net,-cogs,-fulfil,-ads,0],measure=['absolute','relative','relative','relative','total'],increasing_marker_color='#56ddc0',decreasing_marker_color='#ff8b84',totals_marker_color='#8baaff')))
  st.success('Der CFO atmet wieder. Noch keine Gehaltserhöhung, aber immerhin Sauerstoff.') if contribution>0 else st.error('Jede zusätzliche Bestellung braucht zuerst eine bessere Stückökonomie. Der Paketbote ist begeistert. Der CFO weniger.')
 st.caption('Szenario: Nettopreise ohne Umsatzsteuer. Rücksendungen vollständig erstattet, Ware wiederverkaufbar. 6 € variable Abwicklung je Bestellung, zusätzlich 8 € je Retoure. Fixkosten fehlen; DB ist kein Unternehmensgewinn.')
 explain('Umsatz ist das Geld, das hereinkommt. Der Deckungsbeitrag ist das, was nach bestimmten Kosten übrig bleibt.','Wir verbinden Retouren, Rabattintensität und Customer Acquisition Cost mit der Stückökonomie. Die DB-Stufen sind für diese Demo ausdrücklich definiert.','Deterministische Szenarioanalyse, keine trainierte Prognose. Sensitivitäten entstehen aus veränderten Eingaben; kausale Effekte werden nicht geschätzt.','Umsatz bezahlt keine Miete. Außer dein Vermieter akzeptiert PowerPoint.')

elif idx==1:
 st.write('### Anna hat keinen festen Kundentyp. Anna hat einen Dienstag.')
 st.write('Sie startet bei einer kleinen Kaffeemaschine, schaut kurz ins Premiumregal und entdeckt dann ihr Budget wieder. Baue ihre Reise Schritt für Schritt.')
 if 'journey' not in st.session_state: st.session_state.journey=[0]
 chosen=st.selectbox('Nächster Produktkontakt',PRODUCTS.Produkt)
 a,b=st.columns(2)
 if a.button('➕ Anna schaut sich das an',width='stretch'):st.session_state.journey.append(int(PRODUCTS.index[PRODUCTS.Produkt==chosen][0]))
 if b.button('↺ Reise zurücksetzen',width='stretch'):st.session_state.journey=[0]
 seq=st.session_state.journey[-15:]
 st.write(' → '.join(PRODUCTS.iloc[i].Symbol+' '+PRODUCTS.iloc[i].Produkt for i in seq))
 model=st.radio('Welche Logik übernimmt?', ['Bestseller','Gesamte Reise','Letzter Kontakt zählt'],horizontal=True)
 scores=np.array([8.,6.,5.,4.,7.,3.,4.,5.])
 if model!='Bestseller':
  scores=np.zeros(len(PRODUCTS))
  for t,i in enumerate(seq):
   weight=1 if model=='Gesamte Reise' else .5**(len(seq)-t-1)
   scores+=weight*(PRODUCTS.Kategorie==PRODUCTS.iloc[i].Kategorie).to_numpy()*3
   if PRODUCTS.iloc[i].Kategorie=='Kaffeemaschine':scores+=weight*np.array([0,0,0,2,1.5,1,0.5,.2])
  scores+=np.linspace(.1,.8,len(scores))
 scores[list(set(seq))]=-1
 result=PRODUCTS.assign(Score=scores).sort_values('Score',ascending=False).head(3);cards(result)
 st.caption('Ausgeführt: nachvollziehbare regelbasierte Demo. BERT4Rec und SASRec sind hier Erklärthemen, keine heimlich trainierten Modelle.')
 explain('Die Reihenfolge deiner Besuche kann zeigen, was dich gerade interessiert. Ein Bestseller kennt nur die Menge. Ein Sequenzmodell kennt die Geschichte.','Session Recommendation reagiert auf aktuelle Kaufabsicht. Benchmarks müssen gegen einfache Kandidaten antreten und kalte Sitzungen separat betrachten.','BERT4Rec rekonstruiert maskierte Artikel mit bidirektionaler Self-Attention; SASRec modelliert Sequenzen kausal. Hier laufen Bestseller-, Kategorie- und Aktualitätsheuristiken.','Wer einmal einen Toaster anklickt, sollte nicht bis zur Rente als Brotbeauftragter geführt werden.')

elif idx==2:
 st.write('### „So eine kleine schwarze Maschine. Du weißt schon.“')
 query=st.text_input('Beschreibe dein Wunschprodukt','kompakt schwarz kaffee')
 budget=st.slider('Maximales Budget (€)',10,400,150)
 tokens=set(query.lower().split())
 frame=PRODUCTS[PRODUCTS.Preis<=budget].copy()
 frame['Score']=frame.Text.map(lambda text:len(tokens.intersection(text.split()))/max(1,len(tokens)))
 if len(frame):cards(frame.sort_values(['Score','Preis'],ascending=[False,True]).head(3))
 else:st.info('Kein Produkt innerhalb dieses Budgets. Selbst die KI kann keine Kaffeemaschine für Luft und Liebe liefern.')
 st.caption('Aktiv: Wortüberschneidung und harter Preisfilter. Semantische Suche benötigt separat installierte Modelle; hier wird keine Embedding-Qualität behauptet.')
 with st.expander('🖼️ Bildsuche & Text-Bild-Verständnis: Was gehört in die nächste Ausbaustufe?'):
  st.write('Sentence Transformers: Text → Vektor. CLIP/SigLIP: Text und Bilder → vergleichbare Vektoren. Ein Diffusionsmodell: Text → neues Bild. Drei Werkzeuge, drei verschiedene Aufgaben.')
  upload=st.file_uploader('Optionales Referenzbild zur lokalen Vorschau; noch keine Ähnlichkeitssuche',type=['png','jpg','jpeg'])
  if upload:st.image(upload,caption='Nur Vorschau – kein Bildmodell aktiv.',width=250)
 explain('Beschreibe einen Wunsch, statt den exakten Produktnamen zu erraten. Später können auch Bilder als Suchanfrage dienen.','Semantic Search, multimodale Discovery und harte Preis-/Verfügbarkeitsfilter ergänzen klassische Suche.','Diese Demo nutzt Lexical Matching. Produktionspfad: Sentence Transformers und CLIP/SigLIP, normalisierte Embeddings, ANN-Retrieval und anschließendes Reranking.','Eine Suchmaschine sollte dich verstehen. Du bist schließlich Kunde und kein SQL-Statement.')

elif idx==3:
 st.write('### Der geheime Produktclub – wer hängt mit wem zusammen?')
 st.write('Wähle ein Produkt und erkunde sein Nachbarschaftsnetz. In dieser Demo sind Beziehungen redaktionell definiert, nicht aus Kaufdaten gelernt.')
 edges=[(0,3,'Ergänzung'),(0,6,'Ergänzung'),(1,3,'Ergänzung'),(1,5,'Ergänzung'),(2,3,'Ergänzung'),(3,4,'Ergänzung'),(4,7,'Ergänzung'),(0,2,'Alternative'),(1,2,'Alternative')]
 focus=st.selectbox('Produkt im Mittelpunkt',PRODUCTS.Produkt)
 focus_i=int(PRODUCTS.index[PRODUCTS.Produkt==focus][0]); kind=st.radio('Beziehungen',['Alle','Ergänzung','Alternative'],horizontal=True)
 active=[e for e in edges if kind=='Alle' or e[2]==kind]
 angles=np.arange(8)*2*np.pi/8;xx=np.cos(angles);yy=np.sin(angles);fig=go.Figure()
 for a,b,k in active:fig.add_trace(go.Scatter(x=[xx[a],xx[b]],y=[yy[a],yy[b]],mode='lines',line=dict(color='#56ddc0' if k=='Ergänzung' else '#8baaff',width=3 if focus_i in (a,b) else 1),hoverinfo='text',text=k,showlegend=False))
 fig.add_trace(go.Scatter(x=xx,y=yy,mode='markers+text',text=PRODUCTS.Produkt,textposition='top center',marker=dict(size=[30 if i==focus_i else 18 for i in range(8)],color='#56ddc0'),showlegend=False))
 fig.update_xaxes(visible=False);fig.update_yaxes(visible=False);chart(fig)
 st.write('**Direkte Verbindungen:** '+', '.join(PRODUCTS.iloc[b if a==focus_i else a].Produkt+' ('+k+')' for a,b,k in active if focus_i in (a,b)))
 explain('Ein Graph ist ein Beziehungsnetz: Produkte, Menschen und Kategorien werden zu Punkten und Verbindungen.','Cross-Selling und Substitution brauchen unterschiedliche Logik. Gemeinsam angesehen bedeutet nicht automatisch gemeinsam benötigt.','LightGCN propagiert Embeddings über einen User-Item-Graphen. Eine GNN kann zusätzliche Knoten-/Kantentypen verarbeiten. Gezeigt wird ausschließlich ein statischer Beispielgraph.','Kaffeemaschine und Mühle: gutes Paar. Zwei Kaffeemaschinen: möglicherweise eine Ehekrise.')

elif idx==4:
 st.write('### Gibst du Anna einen Rabatt – oder nur Geld zurück, das sie ohnehin bezahlt hätte?')
 st.write('Wir kennen in dieser künstlichen Welt beide Kaufwahrscheinlichkeiten. Im echten Leben sehen wir pro Person nur eine der beiden Welten.')
 budget=st.slider('Maximal kontaktierte Kunden',0,1000,300,50)
 coupon=st.slider('Rabatt je behandeltem Kauf (€)',0,30,10)
 cost=st.slider('Kontaktkosten je Kunde (€)',0.,3.,.5,.1)
 rng=np.random.default_rng(42);n=1000;p0=rng.uniform(.02,.7,n);effect=.20*np.sin(np.arange(n)*.07)-.04;p1=np.clip(p0+effect,0,1)
 df=pd.DataFrame({'Kaufchance ohne Aktion':p0,'Kaufchance mit Aktion':p1});df['Uplift']=p1-p0
 df['Inkrementeller DB']=(p1-p0)*40-p1*coupon-cost
 strategy=st.selectbox('Wen kontaktieren?',['Höchster inkrementeller DB','Höchster Uplift','Höchste Kaufwahrscheinlichkeit','Zufällig'])
 order={'Höchster inkrementeller DB':np.argsort(-df['Inkrementeller DB'].values),'Höchster Uplift':np.argsort(-(p1-p0)),'Höchste Kaufwahrscheinlichkeit':np.argsort(-p0),'Zufällig':rng.permutation(n)}[strategy]
 selected=order[:budget]
 if strategy=='Höchster inkrementeller DB':selected=selected[df.iloc[selected]['Inkrementeller DB'].values>0]
 df['Auswahl']='Nicht kontaktieren';df.loc[selected,'Auswahl']='Kontaktieren'
 a,b,c=st.columns(3);a.metric('Kontakte',len(selected));b.metric('Erwartete Zusatzkäufe',f'{(p1[selected]-p0[selected]).sum():.1f}');c.metric('Erwarteter zusätzlicher DB',f'{df.iloc[selected]["Inkrementeller DB"].sum():,.0f} €')
 chart(px.scatter(df,x='Kaufchance ohne Aktion',y='Uplift',color='Auswahl',color_discrete_sequence=['#576d89','#56ddc0']))
 st.caption('Oracle-Simulation, kein geschätztes Uplift-Modell: bekannte potenzielle Kaufwahrscheinlichkeiten; 40 € Beitrag je Kauf vor Rabatt. Kontaktlimit ist kein Eurobudget. Die DB-Politik lässt schädliche Kontakte aus.')
 explain('Eine hohe Kaufchance sagt nicht, dass Werbung hilft. Entscheidend ist der Unterschied zwischen „mit Aktion“ und „ohne Aktion“.','Uplift-Targeting berücksichtigt Mitnahmeeffekte. Inkrementeller DB zieht Rabatte auch bei ohnehin stattfindenden Käufen ab.','Für reale Schätzung: randomisierte Treatment-/Kontrolldaten, Cross-Fitting, T-/X-/DR-Learner und Policy Evaluation. Diese Daten sind in den bisherigen Shopdatensätzen nicht automatisch enthalten.','Dem sicheren Käufer einen Gutschein geben ist wie dem Regen eine Gießkanne anbieten.')

elif idx==5:
 st.write('### „Sehr relevant“ ist schön. „Wir können die Rechnung bezahlen“ auch.')
 objective=st.radio('Was soll die Rangfolge optimieren?',['Kaufwahrscheinlichkeit','Erwarteter Umsatz','Erwarteter Deckungsbeitrag'],horizontal=True)
 ship=st.slider('Variable Abwicklung je Kauf (€)',0,20,6)
 return_rate=st.slider('Angenommene Retourenquote (%)',0,50,10)
 d=PRODUCTS.copy();d['Kaufwahrscheinlichkeit']=[.18,.035,.11,.14,.25,.13,.30,.17]
 d['Beitrag je Kauf']=(d.Preis-d.Wareneinsatz)*(1-return_rate/100)-ship-return_rate/100*8
 d['Erwarteter Umsatz']=d.Kaufwahrscheinlichkeit*d.Preis*(1-return_rate/100)
 d['Erwarteter Deckungsbeitrag']=d.Kaufwahrscheinlichkeit*d['Beitrag je Kauf']
 ranked=d.sort_values(objective,ascending=False)
 chart(px.bar(ranked,x='Produkt',y=objective,color='Kategorie'))
 st.dataframe(ranked[['Produkt','Preis','Kaufwahrscheinlichkeit','Beitrag je Kauf','Erwarteter Deckungsbeitrag']],hide_index=True,width='stretch')
 if ranked.iloc[0][objective]<=0:st.warning('Auch Nicht-Anbieten ist eine Entscheidung: Alle Kandidaten haben keinen positiven Zielwert.')
 st.download_button('📥 Entscheidung als CSV',ranked.to_csv(index=False).encode('utf-8-sig'),'flight_entscheidung.csv','text/csv')
 explain('Das meistgekaufte Produkt lässt nicht unbedingt das meiste Geld übrig. Wir vergleichen die Ziele.','Expected Contribution verbindet Kaufwahrscheinlichkeit und variable Marge. Retourenkosten verändern die Rangfolge. Werbekosten sind hier nicht enthalten.','Fixe synthetische Wahrscheinlichkeiten, keine kausale Wirkungsprognose. Ein Produktionsranker benötigt kalibrierte Scores und kontrollierte Evaluation.','Der CFO hat den Transformer gesehen und gefragt, ob der auch die Versandkosten transformiert.')

elif idx==6:
 st.write('### Die Kampagne läuft. Ist das Wachstum wirklich unser Verdienst?')
 lift=st.slider('Simulierter zusätzlicher Kampagneneffekt (Prozentpunkte)',-5.,10.,3.,.5)
 trend=st.slider('Allgemeiner Markttrend (Prozentpunkte)',-5.,10.,4.,.5)
 base=.12;control_after=base+trend/100;treated_after=control_after+lift/100
 frame=pd.DataFrame({'Gruppe':['Kontrolle','Kontrolle','Kampagne','Kampagne'],'Zeit':['Vorher','Nachher']*2,'Kaufrate':[base,control_after,base,treated_after]})
 chart(px.line(frame,x='Zeit',y='Kaufrate',color='Gruppe',markers=True,color_discrete_sequence=['#8baaff','#56ddc0']))
 a,b=st.columns(2);a.metric('Naiv: Veränderung Kampagnengruppe',f'{trend+lift:+.1f} Prozentpunkte');b.metric('Difference-in-Differences',f'{lift:+.1f} Prozentpunkte')
 st.caption('Reines Lehrbeispiel ohne Stichprobenrauschen. Gleiche Ausgangswerte und parallele unbehandelte Trends sind konstruiert, nicht empirisch nachgewiesen.')
 st.write('#### Experiment planen: Wie unsicher ist ein beobachteter Unterschied?')
 size=st.slider('Teilnehmer je randomisierter Gruppe',100,20000,2000,100)
 rng=np.random.default_rng(123);ca=rng.binomial(size,.12);ta=rng.binomial(size,np.clip(.12+lift/100,0,1));diff=ta/size-ca/size;se=np.sqrt((ta/size)*(1-ta/size)/size+(ca/size)*(1-ca/size)/size)
 low,high=diff-1.96*se,diff+1.96*se
 st.metric('Simulierter A/B-Unterschied',f'{diff*100:+.2f} Prozentpunkte');st.write(f'Ungefähres 95-%-Wald-Intervall: **{low*100:+.2f} bis {high*100:+.2f} Prozentpunkte**.')
 st.success('Das Intervall liegt über null. Jetzt noch Kosten, Mehrfachtests und praktische Relevanz prüfen.') if low>0 else st.info('Kein klarer positiver Nachweis. „Wir haben es gefühlt“ ist leider kein Konfidenzintervall.')
 explain('Wenn alle mehr kaufen, war deine Kampagne vielleicht nicht der einzige Grund. Eine Vergleichsgruppe hilft.','Randomisierung stützt kausale Aussagen. Difference-in-Differences benötigt insbesondere plausible parallele unbehandelte Trends.','A/B-Simulation mit unabhängigen Binomialziehungen und approximativem Wald-Intervall. Keine echte Studie. Für seltene Ereignisse robustere Intervalle verwenden; Auswertung vorher festlegen.','Korrelation ist, wenn Eisverkauf und Sonnenbrand zusammen steigen. Das Eis ist trotzdem unschuldig.')

else:
 st.write('### Transparenz ist ein Feature. Auch wenn sie weniger glitzert als „AI-powered“ / KI-gestützt.')
 sources=[['Retailrocket','Views, Warenkorb, Transaktionen','Session-/Kaufprognose','https://www.kaggle.com/datasets/retailrocket/ecommerce-dataset'],['Amazon-M2','Sessions und Produktinformationen','Mehrsprachige Sequenzempfehlung','https://github.com/haitaomao/amazon-m2'],['REES46','Verhaltensdaten mehrerer Branchen','Robustheit über Shopkategorien','https://rees46.com/en/datasets'],['Amazon Reviews 2023','Rezensionen und Produktmetadaten','Text, Bilder, Cold Start','https://amazon-reviews-2023.github.io/'],['Amazon ESCI','Suchanfragen und Relevanzurteile','Suche, Alternativen, Ergänzungen','https://github.com/amazon-science/esci-data']]
 for name,data,task,url in sources:
  with st.container(border=True):st.markdown(f'**[{name}]({url})** · {data}');st.caption(task+' · Noch nicht heruntergeladen oder trainiert.')
 st.warning('Die Quellen sind unabhängige Benchmarks. Keine gemeinsamen Kunden-IDs, keine behauptete Zusammenführung. Zugang und Nutzungsbedingungen vor einem Import prüfen. Reale Kostendaten und randomisierte Marketingdaten fehlen.')
 st.write('#### Ein echter Dateneinstieg: Retailrocket-Datei prüfen')
 uploaded=st.file_uploader('events.csv hochladen (bis 200 MB; nur erste 100.000 Zeilen werden gelesen)',type=['csv'])
 if uploaded:
  try:
   raw=pd.read_csv(uploaded,nrows=100000);required={'timestamp','visitorid','event','itemid'}
   if not required.issubset(raw.columns):st.error('Fehlende Spalten: '+', '.join(sorted(required-set(raw.columns))))
   else:
    raw['timestamp']=pd.to_numeric(raw.timestamp,errors='coerce');valid=raw.timestamp.notna() & raw.visitorid.notna() & raw.itemid.notna() & raw.event.isin(['view','addtocart','transaction'])
    st.write(f'{len(raw):,} eingelesene Zeilen · {int(valid.sum()):,} formal gültig · {int((~valid).sum()):,} verworfen')
    clean=raw[valid].copy();st.dataframe(clean.head(20),hide_index=True)
    if len(clean):
     st.bar_chart(clean.event.value_counts());st.write('Besucher in dieser Teilmenge:',clean.visitorid.nunique());st.caption('Teilmenge in Dateireihenfolge, keine repräsentative Stichprobe. Nur Schema-/Werteprüfung, keine vollständige Qualitäts- oder Leakage-Prüfung.')
  except (ValueError,pd.errors.ParserError,UnicodeDecodeError) as e:st.error('Datei konnte nicht als Retailrocket-CSV gelesen werden: '+str(e))
 st.write('#### Was läuft – und was ist die nächste Ausbaustufe?')
 st.dataframe(pd.DataFrame([['Finanzen / Marketing / Experimente','Interaktive, deterministische oder stochastische Simulation'],['Empfehlung / Suche','Regelbasierte Baselines und Wortabgleich'],['Graph','Redaktioneller Beispielgraph'],['Retailrocket','CSV-Vorschau und Validierung'],['BERT4Rec / SASRec / LightGCN','Trainierbare kompakte Implementierungen im Trainingslabor; hier keine geladenen Modelle'],['Sentence Transformers / CLIP','Optional ausführbar im Suchstudio; benötigt Modell-Download'],['Uplift-Schätzung','T-Learner im Marketinglabor; diese Story nutzt Oracle-Simulation']],columns=['Bereich','Status']),hide_index=True)
 st.write('**Benchmark-Regeln:** Zeitbasierter Split; Trainingstransformationen nur auf Trainingsdaten anpassen; Recall@20 und NDCG@10; Kandidatenprotokoll dokumentieren; neue Artikel und kurze Sessions separat; Laufzeit und Ressourcen berichten. Keine frei erfundenen Scores.')
 st.code('streamlit run app.py',language='bash')

st.divider()
st.caption('FLIGHT · Portfolio von Amit Steinberg · Projekt-Version 0.2 · Alle angezeigten Shopdaten, Margen und Effekte sind synthetisch, außer ausdrücklich als hochgeladene Daten ausgewiesen.')
