"""Consistent navigation and introductions for the deeper workspaces."""
import streamlit as st
from .story import LABS

def workspace_links():
 for path,label in LABS:
  st.page_link(path,label=label)

def lab_header(title,purpose,output,chapter):
 with st.sidebar:
  st.page_link('app.py',label='← Zur geführten Geschichte')
  st.caption('Du bist in einem vertiefenden Arbeitsbereich.')
  with st.expander('Anderen Arbeitsbereich öffnen'):
   workspace_links()
 st.title(title)
 st.write(purpose)
 st.info('**Was du hier bekommst:** '+output)
 st.caption('Gehört zur Geschichte: '+chapter)

def detail(business,technical,status):
 with st.expander('Für Geschäftsleute: Nutzen und Kennzahl'):
  st.write(business)
 with st.expander('Für Fachleute: Methode und Grenzen'):
  st.write(technical)
 st.caption('So arbeitet dieses Beispiel: '+status)
