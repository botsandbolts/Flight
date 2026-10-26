import numpy as np
import pandas as pd
import streamlit as st
from flightlab.search import text_search
st.set_page_config(page_title='Flight · Evidenzstudio',layout='wide')
st.title('📐 Evidenzstudio: Auch die schönste Hypothese braucht Zahlen')
a,b=st.tabs(['Amazon ESCI · Suchrelevanz','Ökonometrie · Kampagnenmessung'])
with a:
 st.write('Lade eine zusammengeführte ESCI-Teilmenge mit query_id, query, product_title und esci_label. Produktmetadaten müssen innerhalb desselben Datensatzes über product_id und product_locale verknüpft sein.')
 file=st.file_uploader('ESCI-CSV',type=['csv'])
 if file:
  d=pd.read_csv(file,nrows=30000)
  if not {'query_id','query','product_title','esci_label'}.issubset(d):st.error('Erforderlich: query_id, query, product_title, esci_label.')
  elif st.button('TF-IDF-Ranking gegen Kandidatenreihenfolge testen'):
   records=[];rng=np.random.default_rng(42)
   for q,g in d.groupby('query_id'):
    if len(g)<2:continue
    rel=g.esci_label.map({'E':3,'S':2,'C':1,'I':0,'Exact':3,'Substitute':2,'Complement':1,'Irrelevant':0})
    if rel.isna().any():continue
    scores=text_search(g.product_title.fillna('').astype(str),str(g['query'].iloc[0]));r=rel.to_numpy();ideal=np.sort(r)[::-1][:10];discount=1/np.log2(np.arange(len(ideal))+2);idcg=np.sum((2**ideal-1)*discount)
    def metric(order):return float(np.sum((2**r[order[:10]]-1)*discount)/idcg) if idcg else 0.
    records.append({'query_id':q,'TF-IDF NDCG@10':metric(np.argsort(-scores)),'Zufall NDCG@10':metric(rng.permutation(len(g)))})
   st.dataframe(pd.DataFrame(records),hide_index=True)
   if records:st.write(pd.DataFrame(records).drop(columns='query_id').mean())
   st.caption('Gewählte Relevanzgewichte E/S/C/I = 3/2/1/0. Eigene Kandidaten-Auswertung, kein offizielles ESCI-Leaderboard. TF-IDF wird pro Query-Kandidatenmenge ohne Relevanzlabels angepasst.')
with b:
 st.write('Difference-in-Differences: Hat sich die behandelte Gruppe nach der Maßnahme stärker verändert als die Vergleichsgruppe?')
 st.caption('Benötigte CSV: outcome, treated, post. treated/post binär. Optional unit für nach Einheit geclusterte Standardfehler.')
 f=st.file_uploader('Kampagnen-Panel als CSV',type=['csv'],key='did')
 if f and st.button('OLS mit Interaktion schätzen'):
  try:
   import statsmodels.formula.api as smf
   d=pd.read_csv(f,nrows=100000)
   if not {'outcome','treated','post'}.issubset(d):raise ValueError('outcome, treated, post fehlen.')
   if not d.treated.isin([0,1]).all() or not d.post.isin([0,1]).all():raise ValueError('treated und post müssen binär sein.')
   d=d.dropna(subset=['outcome','treated','post']+(['unit'] if 'unit' in d else []))
   if d.groupby(['treated','post']).ngroups<4:raise ValueError('Alle vier Gruppen/Zeit-Zellen erforderlich.')
   model=smf.ols('outcome ~ treated * post',d)
   fit=model.fit(cov_type='cluster',cov_kwds={'groups':d.unit}) if 'unit' in d else model.fit(cov_type='HC3')
   st.text(fit.summary().as_text());st.metric('Geschätzter DiD-Effekt',f'{fit.params["treated:post"]:.4f}')
   st.warning('Paralleltrends, keine Antizipation und keine gruppenspezifischen zeitgleichen Schocks sind Identifikationsannahmen. Zwei Zeitpunkte beweisen Paralleltrends nicht. Regression allein macht Beobachtungsdaten nicht kausal.')
  except ImportError:st.error('statsmodels fehlt: pip install -r requirements.txt')
  except Exception as e:st.error(str(e))
