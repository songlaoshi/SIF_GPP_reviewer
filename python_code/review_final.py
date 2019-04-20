#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: review_final.py
@time: 2019/4/19 23:19
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


def MaxMinNormalization(x, max, min):
    x = (x - min) / (max - min)
    return x


def plot_01(axs, x, y, c, xlabel, ylabel,vmin,vmax):
    r, p = get_pearsonr(x, y)
    p = axs.scatter(x, y, c=c, cmap='jet', vmin=vmin, vmax=vmax,marker='.', label='r= %.2f' % r + funcs_lzh.funcstar(p))
    axs.set_xlabel(xlabel,**axis_font)
    axs.set_ylabel(ylabel,**axis_font)
    axs.legend()
    return p


def plot_02(axs, x, y, color, llabel):
    r, p = get_pearsonr(x, y)
    axs.scatter(x, y, color=color,
                marker='.', label=llabel + 'r= %.2f' % r + funcs_lzh.funcstar(p))


def plot_07(axs, data, xlabel, ylabel, clabel):
    p = axs.scatter(data['sify'], data['lue'],
                    c=data[clabel], cmap='Blues', marker='.')
    axs.set_xlim([0, 0.002])
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)
    return p


# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 14}
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 18, }
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize = 14

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
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn_8-18_addSZA_norain_all_lueclean.xlsx')
daymean=daymean.parse(0)
# daymean = pd.ExcelFile(
#     filepath + '\\' + r'SIF_GPP_VI_ref_daymean_sq2017corn_8-18_addSZA_norain.xlsx')
# daymean=daymean.parse(0)
# 去掉SZA>60的数据
daymean=daymean[daymean['SZA']<60]
# # 选取晴天数据
# daymean=daymean[daymean['CI']>0.5]
#
daymean = pd.concat([daymean['DOY'], daymean['hour'], daymean['MTVI2'], daymean['CIgreen']
                        ,daymean['SFMlinear'], daymean['GPP'], daymean['PAR'],daymean['ECI']
                        , daymean['VPD'], daymean['Ta'], daymean['PRI'],daymean['sify'],
                     daymean['lue']], axis=1)
daymean = daymean.dropna()
# 去掉structural and pigment effects
meanMTVI2=np.mean(daymean['MTVI2'])
daymean['scaled_MTVI2']=daymean['MTVI2']/meanMTVI2
daymean['rsify']=daymean['sify']/daymean['scaled_MTVI2']
daymean['rpri']=daymean['PRI']/daymean['scaled_MTVI2']
# 分阶段
vege = daymean[daymean['DOY'] <= a2]
repro = daymean[(daymean['DOY'] > a2) & (daymean['DOY'] <= a3)]
ripen = daymean[daymean['DOY'] > a3]
## SIFyield-LUE & PRI-LUE的关系
fig,axs=plt.subplots(1,2,figsize=(8,3.5))
fig.subplots_adjust(left=0.1,bottom=0.15,right=0.92,
                    top=0.92,wspace=0.33)
r,p=get_pearsonr(daymean['lue'],daymean['sify'])
label='R$^2$= %.2f'%np.square(r)+funcs_lzh.funcstar(p)
p=axs[0].scatter(daymean['lue'], daymean['sify'], c=daymean['ECI'],vmin=0, vmax=1
                 , cmap='jet', marker='o',label=label,edgecolor='k')
axs[0].set_ylim([-0.001,0.003])
axs[0].set_ylabel('$SIF_{yield}$',**axis_font)
r,p=get_pearsonr(daymean['lue'],daymean['PRI'])
label='R$^2$= %.2f'%np.square(r)+funcs_lzh.funcstar(p)
p=axs[1].scatter(daymean['lue'], daymean['PRI'], c=daymean['ECI'],vmin=0, vmax=1
                 , cmap='jet', marker='o',label=label,edgecolor='k')
axs[1].set_ylabel('PRI',**axis_font)
for ax in axs:
    ax.yaxis.set_major_formatter(fromatter)
    ax.set_xlim([-0.01,0.14])
    ax.set_xlabel('LUE',**axis_font)
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    ax.legend()

# SIFyield,LUE,PRI与ECI,LAI&Cab是否有关系
fig,axs=plt.subplots(3,2,figsize=(10,10))
# fig.subplots_adjust(left=0.1,right=0.9)
plot_01(axs[0,0],daymean['ECI'],daymean['sify'],daymean['MTVI2'],'','$SIF_{yield}$',vmin=0,vmax=1)
axs[0,0].set_ylim([-0.001,0.003])
plot_01(axs[2,0],daymean['ECI'],daymean['lue'],daymean['MTVI2'],'ECI','LUE',vmin=0,vmax=1)
p1=plot_01(axs[1,0],daymean['ECI'],daymean['PRI'],daymean['MTVI2'],'','PRI',vmin=0,vmax=1)
cbar_ax = fig.add_axes([0.13, 0.9, 0.34, 0.02])
cbar1=fig.colorbar(p1, cax=cbar_ax,orientation='horizontal',ticklocation='top')
cbar1.set_label('MTVI2 [-]', rotation=0,**axis_font)
axs[0,0].yaxis.set_major_formatter(fromatter)
axs[1,0].yaxis.set_major_formatter(fromatter)
axs[2,0].yaxis.set_major_formatter(fromatter)

plot_01(axs[0,1],daymean['MTVI2'],daymean['sify'],daymean['ECI'],'','',vmin=0,vmax=1)
axs[0,1].set_ylim([-0.001,0.003])
axs[0,1].set_yticks([])
plot_01(axs[2,1],daymean['MTVI2'],daymean['lue'],daymean['ECI'],'MTVI2','',vmin=0,vmax=1)
axs[2,1].set_yticks([])
# axs[1,1].axvspan(0.25,0.42,facecolor='gray',alpha=0.2)
p2=plot_01(axs[1,1],daymean['MTVI2'],daymean['PRI'],daymean['ECI'],'','',vmin=0,vmax=1)
axs[1,1].set_yticks([])
cbar_ax1 = fig.add_axes([0.555, 0.9, 0.34, 0.02])
cbar2=fig.colorbar(p2, cax=cbar_ax1,orientation='horizontal',ticklocation='top')
cbar2.set_label('ECI [-]', rotation=0,**axis_font)


for ax in axs[:,0]:
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
for ax in axs[:,1]:
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
for cb in [cbar1,cbar2]:
    cb.ax.tick_params(labelsize=ticklabelsize)
    labels = cb.ax.get_xticklabels() + cb.ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]




plt.show()