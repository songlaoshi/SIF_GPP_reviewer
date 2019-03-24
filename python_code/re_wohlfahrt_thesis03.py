#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: re_wohlfahrt_thesis03.py
@time: 2019/3/5 15:59
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


def func(x, a, b,c):
    return a * x**b + c

def func1(x,a,b,c):
    return a*x*x+b*x+c

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
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = data.parse(0)
# 选出diffuse fraction >0.55的数据
# daymean=daymean[daymean['CI']>0.55]
# 提取用于分析的数据
daymean=pd.concat([daymean['doy'],daymean['PRI'],daymean['MTVI2'],daymean['CIgreen']
                      ,daymean['SFM'],daymean['GPP'],daymean['PAR'],
                   daymean['SIFyieldgndvi'],daymean['LUEgndvi'],daymean['CI']],axis=1)
# daymean=daymean.dropna()
daymean['psify']=daymean['SFM']/daymean['PAR']
daymean['plue']=daymean['GPP']/daymean['PAR']
idx=daymean['plue']>0.1
daymean.loc[idx,'plue']=np.nan

# daymean['psify']=daymean['SIFyieldgndvi']
# daymean['plue']=daymean['LUEgndvi']


vege = daymean[daymean['doy'] <= a2]
repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] < a3+1)]
ripen = daymean[daymean['doy'] > a3]

# ## figure01
# fig,axs=plt.subplots(1,1,figsize=(6,6))
#
# axs.scatter(vege['plue'],vege['psify'],edgecolors='r',facecolors='',marker='.')
# axs.scatter(repro['plue'],repro['psify'],edgecolors='k',facecolors='',marker='.')
# axs.scatter(ripen['plue'],ripen['psify'],edgecolors='b',facecolors='',marker='.')
# axs.set_ylim([-0.0005,0.002])
# axs.set_xlabel('plue [-]')
# axs.set_ylabel('psify [-]')
# axs.yaxis.set_major_formatter(fromatter)
#
# ## figure02
# fig,axs=plt.subplots(3,3,figsize=(14,10))
# plt.subplots_adjust(wspace=0.26)
# axs[0,0].scatter(vege['MTVI2'],vege['psify'],edgecolors='r',facecolors='',marker='.')
# axs[0,0].scatter(repro['MTVI2'],repro['psify'],edgecolors='k',facecolors='',marker='.')
# axs[0,0].scatter(ripen['MTVI2'],ripen['psify'],edgecolors='b',facecolors='',marker='.')
# axs[0,0].set_xlabel('MTVI2 [-]')
# axs[0,0].set_ylabel('psify [-]')
# axs[0,0].set_ylim([-0.001,0.002])
# axs[0,0].yaxis.set_major_formatter(fromatter)
#
# axs[0,1].scatter(vege['MTVI2'],vege['plue'],edgecolors='r',facecolors='',marker='.')
# axs[0,1].scatter(repro['MTVI2'],repro['plue'],edgecolors='k',facecolors='',marker='.')
# axs[0,1].scatter(ripen['MTVI2'],ripen['plue'],edgecolors='b',facecolors='',marker='.')
# axs[0,1].set_xlabel('MTVI2 [-]')
# axs[0,1].set_ylabel('plue [-]')
#
# axs[0,2].scatter(vege['MTVI2'],vege['PRI'],edgecolors='r',facecolors='',marker='.')
# axs[0,2].scatter(repro['MTVI2'],repro['PRI'],edgecolors='k',facecolors='',marker='.')
# axs[0,2].scatter(ripen['MTVI2'],ripen['PRI'],edgecolors='b',facecolors='',marker='.')
# axs[0,2].set_xlabel('MTVI2 [-]')
# axs[0,2].set_ylabel('PRI [-]')
# axs[0,2].yaxis.set_major_formatter(fromatter)
#
# axs[1,0].scatter(vege['CIgreen'],vege['psify'],edgecolors='r',facecolors='',marker='.')
# axs[1,0].scatter(repro['CIgreen'],repro['psify'],edgecolors='k',facecolors='',marker='.')
# axs[1,0].scatter(ripen['CIgreen'],ripen['psify'],edgecolors='b',facecolors='',marker='.')
# axs[1,0].set_xlabel('CIgreen [-]')
# axs[1,0].set_ylabel('psify [-]')
# axs[1,0].set_ylim([-0.001,0.002])
# axs[1,0].yaxis.set_major_formatter(fromatter)
#
# axs[1,1].scatter(vege['CIgreen'],vege['plue'],edgecolors='r',facecolors='',marker='.')
# axs[1,1].scatter(repro['CIgreen'],repro['plue'],edgecolors='k',facecolors='',marker='.')
# axs[1,1].scatter(ripen['CIgreen'],ripen['plue'],edgecolors='b',facecolors='',marker='.')
# axs[1,1].set_xlabel('CIgreen [-]')
# axs[1,1].set_ylabel('plue [-]')
#
# axs[1,2].scatter(vege['CIgreen'],vege['PRI'],edgecolors='r',facecolors='',marker='.')
# axs[1,2].scatter(repro['CIgreen'],repro['PRI'],edgecolors='k',facecolors='',marker='.')
# axs[1,2].scatter(ripen['CIgreen'],ripen['PRI'],edgecolors='b',facecolors='',marker='.')
# axs[1,2].set_xlabel('CIgreen [-]')
# axs[1,2].set_ylabel('PRI [-]')
# axs[1,2].yaxis.set_major_formatter(fromatter)
#
# axs[2,0].scatter(vege['CI'],vege['psify'],edgecolors='r',facecolors='',marker='.')
# axs[2,0].scatter(repro['CI'],repro['psify'],edgecolors='k',facecolors='',marker='.')
# axs[2,0].scatter(ripen['CI'],ripen['psify'],edgecolors='b',facecolors='',marker='.')
# axs[2,0].set_xlabel('CI [-]')
# axs[2,0].set_ylabel('psify [-]')
# axs[2,0].set_ylim([-0.001,0.002])
# axs[2,0].yaxis.set_major_formatter(fromatter)
#
# axs[2,1].scatter(vege['CI'],vege['plue'],edgecolors='r',facecolors='',marker='.')
# axs[2,1].scatter(repro['CI'],repro['plue'],edgecolors='k',facecolors='',marker='.')
# axs[2,1].scatter(ripen['CI'],ripen['plue'],edgecolors='b',facecolors='',marker='.')
# axs[2,1].set_xlabel('CI [-]')
# axs[2,1].set_ylabel('plue [-]')
#
# axs[2,2].scatter(vege['CI'],vege['PRI'],edgecolors='r',facecolors='',marker='.')
# axs[2,2].scatter(repro['CI'],repro['PRI'],edgecolors='k',facecolors='',marker='.')
# axs[2,2].scatter(ripen['CI'],ripen['PRI'],edgecolors='b',facecolors='',marker='.')
# axs[2,2].set_xlabel('CI [-]')
# axs[2,2].set_ylabel('PRI [-]')
# axs[2,2].yaxis.set_major_formatter(fromatter)

