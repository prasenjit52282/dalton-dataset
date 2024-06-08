import glob
import argparse
import pandas as pd

parser=argparse.ArgumentParser(description='Merge Data from all replica dataset')
parser.add_argument('--customer', type=str, help='customer name as per path', required=True)
args = parser.parse_args()

customer=args.customer

#Gathering all replica files
files=glob.glob(f"./Data/{customer}/*.csv")

#Concatinating all files
df=pd.concat([pd.read_csv(f) for f in files],axis=0)
#Filtering out only for the customer
df_customer=df[df.Customer==customer].reset_index(drop=True)
#removing all duplicate entires from the replicas
df_customer.drop_duplicates(inplace=True)
#dumping the unique entries
df_customer.to_csv(f"./Merged/data_{customer}.csv",index=False)
print(f"Merged for {customer}")