#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: re_wohlfahrt_thesis06.py
@time: 2019/3/7 15:24
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
# from sklearn import preprocessing
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

def MaxMinNormalization(x,max,min):
    x=(x-min)/(max-min)
    return x

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
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = daymean.parse(0)

# 选出diffuse fraction >0.55的数据
# daymean=daymean[daymean['CI']>0.55]
daymean=pd.concat([daymean['doy'],daymean['PRI'],daymean['MTVI2'],daymean['greenNDVI']
                      ,daymean['SFM'],daymean['GPP'],daymean['PAR'],daymean['CIgreen']
                      ,daymean['CI'],daymean['VPD'],daymean['Ta']],axis=1)
daymean['APARgreen']=daymean['greenNDVI']*daymean['PAR']
print(daymean.shape)
# daymean=daymean.dropna()
daymean.index=range(len(daymean))
print(daymean.shape)
# 计算NPQ和phi_N （ref: Alonso et al., 2017.）
a=0.72906363
b=-16.781348
c=8.9183602*10**(-4) # unit: m2*s/umol
daymean['NPQ']=a+b*daymean['PRI']+c*daymean['APARgreen']
daymean['phi_F']=daymean['SFM']/daymean['APARgreen']*3.27*10**(-4)*np.pi*487
daymean['phi_F_tr']=daymean['SFM']/daymean['APARgreen']
daymean['phi_P']=daymean['GPP']/daymean['APARgreen']
daymean['phi_N']=daymean['NPQ']/daymean['APARgreen']
# ------删除phi_N异常值
daymean.loc[daymean['phi_N']>0.05,'phi_N']=np.nan
# ------删除LUE异常值
daymean.loc[daymean['phi_P']>0.1,'phi_P']=np.nan

# 计算phi_F,phi_P,phi_N的比例
daymean['frac_phi_F']=daymean['phi_F']
daymean['frac_phi_P']=daymean['phi_F']
daymean['frac_phi_N']=daymean['phi_F']
for i in range(daymean.shape[0]):
    temp=np.nansum([daymean.loc[i,'phi_F']
                       ,daymean.loc[i,'phi_P'],daymean.loc[i,'phi_N']])
    daymean.loc[i,'frac_phi_F']=daymean.loc[i,'phi_F']/temp
    daymean.loc[i, 'frac_phi_P'] = daymean.loc[i, 'phi_P'] / temp
    daymean.loc[i,'frac_phi_N']=daymean.loc[i,'phi_N']/temp

# daymean['phi_D']=1-daymean['phi_F']-daymean['phi_P']-daymean['phi_N']

daymean['nor_phi_F']=MaxMinNormalization(
    daymean['phi_F'],np.max(daymean['phi_F']),np.min(daymean['phi_F']))
daymean['nor_phi_P']=MaxMinNormalization(
    daymean['phi_P'],np.max(daymean['phi_P']),np.min(daymean['phi_P']))
daymean['nor_phi_N']=MaxMinNormalization(
    daymean['phi_N'],np.max(daymean['phi_N']),np.min(daymean['phi_N']))
# daymean['nor_phi_D']=1-daymean['nor_phi_F']-daymean['nor_phi_P']-daymean['nor_phi_N']

# plt.scatter(daymean['doy'],frac_phi_F,marker='.',color='r')
# plt.scatter(daymean['doy'],frac_phi_P,marker='.',color='g')
# plt.scatter(daymean['doy'],frac_phi_N,marker='.',color='b')
# plt.scatter(daymean['doy'],daymean['phi_D'],marker='.',color='k')

