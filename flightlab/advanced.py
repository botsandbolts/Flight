"""Interactive technical evidence below the business story. Demo provenance is explicit."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

TOPICS=[
 dict(title='E-Commerce als Entscheidungssystem',business='Ein Onlinehändler optimiert nicht nur Klicks. Produktsuche, Kaufabsicht, Warenkorb, Retouren und Marketingkosten wirken auf denselben Beitrag.',tech='Die Architektur trennt Retrieval, Ranking, Entscheidungspolitik und Ausführung. Ein Feature-/Kennzahlenvertrag definiert Ereigniszeit, Identitäten und verfügbare Informationen. Ein Sprachmodell ist eine zusätzliche Komponente für Sprache und Werkzeugkoordination.',metric='Beitrag je Besuch und inkrementeller Beitrag; außerdem Sucherfolg, Retouren, Service und Laufzeit.',limit='Die Funnelzahlen unten sind ein Szenario. Verbindungen zeigen Mengenflüsse und keine Ursache-Wirkungs-Beweise.',experiment='Ein gemeinsamer Eventvertrag verbindet session_id, item_id, event_time und action. Reale Kosten werden separat versioniert zugeordnet.',joke='Ein Klick ist ein Anfang. Der CFO akzeptiert ihn leider nicht als Überweisung.'),
 dict(title='Semantische und multimodale Produktsuche',business='Der Suchwunsch muss zum Katalog passen. Harte Einschränkungen wie Preis, Bestand oder Größe gehören zusätzlich zur Ähnlichkeitssuche.',tech='Ein Bi-Encoder erzeugt normalisierte Vektoren. Kosinusähnlichkeit liefert Kandidaten; ein Reranker kann Anfrage und Artikel gemeinsam bewerten. Sentence Transformers verarbeiten Text. CLIP bildet Text und Bilder in einen gemeinsamen Raum ab. Ein Diffusionsmodell erzeugt dagegen neue Bilder.',metric='NDCG für Suchrelevanz, Recall der Kandidaten, Latenz und Fehler bei harten Filtern; Cold-Start-Qualität für neue Artikel.',limit='Die laufende Visualisierung nutzt echte TF-IDF-Vektoren auf einem synthetischen Minikatalog. Sie ist keine Messung eines Sentence-Transformer- oder CLIP-Modells.',experiment='Im Suchstudio lassen sich echte Sentence-Transformer- und CLIP-Gewichte optional laden. ESCI liefert separat Relevanzlabels; neue Bilder sind kein Beleg für Produktmerkmale.',joke='Anna sucht eine Maschine. Sie möchte nicht erst den exakten Datenbankbezeichner heiraten.'),
 dict(title='Transformer, Graph und Ranking im Zusammenspiel',business='Aktuelle Absicht und langfristige Ähnlichkeit sind verschiedene Signale. Kandidaten müssen nützlich sein, bevor Marge, Verfügbarkeit und Kontaktregeln die Reihenfolge verändern.',tech='Attention berechnet softmax(Q K^T / sqrt(d) + Maske). BERT4Rec rekonstruiert maskierte Artikel mit bidirektionaler Attention. SASRec sagt mit kausaler Attention nachfolgende Artikel voraus. LightGCN propagiert Embeddings über den bipartiten User-Item-Graphen und lernt mit BPR: -log sigmoid(s_pos - s_neg), ergänzt um Regularisierung. Ein zweistufiges System kann Kandidaten aus mehreren Verfahren zusammenführen und neu sortieren.',metric='Recall@K misst Treffer, NDCG@K belohnt frühe Treffer. Kandidatenprotokoll, kalte Zielartikel und wiederholte Käufe müssen dokumentiert werden.',limit='Die Attention-Grafik ist eine vollständig deklarierte Toy-Rechnung aus synthetischen Q/K-Vektoren. Sie stammt nicht aus einem trainierten BERT4Rec. Der Graph ist ein Beispielnetz.',experiment='Trainiere alle sechs implementierten Verfahren im Trainingslabor. Vergleiche sie zeitlich getrennt gegen Popularität, ItemKNN und Markov. Hyperparameter nur auf einem zusätzlichen Validierungsset auswählen.',joke='Ein größerer Transformer ist beeindruckend. Ein fair gewonnener Vergleich ist beeindruckender.'),
 dict(title='Deckungsbeitrag, Preis und wirtschaftliches Ranking',business='Die Zielgröße muss zur Entscheidung passen. Umsatzoptimierung kann Rabatte, teure Retouren oder geringe Margen begünstigen.',tech='Eine Entscheidungspolitik kombiniert kalibrierte Kaufwahrscheinlichkeit mit erwartetem Beitrag und Nebenbedingungen. Preiselastizität benötigt geeignete Variation; beobachtete Preise sind oft endogen. SHAP kann Modellbeiträge erklären, beweist aber keine kausale Wirkung.',metric='Erwarteter DB je Exposition, realisierter DB nach Retouren, Budget, Verfügbarkeit und Servicefolgen. Fixkosten ausdrücklich separat betrachten.',limit='Die Sensitivitätsfläche ist eine Kostenrechnung unter Annahmen. Sie schätzt keine Preiselastizität und keine Zahlungsbereitschaft.',experiment='Nutze randomisierte Preis-/Angebotstests, sofern betrieblich geeignet. Sonst Identifikationsannahmen offenlegen. Prüfe Kalibrierung und Stabilität vor einer wertbasierten Rangfolge.',joke='Mehr Umsatz und weniger Geld: ein Klassiker, den niemand im Controlling nachbestellen möchte.'),
 dict(title='Uplift und kausale Marketingentscheidungen',business='Ein Angebot soll zusätzliche Wirkung erzielen. Der wahrscheinlichste Käufer ist nicht zwingend der beste Empfänger eines Gutscheins.',tech='Ein T-Learner schätzt mu1(x) und mu0(x) getrennt. Ihr Unterschied ist geschätzte Heterogenität. Cross-Fitting und doubly robust Schätzung sind mögliche Weiterentwicklungen, hier nicht implementiert. Evaluation auf zurückgehaltenen randomisierten Daten per IPW und Upliftkurve.',metric='AUUC oberhalb Zufall, kalibrierte Gruppenwirkungen und inkrementeller Beitrag nach Kontakt- und Gutscheinkosten. Individuelle Effekte bleiben unbeobachtbar.',limit='Das Streudiagramm zeigt bekannte Effekte einer künstlichen Population. Criteo untersucht Werbung, nicht die Gutscheine dieses Shops. Ein Präfix ohne Kontrollgruppe wurde korrekt abgewiesen.',experiment='Im Marketinglabor wird ein T-Learner tatsächlich trainiert, wenn geeignete Treatment-/Kontrolldaten vorliegen. exposure ist post-treatment und darf nicht als Zuweisung oder Eingangsfeature dienen.',joke='Rabatte für sichere Käufer sind die teuerste Form der Höflichkeit.'),
 dict(title='AI Agents, RAG und operative Planung',business='Onlineversprechen hängen von Beständen und bestätigten Lieferinformationen ab. Ein Agent kann Informationen koordinieren; das Unternehmen trägt weiterhin die Verantwortung für Aktionen.',tech='RAG verbindet Retrieval und belegten Kontext. Tool-Calling trennt strukturierte Werkzeuganfrage und Ausführung. Ein Agentenloop ergänzt Zustand, Abbruchbedingungen und begrenzte Rechte. Flight führt derzeit einen festen lokalen Workflow aus; optionale OpenAI-/Anthropic-APIs formulieren Textentwürfe.',metric='Korrektheit von Zahlen und Quellen, erfolgreiche Tool-Ausführung, Eskalationen, Antwortzeit, Kosten je gelöstem Vorgang und tatsächlich realisierter Nutzen.',limit='Bestandssimulation und Rollenablauf sind lokal. Kein ERP oder Kundensystem ist verbunden. Gemini, autonome Multi-Agent-Orchestrierung und lokale LLM-Server sind Architekturoptionen, nicht implementierte Laufzeit.',experiment='Teste ChatGPT/OpenAI und Claude/Anthropic mit denselben belegten Aufgaben. Prüfe Tool-Argumente, Antworttreue und Kosten. Ein zweiter LLM-Prüfer ersetzt keinen Ground Truth.',joke='Der Agent darf vorbereiten. Eine Yacht als Kulanz braucht immer noch eine sehr gute Erklärung.'),
 dict(title='Experimente, Ökonometrie und Unsicherheit',business='Eine bessere Kennzahl kann durch Zufall oder den Markt entstehen. Erfolg braucht eine passende Gegenprobe und die wirtschaftlich richtige Zielgröße.',tech='A/B-Tests nutzen Randomisierung. Difference-in-Differences benötigt insbesondere parallele unbehandelte Trends. OLS allein schafft keine Kausalität. Mehrfachtests, zeitliche Abhängigkeit und Interferenz können Standardfehler und Interpretation verändern.',metric='Effekt mit Intervall, minimale relevante Wirkung, Stichprobenumfang, DB und Nebenmetriken. Ein statistisch positiver Effekt kann wirtschaftlich unbedeutend sein.',limit='Die Intervallgrafik basiert auf erfundenen festen Kaufraten, nicht auf einer erhobenen Studie. Wald-Intervalle sind eine Approximation.',experiment='Definiere Metrik, Randomisierungseinheit, Horizont und Auswertung vor dem Start. Das Evidenzstudio enthält eine separate OLS-/DiD-Auswertung mit HC3- oder Cluster-Standardfehlern.',joke='Das Konfetti wird erst bestellt, wenn der Unsicherheitsbereich mitfeiert.'),
 dict(title='MLOps, Datenverträge und glaubwürdige Evidenz',business='Eine Demo wird zum belastbaren Portfolio, wenn eine andere Person die Schritte wiederholen und Grenzen erkennen kann.',tech='Zeitlicher Split, Trainingsvokabular und unveränderte Testdaten verhindern typische Leakage-Fehler. Laufprotokolle enthalten Fingerprints, Seed, Kandidatenraum und Zeiten. JSON/NPZ/state_dict werden getrennt von der Oberfläche exportiert. CI prüft Daten-, Modell- und GUI-Verträge.',metric='Reproduzierbarkeit, Datenqualität, Abdeckung, Drift, Laufzeit und Kosten. Produktionswirkung wird gesondert online gemessen.',limit='Aktuell kein nachgewiesener kommerzieller Effekt. Der kleine Amazon-Präfixtest erreichte keinen Top-10-Treffer auf den warmen Testzielen. Das ist ein Entwicklungsbefund und kein allgemeines Modellurteil.',experiment='Nächster Schritt: repräsentativer Datenbestand, zusätzliches Validierungsset, größere Tests und begrenzter Onlinepilot. Öffentlich verfügbare Quellen bleiben getrennte Benchmarks.',joke='Die ehrlich dokumentierte Null ist nützlicher als eine dekorativ erfundene Eins.')
]

def plot_data(index,parameter=1.):
 rng=np.random.default_rng(42)
 if index==0:
  return {'labels':['Besuche','Produktkontakt','Warenkorb','Kauf','Abbruch','Retoure','Behalten'], 'source':[0,1,1,2,2,3,3], 'target':[1,2,4,3,4,5,6], 'value':[10000,2000,8000,500,1500,75,425]}
 if index==1:
  from sklearn.feature_extraction.text import TfidfVectorizer
  from sklearn.decomposition import TruncatedSVD
  texts=['kleine schwarze kaffeemaschine espresso','große silberne kaffeemaschine espresso','schwarze kaffeemühle bohnen','kaffeebohnen espresso aroma','schwarzer reisebecher kaffee']
  v=TfidfVectorizer();x=v.fit_transform(texts);return {'matrix':(x@x.T).toarray(),'coords':TruncatedSVD(n_components=2,random_state=42).fit_transform(x),'labels':['Mini','Premium','Mühle','Bohnen','Becher']}
 if index==2:
  q=rng.normal(size=(6,8));k=q+ rng.normal(size=(6,8))*.4;s=q@k.T/np.sqrt(8)/parameter
  s=np.where(np.triu(np.ones((6,6)),1).astype(bool),-1e9,s);w=np.exp(s-s.max(1,keepdims=True));w/=w.sum(1,keepdims=True)
  return {'matrix':w,'labels':['Suche','Mini','Preisfilter','Refurbished','Mühle','Warenkorb']}
 if index==3:
  discount=np.arange(0,31,2);reserve=np.arange(0,21,2);return {'x':discount,'y':reserve,'matrix':100-discount[None,:]-50-6-reserve[:,None]-12}
 if index==4:
  p0=rng.uniform(.02,.7,500);tau=.18*np.sin(np.arange(500)*.07)-.02;p1=np.clip(p0+tau,0,1);return {'p0':p0,'tau':p1-p0,'db':(p1-p0)*40-p1*parameter-.2}
 if index==5:
  demand=rng.normal(40,12,size=(5000,7)).clip(0).sum(1);return {'demand':demand,'stock':parameter,'shortage':float(np.mean(demand>parameter))}
 if index==6:
  from .story import teaching_experiment
  return pd.DataFrame([teaching_experiment(n) for n in [1000,2500,5000,10000,25000,50000]])
 return pd.DataFrame({'Dimension':['Datenverträge','Baselines','Transformer/GNN','Text/Bild-Modelle','Kausalmethoden','API-Textentwürfe','Produktionswirkung'],'Status':['implementiert','ausgeführt','kompakter Code + kleine Trainingsläufe','optional mit Gewichten ausführbar','T-Learner/OLS implementiert','Adapter, nicht live getestet','offen']})

def figure(index,parameter=1.):
 d=plot_data(index,parameter)
 if index==0:
  f=go.Figure(go.Sankey(node={'label':d['labels']},link={k:d[k] for k in ['source','target','value']}))
 elif index in [1,2,3]:
  f=px.imshow(d['matrix'],x=d.get('labels',d.get('x')),y=d.get('labels',d.get('y')),color_continuous_scale='Teal',aspect='auto',labels={'color':'Kosinus' if index==1 else 'Gewicht' if index==2 else 'Beitrag (€)'})
  if index==3:f.update_xaxes(title='Rabatt (€)');f.update_yaxes(title='Retourenkostenreserve (€)')
 elif index==4:f=px.scatter(x=d['p0'],y=d['tau'],color=d['db'],labels={'x':'Kaufchance ohne Aktion','y':'Bekannter künstlicher Uplift','color':'Zusatz-DB (€)'},color_continuous_scale='RdYlGn')
 elif index==5:
  f=px.histogram(x=d['demand'],nbins=40,labels={'x':'Simulierter Bedarf in 7 Tagen','y':'Simulationen'});f.add_vline(x=parameter,line_color='red',annotation_text='Bestand')
 elif index==6:
  f=go.Figure(go.Scatter(x=d.n,y=d.difference_pp,mode='lines+markers',error_y={'type':'data','array':d.high_pp-d.difference_pp,'arrayminus':d.difference_pp-d.low_pp}));f.add_hline(y=0);f.update_xaxes(type='log',title='Personen je Gruppe');f.update_yaxes(title='Unterschied und 95-%-Intervall (Prozentpunkte)')
 else:return None
 f.update_layout(height=410,margin=dict(l=25,r=25,t=30,b=30));return f

def render(index):
 import streamlit as st
 topic=TOPICS[index];st.divider();st.header('Business & Data Science: die technische Vertiefung')
 st.subheader(topic['title']);st.write('**Geschäftliche Frage:** '+topic['business'])
 if index==2:parameter=st.slider('Temperatur der Toy-Attention',.3,3.,1.,.1,key='attn_temp')
 elif index==4:parameter=st.slider('Gutschein in der künstlichen Population (€)',0,20,10,key='advanced_coupon')
 elif index==5:parameter=st.slider('Bestand für die Risikosimulation',100,450,180,10,key='advanced_stock')
 else:parameter=1.
 f=figure(index,parameter)
 if f is not None:st.plotly_chart(f,width='stretch')
 else:st.dataframe(plot_data(7),hide_index=True,width='stretch')
 st.caption('Evidenzstatus: '+topic['limit'])
 if index==1:
  data=plot_data(1);st.plotly_chart(px.scatter(x=data['coords'][:,0],y=data['coords'][:,1],text=data['labels'],labels={'x':'SVD-Komponente 1','y':'SVD-Komponente 2'}),width='stretch');st.caption('SVD-Projektion derselben TF-IDF-Vektoren. Zweidimensionale Nähe ist verlustbehaftet.')
 if index==2:
  st.plotly_chart(graph_figure(),width='stretch');st.caption('Illustratives Interaktionsnetz, keine gelernten Kanten. Im Trainingslabor kann LightGCN auf Trainingsinteraktionen optimiert werden.')
 if index==5:st.metric('Simulierter Anteil mit Bedarf über Bestand',f'{plot_data(5,parameter)["shortage"]:.1%}')
 a,b=st.tabs(['Methode und Interpretation','Messung und nächstes Experiment'])
 with a:st.write(topic['tech'])
 with b:st.write('**Kennzahlen:** '+topic['metric']);st.write(topic['experiment'])
 st.write('☕ '+topic['joke'])

def graph_figure():
 labels=['Anna','Ben','Clara','Mini','Mühle','Bohnen'];x=[0,0,0,1,1,1];y=[2,1,0,2,1,0];edges=[(0,3),(0,4),(1,3),(1,5),(2,4),(2,5)];f=go.Figure()
 for a,b in edges:f.add_trace(go.Scatter(x=[x[a],x[b]],y=[y[a],y[b]],mode='lines',line={'color':'#64b8a7'},showlegend=False,hoverinfo='skip'))
 f.add_trace(go.Scatter(x=x,y=y,text=labels,mode='markers+text',textposition='top center',marker={'size':22,'color':['#e59c80']*3+['#64b8a7']*3},showlegend=False));f.update_xaxes(visible=False);f.update_yaxes(visible=False);f.update_layout(height=330,title='Bipartiter Beispielgraph: Personen und Artikel');return f
