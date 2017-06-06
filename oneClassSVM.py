# -*- coding: utf-8 -*-
"""
Created on Mon Jun 05 21:33:29 2017

@author: kohei-mu
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from skopt import gp_minimize
from sklearn import svm
from skopt.plots import plot_convergence


df = pd.read_csv("indices_I101.csv",header=None)[1]
tmp =  np.array(df).reshape(-1, 1)

#function to calculate anomaly
def oneClass(nu,gamma):
    clf = svm.OneClassSVM(nu=nu,kernel="rbf",gamma=gamma)
    clf.fit(tmp)    
    ans = clf.predict(tmp)
    return ans
    
#function to optimize
def func(params):
    nu, gamma =params
    r = 0.01
    ret = oneClass(nu,gamma)
    anomaly_ratio = float(len(np.where(ret==-1)[0])) / len(ret)
    resi = abs(r - anomaly_ratio)
    return resi

#parameter bounds
dimensions  = [(0.001, 0.001),   
          (0.01,0.5)
]     

#minimize variance of change score
res_gp = gp_minimize(func, dimensions, n_calls=150, random_state=0,n_random_starts=50)

func_return = oneClass(res_gp.x[0], res_gp.x[1])
print(float(len(np.where(func_return==-1)[0])) / len(func_return))

retPan=pd.DataFrame(func_return)
result=pd.concat([df, retPan], axis=1)

#plot result
fig = plt.figure(figsize=(13, 7))
ax = fig.add_subplot(111)
ax.plot(df)
xIndex=np.where(func_return==-1)[0]
yIndex=df[xIndex]
plt.plot(xIndex, yIndex, 'o',color="r")
plt.show()

plot_convergence(res_gp)

resX = pd.DataFrame(res_gp.x_iters)
resFuncVals = pd.DataFrame(res_gp.func_vals)
resConcat = pd.concat([resX, resFuncVals], axis=1)


#______________________________________________________________
#get variables by random

import random
nu =  [random.uniform(0.01, 0.5) for x in range(0,100)]
gamma = [random.uniform(0.005, 0.005) for x in range(0,100)]
params = [[nu[x], gamma[x]] for x in range(0,100)]

def f(params):
    nu, gamma = params
    clf = svm.OneClassSVM(nu=nu,kernel="rbf",gamma=gamma)
    clf.fit(tmp)    
    ans = clf.predict(tmp)
    anomaly_ratio = float(len(np.where(ans==-1)[0])) / len(ans)
    return anomaly_ratio

ratios = [f(i) for i in params]
result = [[params[i], ratios[i]] for i in range(0,100)]   
resultSorted = sorted(result, key=lambda x: x[0][0])
