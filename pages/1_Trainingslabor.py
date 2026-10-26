import json
import pandas as pd
import streamlit as st
from flightlab.data import SOURCES,demo_events,normalize,m2_sequences
from flightlab.benchmark import run,run_sessions
from flightlab.recommend import rank

st.set_page_config(page_title='Flight · Trainingslabor',page_icon='🧪',layout='wide')
st.title('🧪 Trainingslabor: Der Algorithmus muss liefern')
st.write('Hier werden Modelle wirklich angepasst und auf zurückgehaltenen Ereignissen gemessen. Der Bestseller bekommt denselben Test wie der Transformer. Vetternwirtschaft gibt es nur im Produktgraphen.')
source=st.selectbox('Unabhängiger Datensatz',['Synthetischer Funktionstest','Retailrocket','REES46','Amazon Reviews 2023','Amazon-M2'])
limit=st.slider('Maximal eingelesene Zeilen',1000,200000,20000,1000)
events=None;session_rows=None
if source=='Synthetischer Funktionstest':events=demo_events();st.warning('Künstliche Sequenzen. Resultate prüfen Code, nicht Marktleistung.')
else:
 st.markdown(f'[Originalquelle]({SOURCES[source][0]})');st.caption(SOURCES[source][1])
 file=st.file_uploader('CSV beziehungsweise Reviews-JSONL',type=['csv','jsonl'])
 if file:
  try:
   raw=pd.read_json(file,lines=True,nrows=limit) if source=='Amazon Reviews 2023' else pd.read_csv(file,nrows=limit)
   if source=='Amazon-M2':session_rows=m2_sequences(raw);st.info(f'{len(session_rows)} Sessions erkannt. Eigener Session-Holdout: keine globale Zeitgarantie und kein offizieller Challenge-Score.')
   else:events=normalize(raw,source)
  except Exception as e:st.error(str(e))
if events is not None or session_rows is not None:
 if events is not None: st.write(f'{len(events):,} Ereignisse · {events.user.nunique():,} Kunden · {events.item.nunique():,} Artikel');st.dataframe(events.head(8),hide_index=True)
 names=st.multiselect('Modelle',['Popularität','ItemKNN','Markov','BERT4Rec','SASRec','LightGCN'],default=['Popularität','ItemKNN','Markov'])
 epochs=st.slider('Epochen für neuronale Modelle',1,20,2);cases=st.slider('Testfälle',50,1000,200,50)
 st.caption('Optional: pip install -r requirements-ml.txt. Vollkatalog-Auswertung kostet bei großen Katalogen Zeit. GUI-Training auf kleine Teilmengen begrenzen.')
 if st.button('🚀 Trainieren und fair vergleichen',disabled=not names):
  try:
   with st.spinner('Die Modelle rechnen. Der CFO fragt bereits nach den Stromkosten …'):
    report,models,test_cases=run(events,names,epochs,cases,source) if events is not None else run_sessions(session_rows,names,epochs,source)
   st.session_state['benchmark']=(report,models,test_cases)
  except ImportError:st.error('Neuronale Abhängigkeiten fehlen. Im Terminal: pip install -r requirements-ml.txt')
  except Exception as e:st.error('Training abgebrochen: '+str(e))
if 'benchmark' in st.session_state:
 report,models,test_cases=st.session_state['benchmark'];st.caption('Letzter ausgeführter Lauf: '+report['source']+' · Fingerprint '+report['fingerprint'][:16])
 st.dataframe(pd.DataFrame(report['results']),hide_index=True);st.bar_chart(pd.DataFrame(report['results']).set_index('Modell')[['Recall@10','NDCG@10']])
 st.download_button('📥 Vollständiges Laufprotokoll',json.dumps(report,ensure_ascii=False,indent=2),'flight_benchmark.json','application/json')
 model=st.selectbox('Eine Empfehlung untersuchen',list(models));history,target=test_cases[0]
 st.write('Historie:', ' → '.join(history));st.write('Tatsächlicher nächster Artikel:',target)
 st.dataframe(pd.DataFrame(rank(models[model],history,10),columns=['Artikel','Score']),hide_index=True)
 st.info('Recall@10: War der gesuchte Artikel dabei? NDCG@10: Stand er weit oben? Kalte Zielartikel zählen separat. Wiederholungskäufe bleiben erlaubt. Diese Auswahl der ersten Testfälle ist keine repräsentative Zufallsstichprobe.')
 with st.expander('Technischer Vertrag'):
  st.json({k:v for k,v in report.items() if k!='results'})
  st.write('BERT4Rec-/SASRec-artige kompakte Implementierungen, keine exakte Paper-Reproduktion. LightGCN lernt auf einem bipartiten Graphen mit BPR; Sessioninferenz mittelt historische Itemvektoren. Nur Trainingsdaten definieren Vokabular und Graph.')
 if hasattr(models[model],'vectors') and len(models[model].items)>2:
  from sklearn.decomposition import PCA
  import plotly.express as px
  vectors=models[model].vectors;coords=PCA(n_components=2,random_state=42).fit_transform(vectors)
  st.subheader('Gelernte Produktlandschaft')
  st.plotly_chart(px.scatter(x=coords[:,0],y=coords[:,1],hover_name=models[model].items,labels={'x':'Hauptkomponente 1','y':'Hauptkomponente 2'}),width='stretch')
  st.caption('PCA-Projektion tatsächlich gelernter LightGCN-Itemvektoren. Zweidimensionale Nähe ist eine verlustbehaftete Visualisierung, kein Komplementaritätsnachweis.')