## 拟合曲线
linreg=LinearRegression()

# fig,axs=plt.subplots(3,3,figsize=(14,10))
# plt.subplots_adjust(wspace=0.26)
#---------------psify--------------------
data=pd.concat([daymean['psify'],daymean['plue'],daymean['PRI'],
                daymean['MTVI2'],daymean['CIgreen'],daymean['CI']],axis=1)
data=data.dropna()
x=data['MTVI2'].values.reshape(-1,1)
y=data['psify']
a,b,r2score,pred1=get_a_b_r2score(x,y)
print(r2score,a,b)
psify_sub=y-pred1
# r,p=get_pearsonr(data['MTVI2'],psify_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[0,0].scatter(data['MTVI2'],psify_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[0,0].set_ylim(-0.0025,0.001)
# axs[0,0].yaxis.set_major_formatter(fromatter)
# axs[0,0].set_ylabel('rpsify [-]')
# axs[0,0].set_xlabel('MTVI2 [-]')
# axs[0,0].legend()
# r,p=get_pearsonr(data['CIgreen'],psify_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[1,0].scatter(data['CIgreen'],psify_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[1,0].set_ylim(-0.0025,0.001)
# axs[1,0].yaxis.set_major_formatter(fromatter)
# axs[1,0].set_ylabel('rpsify [-]')
# axs[1,0].set_xlabel('CIgreen [-]')
# axs[1,0].legend()
# r,p=get_pearsonr(data['CI'],psify_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[2,0].scatter(data['CI'],psify_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[2,0].set_ylim(-0.0025,0.001)
# axs[2,0].yaxis.set_major_formatter(fromatter)
# axs[2,0].set_ylabel('rpsify [-]')
# axs[2,0].set_xlabel('CI [-]')
# axs[2,0].legend()
#---------------plue--------------------
data=data.dropna()
x=data['MTVI2'].values.reshape(-1,1)
y=data['plue']
a,b,r2score,pred1=get_a_b_r2score(x,y)
print(r2score,a,b)
plue_sub=y-pred1
# r,p=get_pearsonr(data['MTVI2'],plue_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[0,1].scatter(data['MTVI2'],plue_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[0,1].yaxis.set_major_formatter(fromatter)
# axs[0,1].set_ylabel('rplue [-]')
# axs[0,1].set_xlabel('MTVI2 [-]')
# axs[0,1].legend()
# r,p=get_pearsonr(data['CIgreen'],plue_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[1,1].scatter(data['CIgreen'],plue_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[1,1].yaxis.set_major_formatter(fromatter)
# axs[1,1].set_ylabel('rplue [-]')
# axs[1,1].set_xlabel('CIgreen [-]')
# axs[1,1].legend()
# r,p=get_pearsonr(data['CI'],plue_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[2,1].scatter(data['CI'],plue_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[2,1].yaxis.set_major_formatter(fromatter)
# axs[2,1].set_ylabel('rplue [-]')
# axs[2,1].set_xlabel('CI [-]')
# axs[2,1].legend()
#---------------pri--------------------
data=data.dropna()
x=data['MTVI2'].values.reshape(-1,1)
y=data['PRI']
a,b,r2score,pred1=get_a_b_r2score(x,y)
print(r2score,a,b)
pri_sub=y-pred1
# r,p=get_pearsonr(data['MTVI2'],pri_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[0,2].scatter(data['MTVI2'],pri_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[0,2].yaxis.set_major_formatter(fromatter)
# axs[0,2].set_ylabel('rpri [-]')
# axs[0,2].set_xlabel('MTVI2 [-]')
# axs[0,2].legend()
# r,p=get_pearsonr(data['CIgreen'],pri_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[1,2].scatter(data['CIgreen'],pri_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[1,2].yaxis.set_major_formatter(fromatter)
# axs[1,2].set_ylabel('rpri [-]')
# axs[1,2].set_xlabel('CIgreen [-]')
# axs[1,2].legend()
# r,p=get_pearsonr(data['CI'],pri_sub)
# label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
# axs[2,2].scatter(data['CI'],pri_sub,edgecolors='k'
#                  ,facecolors='',marker='.',label=label)
# axs[2,2].yaxis.set_major_formatter(fromatter)
# axs[2,2].set_ylabel('rpri [-]')
# axs[2,2].set_xlabel('CI [-]')
# axs[2,2].legend()

