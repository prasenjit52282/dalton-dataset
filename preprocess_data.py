import os
import argparse
import pandas as pd
from tqdm import tqdm
import concurrent.futures
from library import process_for_one_device_at_date

parser=argparse.ArgumentParser(description='Execute Data pre-Processing Pipeline')
parser.add_argument('--workers', type=int, help='max cpu worker to be used', default=2)
parser.add_argument('--customer', type=str, help='customer name as per path', required=True)
args = parser.parse_args()

customer=args.customer
workers=args.workers

df=pd.read_csv(f"./Merged/data_{customer}.csv")

df['Date']=df.ts.apply(lambda e: e.split()[0])
params=list(df.groupby(['Date','ID','Loc']))


#Making parent directory
parent_dir=f"./Processed/{customer}"
os.makedirs(parent_dir,exist_ok=True)


with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    results=list(tqdm(executor.map(lambda e:process_for_one_device_at_date(*e[0],e[1],parent_dir), params),
                      total=len(params)))

print(f"Completed for {customer}")