# # 提取用于分析NPQ的数据
doy=daymean['doy']
data_repro=daymean.loc[(doy>=a2) & (doy<a3)]
# # figure01=未去除冠层效应（LAI+Cab）的phi_P,phi_F,phi_N柱状图
# fracdata=pd.concat([data_repro['doy'],data_repro['frac_phi_P'],data_repro['frac_phi_F']
#                        ,data_repro['frac_phi_N']],axis=1)
# fracdata.index=range(len(fracdata))
# yoffset=np.zeros(len(fracdata))
# fig,axs=plt.subplots(1,1,figsize=(14,3))
# colors=['green','r','b']
# labels=['phi_P','phi_F','phi_N']
# x=np.arange((a3-a2)*15)+1
# for row in range(3):
#     # print(fracdata.iloc[:,row+1])
#     axs.bar(x,fracdata.iloc[:,row+1],bottom=yoffset,
#             width=1,facecolor=colors[row],label=labels[row])
#     yoffset=yoffset+fracdata.iloc[:,row+1]
# axs.set_xlabel('DOY')
# axs.set_ylabel('fraction [-]')
# axs.legend()
#
# ------------------------------------------------------
daymean=daymean.dropna()
vege = daymean[daymean['doy'] <= a2]
repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] < a3+1)]
ripen = daymean[daymean['doy'] > a3]

