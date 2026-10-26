"""Text retrieval, optional semantic and cross-modal retrieval."""
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

def text_search(texts,query,semantic=False):
 if semantic:
  from sentence_transformers import SentenceTransformer
  model=SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
  vectors=model.encode(list(texts),normalize_embeddings=True);q=model.encode([query],normalize_embeddings=True)
  return vectors @ q[0]
 vectorizer=TfidfVectorizer(ngram_range=(1,2),analyzer='char_wb',min_df=1)
 vectors=vectorizer.fit_transform(texts);return (vectors @ vectorizer.transform([query]).T).toarray().ravel()

def image_search(images,query):
 from sentence_transformers import SentenceTransformer
 model=SentenceTransformer('clip-ViT-B-32')
 vectors=model.encode(images,normalize_embeddings=True);q=model.encode([query],normalize_embeddings=True)
 return vectors @ q[0]
