# -*- coding: utf-8 -*-
#/usr/bin/env python

"""
Created on Fri Jul 21 16:11:58 2017

@author: muramatsu
"""

import argparse
import numpy as np
import pandas as pd
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns


parser = argparse.ArgumentParser(description="help messages")
group1 = parser.add_argument_group('Main options')
group2 = parser.add_argument_group('additional options')
group1.add_argument("-freq", dest="freq", default="5T", type=str, help="time frequency of data")
group1.add_argument("-periods", dest="prd", default=288, type=int, help="periods of data(data points)")
group1.add_argument("-anomaNum", dest="amN", default=10, type=int, help="anomaly points")
group1.add_argument("-anomaDirect", dest="amD", choices=["pos","neg"], default="pos", type=str, help="anomaly direction")
group1.add_argument("-resFreq", dest="rsF", default="5T", type=str, help="resampling frequency")
group1.add_argument("-in", dest="in", type=str, help="input csv")
group1.add_argument("-out", dest="out", type=str, help="output csv")



group2.add_argument("-resHow", dest="rsH", type=str, default="mean", choices=["sum","mean","median","max","min","last","first"],help="how to resampling")
group2.add_argument("-missHow", dest="msH",type=str, default="interpolate", help="how to cover missing values")  
group2.add_argument("-input_header",dest="inH", type=int, default=0, choices=[0,-1], help="input header option")
args=parser.parse_args()


def plot_func(df):
    df.plot()
    
def make_data(freq,periods):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    idx=pd.date_range(now,freq=freq,periods=periods)
    x = np.linspace(0, 100, num=periods)
    np.random.seed(1234)
    pi2 = 2.*np.pi
    value = 1.0*np.sin(0.1*pi2*x) + 1.0*np.cos(1.*pi2*x) + 0.5*np.random.randn(x.size)
    
    value2 = 2.0*np.sin(0.1*pi2*x) + 3.0*np.cos(1.*pi2*x) + 0.6*np.random.randn(x.size)
    
    df=pd.DataFrame({"val":value,"val2":value2},index=idx)
    return df
    
def make_anomaly(df, periods, num, direction):
    start = np.random.randint(periods)
    end = start + num
    print df.iloc[start], df.iloc[end]
    if direction == "pos":
        df["val"].iloc[start:end] = float(df.max()) * 10
    elif direction == "neg":
        if float(df.min()) < 0:
            df["val"].iloc[start:end] = float(df.min()) * 10
        else:
            df["val"].iloc[start:end] = float(df.min()) / 10
    return df
#df = make_anomaly(df, 288, 20, "neg")
#plot_func(df)
    
def resample_time(df, freq, how="mean"):
    if how == "last":
        df = df.resample(freq).last()
    elif how == "first":
        df = df.resample(freq).first()
    elif how == "sum":
        df = df.resample(freq).sum()
    elif how == "median":
        df = df.resample(freq).median()
    elif how == "max":
        df = df.resample(freq).max()
    elif how == "min":
        df = df.resample(freq).min()        
    else:#mean
        df = df.resample(freq).mean()

    return df
#df=resample_time(df,"10T","mean")
#plot_func(df)

def missing_value(df, how="interpolate"):
    #indexer=np.random.randint(4,size=30)==1
    #df.loc[indexer]=np.nan
    if how == "interpolate":
        df=df.interpolate()
    elif how == "drop":
        df=df.dropna()
    else:
        df=df.fillna(df.mean())
        #bfill : backward
        #ffill : forward
    return df
#df = missing_value(df,"interpolate")

def autocorr(df):
    lags = range(len(df)//2) 
    corrs = [df.autocorr(lag) for lag in lags]
    return lags, corrs

def plot_autocorr(df):
    lags, corrs = autocorr(df.val)
    plt.xlabel('lags')
    plt.ylabel('autocorr val')
    plt.bar(lags, corrs)

def slide_window(df, num):
    df.shift(num)
    return df


def file_reader(csv, header=0):
    df=pd.read_csv(csv,header=header)
    if df.isnull().any().sum() > 0:
        df = missing_value(df)
    return df
    
def file_writer(df, out_name):
    df.to_csv(out_name)


#def data_understand():
    

    
df=make_data("5t",288)
df.describe()
sns.pairplot(df)