# figure03
fig,axs=plt.subplots(4,3,figsize=(14,10))
plt.subplots_adjust(wspace=0.26,hspace=0.5,bottom=0.07,top=0.93)
r,p=get_pearsonr(daymean['MTVI2'],daymean['phi_F_tr'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,0].set_title(label)
axs[0,0].scatter(vege['MTVI2'],vege['phi_F_tr'],edgecolors='r',facecolors='',marker='.',label='vege')
axs[0,0].scatter(repro['MTVI2'],repro['phi_F_tr'],edgecolors='k',facecolors='',marker='.',label='repro')
axs[0,0].scatter(ripen['MTVI2'],ripen['phi_F_tr'],edgecolors='b',facecolors='',marker='.',label='ripen')
axs[0,0].set_xlabel('MTVI2 [-]')
axs[0,0].set_ylabel('phi_F [-]')
axs[0,0].legend()
axs[0,0].set_ylim([-0.001,0.003])
axs[0,0].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['MTVI2'],daymean['phi_P'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,1].set_title(label)
axs[0,1].scatter(vege['MTVI2'],vege['phi_P'],edgecolors='r',facecolors='',marker='.')
axs[0,1].scatter(repro['MTVI2'],repro['phi_P'],edgecolors='k',facecolors='',marker='.')
axs[0,1].scatter(ripen['MTVI2'],ripen['phi_P'],edgecolors='b',facecolors='',marker='.')
axs[0,1].set_xlabel('MTVI2 [-]')
axs[0,1].set_ylabel('phi_P [-]')

r,p=get_pearsonr(repro['MTVI2'],repro['phi_N'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,2].set_title(label)
# axs[0,2].scatter(vege['MTVI2'],vege['phi_N'],edgecolors='r',facecolors='',marker='.')
axs[0,2].scatter(repro['MTVI2'],repro['phi_N'],edgecolors='k',facecolors='',marker='.')
# axs[0,2].scatter(ripen['MTVI2'],ripen['phi_N'],edgecolors='b',facecolors='',marker='.')
axs[0,2].set_xlabel('MTVI2 [-]')
axs[0,2].set_ylabel('phi_N [-]')
axs[0,2].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['VPD'],daymean['phi_F_tr'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[1,0].set_title(label)
axs[1,0].scatter(vege['VPD'],vege['phi_F_tr'],edgecolors='r',facecolors='',marker='.')
axs[1,0].scatter(repro['VPD'],repro['phi_F_tr'],edgecolors='k',facecolors='',marker='.')
axs[1,0].scatter(ripen['VPD'],ripen['phi_F_tr'],edgecolors='b',facecolors='',marker='.')
axs[1,0].set_xlabel('VPD [kPa]')
axs[1,0].set_ylabel('phi_F [-]')
axs[1,0].set_ylim([-0.001,0.003])
axs[1,0].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['VPD'],daymean['phi_P'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[1,1].set_title(label)
axs[1,1].scatter(vege['VPD'],vege['phi_P'],edgecolors='r',facecolors='',marker='.')
axs[1,1].scatter(repro['VPD'],repro['phi_P'],edgecolors='k',facecolors='',marker='.')
axs[1,1].scatter(ripen['VPD'],ripen['phi_P'],edgecolors='b',facecolors='',marker='.')
axs[1,1].set_xlabel('VPD [kPa]')
axs[1,1].set_ylabel('phi_P [-]')

r,p=get_pearsonr(repro['VPD'],repro['phi_N'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[1,2].set_title(label)
# axs[1,2].scatter(vege['VPD'],vege['phi_N'],edgecolors='r',facecolors='',marker='.')
axs[1,2].scatter(repro['VPD'],repro['phi_N'],edgecolors='k',facecolors='',marker='.')
# axs[1,2].scatter(ripen['VPD'],ripen['phi_N'],edgecolors='b',facecolors='',marker='.')
axs[1,2].set_xlabel('VPD [kPa]')
axs[1,2].set_ylabel('phi_N [-]')
axs[1,2].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['CI'],daymean['phi_F_tr'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,0].set_title(label)
axs[2,0].scatter(vege['CI'],vege['phi_F_tr'],edgecolors='r',facecolors='',marker='.')
axs[2,0].scatter(repro['CI'],repro['phi_F_tr'],edgecolors='k',facecolors='',marker='.')
axs[2,0].scatter(ripen['CI'],ripen['phi_F_tr'],edgecolors='b',facecolors='',marker='.')
axs[2,0].set_xlabel('CI [-]')
axs[2,0].set_ylabel('phi_F [-]')
axs[2,0].set_ylim([-0.001,0.003])
axs[2,0].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['CI'],daymean['phi_P'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,1].set_title(label)
axs[2,1].scatter(vege['CI'],vege['phi_P'],edgecolors='r',facecolors='',marker='.')
axs[2,1].scatter(repro['CI'],repro['phi_P'],edgecolors='k',facecolors='',marker='.')
axs[2,1].scatter(ripen['CI'],ripen['phi_P'],edgecolors='b',facecolors='',marker='.')
axs[2,1].set_xlabel('CI [-]')
axs[2,1].set_ylabel('phi_P [-]')

r,p=get_pearsonr(repro['CI'],repro['phi_N'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,2].set_title(label)
# axs[2,2].scatter(vege['CI'],vege['phi_N'],edgecolors='r',facecolors='',marker='.')
axs[2,2].scatter(repro['CI'],repro['phi_N'],edgecolors='k',facecolors='',marker='.')
# axs[2,2].scatter(ripen['CI'],ripen['phi_N'],edgecolors='b',facecolors='',marker='.')
axs[2,2].set_xlabel('CI [-]')
axs[2,2].set_ylabel('phi_N [-]')
axs[2,2].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['Ta'],daymean['phi_F_tr'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[3,0].set_title(label)
axs[3,0].scatter(vege['Ta'],vege['phi_F_tr'],edgecolors='r',facecolors='',marker='.')
axs[3,0].scatter(repro['Ta'],repro['phi_F_tr'],edgecolors='k',facecolors='',marker='.')
axs[3,0].scatter(ripen['Ta'],ripen['phi_F_tr'],edgecolors='b',facecolors='',marker='.')
axs[3,0].set_xlabel('Ta [degree]')
axs[3,0].set_ylabel('phi_F [-]')
axs[3,0].set_ylim([-0.001,0.003])
axs[3,0].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['Ta'],daymean['phi_P'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[3,1].set_title(label)
axs[3,1].scatter(vege['Ta'],vege['phi_P'],edgecolors='r',facecolors='',marker='.')
axs[3,1].scatter(repro['Ta'],repro['phi_P'],edgecolors='k',facecolors='',marker='.')
axs[3,1].scatter(ripen['Ta'],ripen['phi_P'],edgecolors='b',facecolors='',marker='.')
axs[3,1].set_xlabel('Ta [degree]')
axs[3,1].set_ylabel('phi_P [-]')

r,p=get_pearsonr(repro['Ta'],repro['phi_N'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[3,2].set_title(label)
# axs[3,2].scatter(vege['Ta'],vege['phi_N'],edgecolors='r',facecolors='',marker='.')
axs[3,2].scatter(repro['Ta'],repro['phi_N'],edgecolors='k',facecolors='',marker='.')
# axs[3,2].scatter(ripen['Ta'],ripen['phi_N'],edgecolors='b',facecolors='',marker='.')
axs[3,2].set_xlabel('Ta [degree]')
axs[3,2].set_ylabel('phi_N [-]')
axs[3,2].yaxis.set_major_formatter(fromatter)

plt.show()