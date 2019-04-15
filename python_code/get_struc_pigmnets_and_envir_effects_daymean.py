#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_struc&pigments_and_envir_effects.py
@time: 2019/4/9 19:58
'''
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
# from sklearn import preprocessing
from scipy.optimize import curve_fit
import math
from mpl_toolkits.mplot3d import Axes3D
import funcs_lzh
from scipy.stats.stats import pearsonr
from matplotlib import ticker

linreg = LinearRegression()


def get_a_b_r2score(x, y):
    reg = linreg.fit(x, y)
    a, b = linreg.coef_, linreg.intercept_
    pred = reg.predict(x)
    r2score = r2_score(y, pred)
    return a, b, r2score, pred

def get_pearsonr(x, y):
    r, p = pearsonr(x, y)  # 相关系数
    return r, p

# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize = 14
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}

def plot_01(axs, x, y, c, xlabel, ylabel):
    r, p = get_pearsonr(x, y)
    p = axs.scatter(x, y, c=c, cmap='jet', marker='.', label='r= %.2f' % r + funcs_lzh.funcstar(p))
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)
    axs.legend()
    return p

def scatterplot(ax,x,y,c,xlim_range,ylim_range):
    r, p = get_pearsonr(x, y)
    label = 'r= %.2f' % r + funcs_lzh.funcstar(p)
    p=ax.scatter(x, y, c=c, vmin=0, vmax=1, cmap='jet', marker='o', label=label)
    ax.set_xlim(xlim_range)
    ax.set_ylim(ylim_range)
    return p

def scatterplot1(ax,x,y,xlim_range,ylim_range,color):
    r, p = get_pearsonr(x, y)
    label = 'r= %.2f' % r + funcs_lzh.funcstar(p)
    p=ax.scatter(x, y, marker='.', facecolor='',edgecolor=color,label=label)
    ax.set_xlim(xlim_range)
    ax.set_ylim(ylim_range)
    return p

# growth stage
a1 = 192.0
a2 = 205.0
a3 = 255.0
a4 = 283.0
parthred1 = 450.0
parthred2 = 700.0
cithred1 = 0.4
cithred2 = 0.6
ecithred1 = 0.6
ecithred2 = 0.8
# daymean
filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_daymean_sq2017corn_8-18_addSZA_norain.xlsx')
daymean=daymean.parse(0)
# 去掉SZA>60的数据
# daymean=daymean[daymean['SZA']<60]
# 选取晴天数据
daymean=daymean[daymean['CI']>0.5]
#
daymean = pd.concat([daymean['DOY'], daymean['hour'], daymean['MTVI2'], daymean['CIgreen'],daymean['EVI']
                        , daymean['rededgeNDVI'],daymean['greenNDVI'],daymean['SFMlinear'], daymean['GPP'], daymean['PAR'],daymean['CI']
                        , daymean['VPD'], daymean['Ta'], daymean['PRI'],daymean['CI']], axis=1)
daymean = daymean.dropna()


# 使用一个scaled的EVI当做fAPAR
# fAPARchl_evi = 1.29 * daymean['EVI'] - 0.16
daymean['apar'] = daymean['rededgeNDVI']* daymean['PAR']
# daymean['apar'] = (1.29 * daymean['EVI'] - 0.16 )* daymean['PAR']

# 计算ECI
daymean['scaled_APAR'] = funcs_lzh.MaxMinNormalization(daymean['apar'], np.max(daymean['apar']), np.min(daymean['apar']))
daymean['scaled_VPD'] = funcs_lzh.MaxMinNormalization(daymean['VPD'], np.max(daymean['VPD']), np.min(daymean['VPD']))
daymean['scaled_Ta'] = funcs_lzh.MaxMinNormalization(daymean['Ta'], np.max(daymean['Ta']), np.min(daymean['Ta']))
daymean['eci'] = daymean['scaled_APAR'] + daymean['scaled_VPD'] + daymean['scaled_Ta']
daymean['ECI'] = funcs_lzh.MaxMinNormalization(daymean['eci'], np.max(daymean['eci']), np.min(daymean['eci']))
# 计算光合和荧光效率
daymean['sify'] = daymean['SFMlinear']/daymean['apar']
daymean['lue'] = daymean['GPP']/daymean['apar']
# 去掉LUE异常值
daymean.loc[daymean['lue']>0.15,'lue']=np.nan
daymean=daymean.dropna()
# 去掉structural and pigment effects
meanMTVI2=np.mean(daymean['MTVI2'])
daymean['scaled_MTVI2']=daymean['MTVI2']/meanMTVI2

daymean['rsify']=daymean['sify']/daymean['scaled_MTVI2']

# x = daymean['MTVI2'].values.reshape(-1, 1)
# y = daymean['sify']
# a, b, r2score, pred1 = get_a_b_r2score(x, y)
# daymean['rsify'] = y - pred1

# 分阶段
vege = daymean[daymean['DOY'] <= a2]
repro = daymean[(daymean['DOY'] > a2) & (daymean['DOY'] <= a3)]
ripen = daymean[daymean['DOY'] > a3]

##################
fig, axs = plt.subplots(3, 4, figsize=(15, 12))
fig.subplots_adjust(left=0.07,right=0.85,hspace=0.3)

scatterplot(axs[0,0],vege['GPP'],vege['SFMlinear'],c=vege['ECI'],xlim_range=[0,100],ylim_range=[0,3])
scatterplot(axs[0,1],repro['GPP'],repro['SFMlinear'],c=repro['ECI'],xlim_range=[0,100],ylim_range=[0,3])
scatterplot(axs[0,2],ripen['GPP'],ripen['SFMlinear'],c=ripen['ECI'],xlim_range=[0,100],ylim_range=[0,3])
scatterplot(axs[0,3],daymean['GPP'],daymean['SFMlinear'],c=daymean['ECI'],xlim_range=[0,100],ylim_range=[0,3])

title=['vegetation stage','reproductive stage','ripening stage','whole season']
for i in range(4):
    axs[0,i].set_title(title[i],**title_font)
    axs[0,i].legend()
    axs[0,i].tick_params(labelsize=ticklabelsize)
    labels = axs[0,i].get_xticklabels() + axs[0,i].get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    axs[0,i].set_xlabel('GPP $[μmol CO_2/m^2/s]$',**axis_font)
    if i==0:
        axs[0,i].set_ylabel('SIF $[mW/m^2/nm/sr]$',**axis_font)

scatterplot(axs[1,0],vege['lue'],vege['sify'],c=vege['ECI'],xlim_range=[0,0.2],ylim_range=[0,0.003])
scatterplot(axs[1,1],repro['lue'],repro['sify'],c=repro['ECI'],xlim_range=[0,0.2],ylim_range=[0,0.003])
scatterplot(axs[1,2],ripen['lue'],ripen['sify'],c=ripen['ECI'],xlim_range=[0,0.2],ylim_range=[0,0.003])
p=scatterplot(axs[1,3],daymean['lue'],daymean['sify'],c=daymean['ECI'],xlim_range=[0,0.2],ylim_range=[0,0.003])

for i in range(4):
    axs[1,i].legend()
    axs[1,i].tick_params(labelsize=ticklabelsize)
    labels = axs[1,i].get_xticklabels() + axs[1,i].get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    axs[1,i].set_xlabel('LUE',**axis_font)
    axs[1,i].yaxis.set_major_formatter(fromatter)
    if i==0:
        axs[1,i].set_ylabel('SIF$_{yield}$',**axis_font)

cbar_ax = fig.add_axes([0.87, 0.15, 0.01, 0.7])
cbar1=fig.colorbar(p, cax=cbar_ax)
cbar1.set_label('ECI [-]',rotation=90, **axis_font)
cbar1.ax.set_yticklabels(['0','0.2','0.4','0.6','0.8','1'],**axis_font)

axs[2,0].hist(vege['MTVI2'],bins=20,normed=0,facecolor='k')
axs[2,1].hist(repro['MTVI2'],bins=20,normed=0,facecolor='k')
axs[2,2].hist(ripen['MTVI2'],bins=20,normed=0,facecolor='k')
axs[2,3].hist(daymean['MTVI2'],bins=20,normed=0,facecolor='k')

for i in range(4):
    axs[2,i].set_xlim([0,1])
    axs[2, i].tick_params(labelsize=ticklabelsize)
    labels = axs[2, i].get_xticklabels() + axs[2, i].get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    axs[2, i].set_xlabel('MTVI2', **axis_font)
    if i == 0:
        axs[2, i].set_ylabel('frequency', **axis_font)


## 消去structural and pigments effects
fig, axs = plt.subplots(1, 4, figsize=(15, 6))
fig.subplots_adjust(left=0.07,right=0.85,bottom=0.2)
scatterplot1(axs[0],vege['lue'],vege['rsify'],xlim_range=[0,0.2],ylim_range=[0,0.004],color='k')
scatterplot1(axs[1],repro['lue'],repro['rsify'],xlim_range=[0,0.2],ylim_range=[0,0.004],color='k')
scatterplot1(axs[2],ripen['lue'],ripen['rsify'],xlim_range=[0,0.2],ylim_range=[0,0.004],color='k')
p=scatterplot1(axs[3],daymean['lue'],daymean['rsify'],xlim_range=[0,0.2],ylim_range=[0,0.004],color='k')
for i in range(4):
    axs[i].legend()
    axs[i].tick_params(labelsize=ticklabelsize)
    labels = axs[i].get_xticklabels() + axs[i].get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    axs[i].set_xlabel('LUE',**axis_font)
    axs[i].yaxis.set_major_formatter(fromatter)
    if i==0:
        axs[i].set_ylabel('rSIF$_{yield}$',**axis_font)


fig, axs = plt.subplots(1, 1, figsize=(6,6))
idxeci=daymean['ECI']<0.3
idxeci1=daymean['ECI']>0.5
scatterplot1(axs,daymean['lue'],daymean['rsify']
             ,xlim_range=[0,0.2],ylim_range=[0,0.004],color='w')
scatterplot1(axs,daymean.loc[idxeci,'lue'],daymean.loc[idxeci,'rsify']
             ,xlim_range=[0,0.2],ylim_range=[0,0.004],color='r')
scatterplot1(axs,daymean.loc[idxeci1,'lue'],daymean.loc[idxeci1,'rsify']
             ,xlim_range=[0,0.2],ylim_range=[0,0.004],color='b')
scatterplot1(axs,daymean.loc[(-idxeci) & (-idxeci1),'lue'],daymean.loc[(-idxeci) & (-idxeci1),'rsify']
             ,xlim_range=[0,0.2],ylim_range=[0,0.004],color='k')

axs.legend()
axs.tick_params(labelsize=ticklabelsize)
labels = axs.get_xticklabels() + axs.get_yticklabels()
[label.set_fontname('Arial') for label in labels]
axs.set_xlabel('LUE',**axis_font)
axs.yaxis.set_major_formatter(fromatter)
axs.set_ylabel('rSIF$_{yield}$',**axis_font)


plt.show()