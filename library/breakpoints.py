import os
import glob
# import matplotlib
import matplotlib.pyplot as plt
# matplotlib.use("Agg")

import numpy as np
import pandas as pd
import ruptures as rpt
from .constants import POLLUTANTS,PEN

def downsample_10sec(df_cpy):
    df_cpy['ts10sec']=df_cpy.ts.apply(lambda e:e[:-1])
    df_10sec=df_cpy.groupby('ts10sec')[POLLUTANTS].mean()
    return df_10sec

def get_normalized_signals(df_10sec):
    #computing min and max only on positive pollutants
    #corner case: when CO2 is invalid for whole day then results NaN for CO2 min and max
    #NaN min max values are repalced with 0
    gMin=df_10sec[df_10sec[POLLUTANTS]>0][POLLUTANTS].quantile(0.0015).replace(np.nan,0) #upto 3 std 99.7%
    gMax=df_10sec[df_10sec[POLLUTANTS]>0][POLLUTANTS].quantile(0.9985).replace(np.nan,0) #upto 3 std 99.7%
    
    #Normalizing all signals (stability factor eps: 1e-10)
    signal_norm=((df_10sec[POLLUTANTS]-gMin)/((gMax-gMin)+1e-10)).clip(0,1)
    return signal_norm


def detect_breakpoints(df,PEN=PEN,use_algo='KLCPD',plot=False,scaled=True,title=None):    
    df_cpy=df.copy()
    #downsample samples to 1sample per 10 sec
    df_10sec=downsample_10sec(df_cpy)

    #normalized the polution signatures based on Min-Max strategy
    signal_norm=get_normalized_signals(df_10sec)

    if use_algo=='KLCPD':
        algo=rpt.KernelCPD(kernel='rbf',min_size=(30*60/10)).fit(signal_norm.values)
    elif use_algo=='PELT':
        algo=rpt.Pelt(model='rbf').fit(signal_norm.values)
    idx=algo.predict(pen=PEN)[:-1] #ignoring end bkpt 
    BKPS=np.array(list(signal_norm.index))[np.array(idx)]

    #plotting
    if plot:
        fig,ax=plt.subplots(figsize=(14,4))
        if title is not None:fig.suptitle(title)
        for c in POLLUTANTS:
            if scaled:
                ax.plot(signal_norm[c],label=c)
            else:
                ax.plot(df_10sec[c],label=c)
        for ts in BKPS:
            ax.axvline(ts, linestyle="dashed",color='k')

        if scaled: 
            ax.set_ylim(0,1)
            ax.set_ylabel(f"Saturation (pen={PEN})")
        else:
            ax.set_ylabel(f"Concentration (pen={PEN})")
        ax.set_xlabel("T")
        plt.xticks(BKPS,map(lambda e:str(e).split()[1],BKPS),rotation=45)
        plt.legend(ncols=10,loc=(0.1,1.01))
        plt.tight_layout()
        plt.close()
        return list(map(lambda e:e+'0',BKPS)),fig #adding zero, returning fig
    else:
        return list(map(lambda e:e+'0',BKPS)) #adding zero


def Add_breakpoints_to_one_folder(folder,plot=False):
    files_in_folder=glob.glob(folder+"/*.csv")
    if plot: os.makedirs(f"{folder}/BKPS",exist_ok=True)
    for file in files_in_folder:
        df=pd.read_csv(file)
        if plot:
            BKPS,fig=detect_breakpoints(df,PEN=PEN,use_algo="KLCPD",plot=plot)
            fig.savefig(f"{folder}/BKPS/{file.split('/')[-1].replace('csv','png')}")
        else:
            BKPS=detect_breakpoints(df,PEN=PEN,use_algo="KLCPD",plot=plot)
        df['bkps']=df['ts'].apply(lambda e: 1 if e in BKPS else 0)
        df.to_csv(file,index=False)