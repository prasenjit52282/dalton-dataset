import numpy as np
import pandas as pd

#JCP (Development of indoor environmental quality index using a low-cost monitoring platform)
def Ico2(Cco2):
    return 100-(70*np.log(Cco2/415))

def Ivoc(Cvoc):
    return 100-(100*np.log(Cvoc/30))

def Ipm2_5(Cpm2_5):
    return 100-(85*np.log(Cpm2_5/10))

def IAQI_jcp(df):
    return pd.Series(np.min([Ico2(df.CO2),Ivoc(df.VoC),Ipm2_5(df.PMS2_5)],axis=0),index=df.index)

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
    elif 3301<=voc:
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


def TRH_idx(temp,hum):
    row=np.clip(round(hum)%10,1,9)
    col=np.clip(round(temp),16+12,28+12) #+12 deg due to india temp
    return TempHum_mat.loc[row,col]

def IAQI_breeze(df):
    c1=df.CO2.apply(co2_idx)
    c2=df.VoC.apply(voc_idx)
    c3=df[['T','H']].apply(lambda e:TRH_idx(*e),axis=1)
    return pd.Series(np.max([c1,c2,c3],axis=0),index=df.index)