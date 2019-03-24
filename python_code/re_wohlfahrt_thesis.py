#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-25 11:01:56
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

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

def func(x, a, b,c):
    return a * x**b + c

def func1(x,a,b,c):
    return a*x*x+b*x+c



# 科学计数法
# fromatter = ticker.ScalarFormatter(useMathText=True)
# fromatter.set_scientific(True)
# fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 18}
font1={'family':'Times New Roman',
'weight':'normal',
'size':18,}
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize=18

# daymean
filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
data = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = data.parse(0)
daymean=pd.concat([daymean['doy'],daymean['PRI'],daymean['MTVI2'],daymean['SFMSIFyield'],daymean['LUE']],axis=1)
daymean=daymean.dropna()
a1 = 192
a2 = 205
a3 = 255
a4 = 283

vege = daymean[daymean['doy'] <= a2]
repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] < a3+1)]
ripen = daymean[daymean['doy'] > a3]

reprosify=repro['SFMSIFyield']
repromtvi2=repro['MTVI2'].values
repropri=repro['PRI'].values
reprolue=repro['LUE']

# ## Section01-计算出sPRI和sFY760模型
# linreg = LinearRegression()
# plt.figure()
# plt.scatter(repromtvi2,repropri)
# popt,pcov=curve_fit(func,repromtvi2,repropri)
# temp=np.arange(np.min(repromtvi2)*0.9,np.max(repromtvi2)*1.1,0.02)
# pred_1=func(repromtvi2,popt[0],popt[1],popt[2])
# print(popt)
# r, p = pearsonr(repromtvi2, repropri) #相关系数
# r2 = np.square(r)
# print(r2)
# r2score=r2_score(repropri,pred_1) # 决定系数
# print(r2score)
#
# #------------------------------------------------
# # sPRI=0.089*MTVI2^2.8 -0.050, R2_score=0.65
# #------------------------------------------------
#
# # pred_2=0.1502*repromtvi2**2-0.0724*repromtvi2-0.0391
# # rmse1,rrmse1=funcs_lzh.get_rmse_rrmse(repropri,pred_1)
# # rmse2,rrmse2=funcs_lzh.get_rmse_rrmse(repropri,pred_2)
# # reg = linreg.fit(repromtvi2.reshape(-1,1),repropri)
# # a, b = linreg.coef_, linreg.intercept_
# # pred_3 = reg.predict(repromtvi2.reshape(-1,1))
# # rmse3,rrmse3=funcs_lzh.get_rmse_rrmse(repropri,pred_3)
# # print(rmse1,rmse2,rmse3)
# plt.plot(repromtvi2, pred_1, color='r', linewidth=2, label='')
# # plt.plot(repromtvi2, pred_2, color='g', linewidth=2, label='')
# # plt.plot(repromtvi2, pred_3, color='b', linewidth=2, label='')
#
# plt.figure()
# plt.scatter(repromtvi2,reprosify)
# reg = linreg.fit(repromtvi2.reshape(-1,1),reprosify)
# a, b = linreg.coef_, linreg.intercept_
# pred_3 = reg.predict(repromtvi2.reshape(-1,1))
# r, p = pearsonr(repromtvi2, reprosify) #相关系数，当用线性回归时，相关系数2=决定系数
# r2 = np.square(r)
# print(a,b)
# r2score=r2_score(reprosify,pred_3) #决定系数
# print(r2)
# print(r2score)
# plt.ylim([0,0.003])
# #------------------------------------------------
# # sFY760=0.0022*MTVI2-0.00034, R2_score=0.13
# #------------------------------------------------

## Section02-计算rPRI和rFY760，求与LUE的相关性
sPRI=0.089*repromtvi2**2.8 -0.050
sFY760=0.0022*repromtvi2-0.00034
rPRI=repropri-sPRI
rFY760=reprosify-sFY760

plt.scatter(reprolue,reprosify)
plt.ylim([0,0.003])
plt.show()