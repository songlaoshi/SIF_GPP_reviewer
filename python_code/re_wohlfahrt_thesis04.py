#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: re_wohlfahrt_thesis04.py
@time: 2019/3/5 21:26
'''


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
import math
import funcs_lzh
from scipy.stats.stats import pearsonr
from matplotlib import ticker

linreg=LinearRegression()

def get_a_b_r2score(x,y):
    reg = linreg.fit(x, y)
    a, b = linreg.coef_, linreg.intercept_
    pred = reg.predict(x)
    r2score = r2_score(y, pred)
    return a,b,r2score,pred

def get_pearsonr(x,y):
    r, p = pearsonr(x, y)  # 相关系数
    return r,p

# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 18}
font1={'family':'Times New Roman',
'weight':'normal',
'size':18,}
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize=18
# growth stage
a1 = 192
a2 = 205
a3 = 255
a4 = 283
# daymean
filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
data = pd.ExcelFile(
    filepath + '\\' + r'leaf data_top and canopy_20180311_corn.xlsx')
data = data.parse(0)
data=pd.concat([data['Canopy_SIF'],data['Canopy_GPP']
                   ,data['PAR'],data['LAI'],data['Cab'] # chl a+b(mg/cm2)
                ,data['SIFyield760']],axis=1)
data=data.dropna()
print(data)
data['psify']=data['Canopy_SIF']/data['PAR']
data['plue']=data['Canopy_GPP']/data['PAR']
data['leafsify']=data['SIFyield760']*1000

## fig
fig,axs=plt.subplots(2,4,figsize=(15,8))

r,p=get_pearsonr(data['plue'],data['psify'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,0].scatter(data['plue'],data['psify'],edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[0,0].yaxis.set_major_formatter(fromatter)
axs[0,0].set_ylabel('psify [-]')
axs[0,0].set_xlabel('plue [-]')
axs[0,0].legend()

plt.show()