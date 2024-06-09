import os
import glob
import argparse
from tqdm import tqdm
import concurrent.futures
from library import process_feat_for

parser=argparse.ArgumentParser(description='Execute Feat computation Pipeline')
parser.add_argument('--workers', type=int, help='max cpu worker to be used', default=2)
parser.add_argument('--customer', type=str, help='customer name as per path', required=True)
args = parser.parse_args()

customer=args.customer
workers=args.workers

files=glob.glob(f"./Processed/{customer}/*/*.csv")

#Making parent directory
parent_dir=f"./Features/{customer}"
os.makedirs(parent_dir,exist_ok=True)


with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
    results=list(tqdm(executor.map(lambda e:process_feat_for(e,parent_dir), files),total=len(files)))
    
print("Completed")