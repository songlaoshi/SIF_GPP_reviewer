#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_sif_gpp.py
@time: 2019/3/21 16:00
'''

import os
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from matplotlib import ticker
from sklearn.metrics import r2_score
import funcs_lzh

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 14}
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}
ticklabelsize = 14
markersize = 8
linewidth = 3
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

def funcp(p):
    if p < 0.001:
        return 0.001
    if p < 0.05 and p > 0.001:
        return 0.05
    if p > 0.05 and p < 0.1:
        return 0.1
    else:
        return 1

# growth stage
a1 = 192.0
a2 = 205.0
a3 = 255.0
a4 = 283.0
# daymean
filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = daymean.parse(0)
# daymean=daymean[daymean['CI']>0.8]

daymean = pd.concat([daymean['doy'], daymean['SFM'], daymean['GPP'], daymean['PAR'],
                     daymean['SIFyieldgndvi'], daymean['LUEgndvi'], daymean['CI'],
                     daymean['greenNDVI'], daymean['VPD'], daymean['Ta'], daymean['PRI']], axis=1)
daymean = daymean.dropna()
daymean['apar'] = daymean['greenNDVI'] * daymean['PAR']
daymean['scaled_APAR'] = MaxMinNormalization(daymean['apar'], np.max(daymean['apar']), np.min(daymean['apar']))
daymean['scaled_VPD'] = MaxMinNormalization(daymean['VPD'], np.max(daymean['VPD']), np.min(daymean['VPD']))
daymean['scaled_Ta'] = MaxMinNormalization(daymean['Ta'], np.max(daymean['Ta']), np.min(daymean['Ta']))
daymean['eci'] = daymean['scaled_APAR'] + daymean['scaled_VPD'] + daymean['scaled_Ta']
daymean['ECI'] = MaxMinNormalization(daymean['eci'], np.max(daymean['eci']), np.min(daymean['eci']))
daymean['sify'] = daymean['SIFyieldgndvi']
daymean['lue'] = daymean['LUEgndvi']

# 分阶段
vege = daymean[daymean['doy'] <= a2]
repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] <= a3)]
ripen = daymean[daymean['doy'] > a3]

fig, axs = plt.subplots(2, 4, figsize=(30, 8.5))
fig.subplots_adjust(left=0.07,right=0.85)

r,p=get_pearsonr(vege['GPP'],vege['SFM'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[0, 0].scatter(vege['GPP'], vege['SFM'], c=vege['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[0,0].set_xlabel('GPP $[μmol CO_2/m^2/s]$',**axis_font)
axs[0,0].set_ylabel('SIF $[mW/m^2/nm/sr]$',**axis_font)
axs[0,0].set_xlim([0,100])
axs[0,0].set_ylim([0,2.5])
r,p=get_pearsonr(repro['GPP'],repro['SFM'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[0, 1].scatter(repro['GPP'], repro['SFM'], c=repro['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[0,1].set_xlabel('GPP $[μmol CO_2/m^2/s]$',**axis_font)
axs[0,1].set_xlim([0,100])
axs[0,1].set_ylim([0,2.5])
r,p=get_pearsonr(ripen['GPP'],ripen['SFM'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[0, 2].scatter(ripen['GPP'], ripen['SFM'], c=ripen['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[0,2].set_xlabel('GPP $[μmol CO_2/m^2/s]$',**axis_font)
axs[0,2].set_xlim([0,100])
axs[0,2].set_ylim([0,2.5])
r,p=get_pearsonr(daymean['GPP'],daymean['SFM'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[0, 3].scatter(daymean['GPP'], daymean['SFM'], c=daymean['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[0,3].set_xlabel('GPP $[μmol CO_2/m^2/s]$',**axis_font)
axs[0,3].set_xlim([0,100])
axs[0,3].set_ylim([0,2.5])
axs[0, 0].tick_params(labelsize=ticklabelsize)
axs[0, 1].tick_params(labelsize=ticklabelsize)
axs[0, 2].tick_params(labelsize=ticklabelsize)
axs[0, 3].tick_params(labelsize=ticklabelsize)
axs[0, 0].set_title('vegetation stage', **title_font)
axs[0, 1].set_title('reproductive stage', **title_font)
axs[0, 2].set_title('ripening stage', **title_font)
axs[0, 3].set_title('whole season', **title_font)
axs[0,0].legend()
axs[0,1].legend()
axs[0,2].legend()
axs[0,3].legend()

r,p=get_pearsonr(vege['lue'],vege['sify'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[1, 0].scatter(vege['lue'], vege['sify'], c=vege['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[1,0].set_ylim([0,0.002])
axs[1,0].set_xlim([0,0.15])
axs[1,0].yaxis.set_major_formatter(fromatter)
axs[1,0].set_xlabel('LUE',**axis_font)
axs[1,0].set_ylabel('SIF$_{yield}$',**axis_font)

r,p=get_pearsonr(repro['lue'],repro['sify'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[1, 1].scatter(repro['lue'], repro['sify'], c=repro['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[1,1].set_ylim([0,0.002])
axs[1,1].set_xlim([0,0.15])
axs[1,1].set_xlabel('LUE',**axis_font)
axs[1,1].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(ripen['lue'],ripen['sify'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
axs[1, 2].scatter(ripen['lue'], ripen['sify'], c=ripen['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[1,2].set_ylim([0,0.002])
axs[1,2].set_xlim([0,0.15])
axs[1,2].set_xlabel('LUE',**axis_font)
axs[1,2].yaxis.set_major_formatter(fromatter)

r,p=get_pearsonr(daymean['lue'],daymean['sify'])
label='r= %.2f'%r+funcs_lzh.funcstar(p)
p=axs[1, 3].scatter(daymean['lue'], daymean['sify'], c=daymean['ECI'],vmin=0, vmax=1, cmap='jet', marker='o',label=label)
axs[1,3].set_ylim([0,0.002])
axs[1,3].set_xlim([0,0.15])
axs[1,3].set_xlabel('LUE',**axis_font)
axs[1,3].yaxis.set_major_formatter(fromatter)

axs[1, 0].tick_params(labelsize=ticklabelsize)
axs[1, 1].tick_params(labelsize=ticklabelsize)
axs[1, 2].tick_params(labelsize=ticklabelsize)
axs[1, 3].tick_params(labelsize=ticklabelsize)
axs[1,0].legend()
axs[1,1].legend()
axs[1,2].legend()
axs[1,3].legend()
cbar_ax = fig.add_axes([0.87, 0.15, 0.01, 0.7])
cbar1=fig.colorbar(p, cax=cbar_ax)
cbar1.set_label('ECI [-]',rotation=90, **axis_font)
cbar1.ax.set_yticklabels(['0','0.2','0.4','0.6','0.8','1'],**axis_font)


plt.show()