## rpsify,rplue,rpri之间的关系
fig,axs=plt.subplots(3,3,figsize=(14,10))
plt.subplots_adjust(wspace=0.26)

r,p=get_pearsonr(data['plue'],data['psify'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,0].scatter(data['plue'],data['psify'],edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[0,0].yaxis.set_major_formatter(fromatter)
axs[0,0].set_ylim(-0.0005,0.002)
axs[0,0].set_ylabel('psify [-]')
axs[0,0].set_xlabel('plue [-]')
axs[0,0].legend()

r,p=get_pearsonr(data['plue'],data['PRI'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,1].scatter(data['plue'],data['PRI'],edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[0,1].yaxis.set_major_formatter(fromatter)
axs[0,1].set_ylabel('pri [-]')
axs[0,1].set_xlabel('plue [-]')
axs[0,1].legend()

r,p=get_pearsonr(data['PRI'],data['psify'])
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[0,2].scatter(data['PRI'],data['psify'],edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[0,2].yaxis.set_major_formatter(fromatter)
axs[0,2].set_ylim(-0.0005,0.002)
axs[0,2].set_ylabel('psify [-]')
axs[0,2].set_xlabel('pri [-]')
axs[0,2].legend()

r,p=get_pearsonr(data['plue'],psify_sub)
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[1,0].scatter(data['plue'],psify_sub,edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[1,0].yaxis.set_major_formatter(fromatter)
axs[1,0].set_ylim(-0.001,0.002)
axs[1,0].set_ylabel('rpsify [-]')
axs[1,0].set_xlabel('plue [-]')
axs[1,0].legend()

r,p=get_pearsonr(data['plue'],pri_sub)
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[1,1].scatter(data['plue'],pri_sub,edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[1,1].yaxis.set_major_formatter(fromatter)
axs[1,1].set_ylabel('rpri [-]')
axs[1,1].set_xlabel('plue [-]')
axs[1,1].legend()

r,p=get_pearsonr(plue_sub,psify_sub)
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,0].scatter(plue_sub,psify_sub,edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[2,0].yaxis.set_major_formatter(fromatter)
axs[2,0].set_ylim(-0.001,0.002)
axs[2,0].set_ylabel('rpsify [-]')
axs[2,0].set_xlabel('rplue [-]')
axs[2,0].legend()

r,p=get_pearsonr(plue_sub,pri_sub)
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,1].scatter(plue_sub,pri_sub,edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[2,1].yaxis.set_major_formatter(fromatter)
axs[2,1].set_ylabel('rpri [-]')
axs[2,1].set_xlabel('rplue [-]')
axs[2,1].legend()

r,p=get_pearsonr(pri_sub,psify_sub)
label='r= '+'%.2f'%r+funcs_lzh.funcstar(p)
axs[2,2].scatter(pri_sub,psify_sub,edgecolors='k'
                 ,facecolors='',marker='.',label=label)
axs[2,2].yaxis.set_major_formatter(fromatter)
axs[2,2].set_ylim(-0.001,0.002)
axs[2,2].set_ylabel('rpsify [-]')
axs[2,2].set_xlabel('rpri [-]')
axs[2,2].legend()

plt.show()