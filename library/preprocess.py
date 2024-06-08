import os
import numpy as np
import pandas as pd
from .constants import MAX_MISSING_MINUTES,SMOOTHING_WINDOW,POLLUTANTS,OVER_WRITE


def preprocess_fn(d,date):
    """
    Input_1[DataFrame]: data for a perticular device (e.g., 11) for a specific date (e.g., 2023/04/04)
    Input_2[str]:       which specific date (e.g., 2023/04/04)
    Output[DataFrame]:  cleaned data
    """
    #step1. remove all unnecessary columns keeping only pollutants
    # d_pol=d.drop(columns=['Customer','ID','Loc','Ph','Date'])
    d_pol=d.drop(columns=['Date'])
    
    #step2. assigning timestamp(ts) as index and sorting data
    #very rarely one sensor has multiple entries for same timestamp
    d_pol['ts']=d_pol.ts.apply(lambda e:pd.to_datetime(e).tz_localize(None))
    d_pol.drop_duplicates(subset=['ts'],inplace=True) 
    d_pol.set_index('ts',inplace=True)
    d_pol.sort_index(inplace=True)
    
    #step3.1. creating entire timestamp range for the day
    filled_ts=pd.date_range(start=f"{date} 00:00:00", end=f"{date} 23:59:59", freq="S")

    #step3.2. reindex with entire timestamp and fill nan values with nearest method 
    #maximum fill limit is MAX_MISSING_MINUITES (e.g., 15 minutes)
    #so if the sensor is off for max 15mins then its value is filled with nearest method
    d_full=d_pol.reindex(filled_ts,method='nearest',limit=MAX_MISSING_MINUTES*60)
    
    #step4.1. marking Valid entries where all sensors have non-null values
    d_full['Valid']=(~(d_full['T'].isna() & d_full['C2H5OH'].isna() & d_full['CO2'].isna())).astype('int')
    
    #step4.2. marking entries where CO2 sensor was effected by static-electricity
    #similar to step3.2. CO2 missing entries has fill limit of MAX_MISSING_MINUITES (e.g., 15 minutes)
    d_full['CO2']=d_full.CO2.apply(lambda e:np.nan if e>10000 else e)
    d_full['CO2']=d_full.CO2.interpolate(method='nearest',limit=MAX_MISSING_MINUTES*60)
    d_full['Valid_CO2']=(~d_full['CO2'].isna()).astype('int')
    
    #step5.1. replacing all nan values with zero before smoothing
    d_full.replace(np.nan,0,inplace=True)

    #step5.2. smoothing pollutants with SMOOTHING_WINDOW (i.e., 60 sec) sensitivity
    #further rounding up to 4 decimal places
    for pol in POLLUTANTS:
        d_full[pol]=d_full[pol].rolling(window=SMOOTHING_WINDOW).mean().bfill().round(decimals=4)

    #step6. geting the timestamp(ts) column back in the dataframe
    d_full.reset_index(names='ts',inplace=True)
    
    return d_full


def process_for_one_device_at_date(date,ID,loc,d,parent_dir):
    folder_name=date.replace("/",'_')
    os.makedirs(f"{parent_dir}/{folder_name}",exist_ok=True)
    
    remarks=loc.replace(' ','_')
    file_name=f"{ID}_{remarks}.csv"
    file_path=f"{parent_dir}/{folder_name}/{file_name}"
    
    if (not os.path.exists(file_path)) or OVER_WRITE:
        preprocess_fn(d,date).to_csv(file_path,index=False)