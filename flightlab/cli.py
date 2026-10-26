"""Run with python -m flightlab.cli. Artifacts remain outside git by default."""
import argparse
from .data import demo_events,load_path
from .benchmark import run,save

def main():
 p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--source',default='Retailrocket',choices=['Retailrocket','REES46','Amazon Reviews 2023']);p.add_argument('--limit',type=int,default=100000);p.add_argument('--models',nargs='+',default=['Popularität','ItemKNN','Markov']);p.add_argument('--epochs',type=int,default=2);p.add_argument('--out',default='artifacts/latest.json');p.add_argument('--cases',type=int,default=300);args=p.parse_args()
 data=load_path(args.input,args.source,args.limit) if args.input else demo_events()
 result,fitted,_=run(data,args.models,args.epochs,args.cases,args.source if args.input else 'SYNTHETISCH');save(result,args.out)
 from .artifacts import export_models
 from pathlib import Path
 export_models(fitted,Path(args.out).with_suffix(''))
 print(args.out)
if __name__=='__main__':main()
