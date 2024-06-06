import glob
import argparse
from tqdm import tqdm
import concurrent.futures
from library import Add_breakpoints_to_one_folder

parser=argparse.ArgumentParser(description='Execute BreakPointing Pipeline')
parser.add_argument('--workers', type=int, help='max cpu worker to be used', default=2)
parser.add_argument('--customer', type=str, help='customer name as per path', required=True)
parser.add_argument('--plot', action='store_true', help="plotting is done serially so workers are ignored")

args = parser.parse_args()

customer=args.customer
workers=args.workers
plot=args.plot

folders=glob.glob(f"./DATA/{customer}/processed/*")

if plot:
    for folder in tqdm(folders):
        Add_breakpoints_to_one_folder(folder,plot)
else:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        results=list(tqdm(executor.map(lambda folder:Add_breakpoints_to_one_folder(folder,plot), folders),total=len(folders)))

print("Completed")