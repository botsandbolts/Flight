"""Bounded, explicit public-file prefix imports; not representative samples."""
import argparse
import csv
import gzip
import io
import itertools
import re
import urllib.request
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('source',choices=['criteo','reviews']);p.add_argument('--rows',type=int,default=20000);p.add_argument('--category',default='All_Beauty');p.add_argument('--out',required=True);args=p.parse_args()
 if not 1<=args.rows<=500000:raise ValueError('rows muss zwischen 1 und 500000 liegen.')
 if not re.fullmatch('[A-Za-z_]+',args.category):raise ValueError('Ungültige Kategorie.')
 url='https://huggingface.co/datasets/criteo/criteo-uplift/resolve/main/criteo-research-uplift-v2.1.csv.gz' if args.source=='criteo' else 'https://huggingface.co/datasets/McAuley-Lab/Amazon-Reviews-2023/resolve/main/raw/review_categories/'+args.category+'.jsonl'
 Path(args.out).parent.mkdir(parents=True,exist_ok=True)
 with urllib.request.urlopen(url,timeout=60) as response:
  if args.source=='criteo':
   reader=csv.reader(io.TextIOWrapper(gzip.GzipFile(fileobj=response)))
   with open(args.out,'w',newline='') as f:csv.writer(f).writerows(itertools.islice(reader,args.rows+1))
   print('WARNUNG: Dateipräfix kann nur Treatment enthalten. Keine repräsentative Stichprobe. Vor Uplift-Training beide Arme prüfen.')
  else:
   with open(args.out,'wb') as f:
    for line in itertools.islice(response,args.rows):f.write(line)
 print(args.out)
if __name__=='__main__':main()
