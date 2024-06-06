import os
import scipy
import numpy as np
import pandas as pd
import ruptures as rpt
from library import downsample_10sec,get_normalized_signals

OVER_WRITE=False

COLUMNS=['CO2','VoC','PMS2_5','PMS10','H','T']
#TARGET LEVELS
CO2_LEVEL=1000 #ppm
VOC_LEVEL= 220 #ppb
PMS2_5_LEVEL= 100 #mu g/m^3 (https://www.iqair.com/india)
PMS10_LEVEL=100 #mu g/m^3   (https://www.iqair.com/india)
H_LEVEL= 60 #% COMFORT
T_LEVEL=26 #deg COMFORT

MIN_PEAK_LVLS=dict(zip(COLUMNS,[CO2_LEVEL,VOC_LEVEL,PMS2_5_LEVEL,PMS10_LEVEL,H_LEVEL,T_LEVEL]))

DOWN_to_10=True
SEC_MULTIPLIER=60 # for 1 min 60 sec
if DOWN_to_10:
    SEC_MULTIPLIER=6 #for 1 min 6 10sec seg
    
GRAD_AVG_WIN=20 #20 sec
if DOWN_to_10:
    GRAD_AVG_WIN=2 #20sec
    
MINUTE=10
WINDOW=MINUTE*SEC_MULTIPLIER

def read_valid(f):
    df=pd.read_csv(f)
    return df[(df.Valid==1) & (df.Valid_CO2==1)].copy()

def read_data(fname,COLUMNS=None,down_to_10=False,norm=False):
    df=read_valid(fname)
    if down_to_10:df=downsample_10sec(df)
    else:
        df['ts']=df.ts.apply(pd.to_datetime)
        df.set_index('ts',drop=True,inplace=True)
    if norm:df=get_normalized_signals(df)
    return df[COLUMNS]



#Breeze (https://www.breeze-technologies.de/blog/calculating-an-actionable-indoor-air-quality-index/)
def co2_idx(co2):
    if 0<=co2<400:
        return 1
    elif 400<=co2<1000:
        return 2
    elif 1000<=co2<1500:
        return 3
    elif 1500<=co2<2000:
        return 4
    elif 2000<=co2<5000:
        return 5
    elif co2>5000:
        return 6

#https://learn.kaiterra.com/en/resources/understanding-tvoc-volatile-organic-compounds
def voc_idx(voc):
    if 0<=voc<=220:
        return 1
    elif 221<=voc<=660:
        return 2
    elif 661<=voc<=1430:
        return 3
    elif 1431<=voc<=2200:
        return 4
    elif 2201<=voc<=3300:
        return 5
    elif voc>=3301:
        return 6

TempHum_mat=\
pd.DataFrame([[6,5,4,3,3,3,3,4,5,5,6,6,6],
[5,4,2,2,2,2,2,3,4,5,5,5,6],
[5,4,3,2,1,1,1,2,3,4,5,5,6],
[5,4,3,2,1,1,1,2,2,3,4,5,6],
[5,5,4,3,2,1,1,1,2,3,4,5,6],
[6,5,5,4,3,3,3,2,2,3,4,5,6],
[6,5,5,4,4,4,4,4,4,4,4,5,6],
[6,5,5,5,5,5,5,5,5,5,5,5,6],
[6,6,6,6,6,6,6,6,6,6,6,6,6]],
index=[9,8,7,6,5,4,3,2,1],
columns=np.array([16,17,18,19,20,21,22,23,24,25,26,27,28])+12) #12 deg bias added for India

def IAQI_breeze(co2,voc,ht_idx):
    c1=co2_idx(co2)
    c2=voc_idx(voc)
    return max([c1,c2,ht_idx])

def TRH_idx(temp,hum):
    row=np.clip(round(hum)%10,1,9)
    col=np.clip(round(temp),16+12,28+12) #+12 deg due to india temp
    return TempHum_mat.loc[row,col]

def Ico2(Cco2):
    return (70*np.log(Cco2/(CO2_LEVEL+1e-7)))

def Ivoc(Cvoc):
    return (100*np.log(Cvoc/(VOC_LEVEL+1e-7)))

def Ipm2_5(Cpm2_5):
    return (85*np.log(Cpm2_5/(PMS2_5_LEVEL+1e-7)))

def Ipm10(Cpm10):
    return (85*np.log(Cpm10/(PMS10_LEVEL+1e-7)))

def compute_min_max_rate_of_change(d,COLUMN,pen=10): 
    # pen=10 #10 works best
    # COLUMN='VoC'
    cpd=rpt.Pelt(model='rbf',min_size=1*SEC_MULTIPLIER)
    dd=d[[COLUMN]]
    bkps=cpd.fit_predict(dd,pen)[:-1] #determine change points
    if len(bkps)==0:
        return 0,0 #no change detected
    grads=np.gradient(dd[COLUMN])
    bk_grds=[]
    for bk in bkps:
        lower=np.clip(bk-GRAD_AVG_WIN,0,grads.shape[0]) #setting lower to be 0
        upper=np.clip(bk+GRAD_AVG_WIN,0,grads.shape[0]) #setting upper to be maxlen
        bk_grds.append(grads[np.arange(lower,upper)].mean()) #get avg grad in the change points +- 15 window
    return min(bk_grds),max(bk_grds) #send min and max grad

def get_features(d):
    index=[]
    value=[]
    for c in d.columns:
        peaks=scipy.signal.find_peaks(d[c],height=MIN_PEAK_LVLS[c])[0]; peak_count=len(peaks)
        peak_dur=scipy.signal.peak_widths(d[c],peaks)[0].sum()
        long_stay=(d[c]>MIN_PEAK_LVLS[c]).sum()
        min_grad,max_grad=compute_min_max_rate_of_change(d,c)
        index.extend([f'{c}_avg',f'{c}_min',f'{c}_max',f'{c}_std',
                      f'{c}_roc_min',f'{c}_roc_max',f'{c}_pc',f'{c}_pd',f'{c}_lg_stay'])
        value.extend([d[c].mean(),d[c].min(),d[c].max(),d[c].std(),min_grad,max_grad,peak_count,peak_dur,long_stay])
    #computing IAQI like values
    index.extend(['I_co2','I_voc','I_pm2_5','I_pm10','IAQI'])
    indidual_idx=[Ico2(d['CO2'].mean()),Ivoc(d['VoC'].mean()),Ipm2_5(d['PMS2_5'].mean()),Ipm10(d['PMS10'].mean())]
    iaqi=max(indidual_idx)
    value.extend(indidual_idx+[iaqi])
    #Breeze AQIs
    ht_idx=TRH_idx(round(d['T'].mean()),round(d['H'].mean()))
    baqi=IAQI_breeze(round(d['CO2'].mean()),round(d['VoC'].mean()),ht_idx)
    index.extend(['HT_idx','BAQI'])
    value.extend([ht_idx,baqi])
    return pd.Series(value,index)

def read_feat(fname):
    df=read_data(fname,COLUMNS,down_to_10=DOWN_to_10)
    index=[]
    stats=[]
    for d in df.rolling(WINDOW):
        if d.shape[0]<WINDOW:
            continue
        stats.append(get_features(d))
        index.append(d.index[-1])
    df_feat=pd.DataFrame(stats,index=index)
    return df_feat

def process_feat_for(fname,parent_dir):
    name='_'.join(fname.split("/")[-2:])
    if (not os.path.exists(f"{parent_dir}/{name}")) or OVER_WRITE:
        df=read_feat(fname)
        df.to_csv(f"{parent_dir}/{name}")
    else:
        print("Skipping",fname)