#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_sif_par_hysteresis.py
@time: 2019/3/7 16:16
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

axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 12}
title_font = {'fontname': 'Times New Roman', 'size': 14, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}

def funcstar(p):
  if p<0.001:
    return '**'
  if p<0.05 and p>=0.001:
    return '*'
  else:
    return ''

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))
ticklabelsize = 15
markersize = 15
linewidth = 3
# -------------------SIF_PAR------------------------------

filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\sunny_cloudy_data'
data = pd.read_excel(
    filepath + '\\' + r'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_diurnal_average.xlsx')

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.subplots_adjust(hspace=0.3)
time1 = np.arange(9, 12.5, 0.5)
time2 = np.arange(12.5, 16.5, 0.5)

datax = data['sunnypar']
datay = data['sunnysif']
p1 = axs[0, 0].scatter(datax.loc[0:6], datay.loc[0:6],
                       c=time1, vmin=9,vmax=16, cmap='bwr', edgecolors='k', marker='o', s=60,)
p2 = axs[0, 0].scatter(datax.loc[7:15], datay.loc[7:15],
                       c=time2, vmin=9,vmax=16, cmap='bwr',  edgecolors='k', marker='o', s=60)
# # axs[0,0].vlines(1070,0,0.88,color='k',linestyle=':',linewidth=2)
# # axs[0,0].hlines(0.88,0,1070,color='k',linestyle=':',linewidth=2)
# # axs[0,0].hlines(0.66,0,1070,color='k',linestyle=':',linewidth=2)
# axs[0, 0].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
axs[0, 0].set_ylabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
axs[0, 0].tick_params(labelsize=ticklabelsize)
axs[0,0].set_ylim(0.5,1.8)
axs[0,0].set_xlim(700,1800)
axs[0,0].text((1800-700)*0.05+700,1.8-(1.8-0.5)*0.1,'(a) Sunny days',**axis_font)

datax = data['sunnypar']
datay = data['sunnygpp']
p1 = axs[1, 0].scatter(datax.loc[0:6], datay.loc[0:6],
                       c=time1, vmin=9,vmax=16, cmap='bwr', edgecolors='k', marker='o', s=60,)
p2 = axs[1, 0].scatter(datax.loc[7:15], datay.loc[7:15],
                       c=time2, vmin=9,vmax=16, cmap='bwr',  edgecolors='k', marker='o', s=60)
axs[1, 0].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
axs[1, 0].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[1, 0].tick_params(labelsize=ticklabelsize)
axs[1,0].set_ylim(25,80)
axs[1,0].set_xlim(700,1800)
axs[1,0].text((1800-700)*0.05+700,80-(80-25)*0.1,'(c) Sunny days',**axis_font)

datax = data['cloudypar']
datay = data['cloudysif']
p1 = axs[0, 1].scatter(datax.loc[0:6], datay.loc[0:6],
                       c=time1, vmin=9,vmax=16, cmap='bwr', edgecolors='k', marker='o', s=60,)
p2 = axs[0, 1].scatter(datax.loc[7:15], datay.loc[7:15],
                       c=time2, vmin=9,vmax=16, cmap='bwr',  edgecolors='k', marker='o', s=60)
# axs[0, 1].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
# axs[0, 1].set_ylabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
axs[0, 1].tick_params(labelsize=ticklabelsize)
axs[0,1].set_ylim(0.2,0.6)
axs[0,1].set_xlim(200,800)
axs[0,1].text((800-200)*0.05+200,0.6-(0.6-0.2)*0.1,'(b) Cloudy days',**axis_font)

datax = data['cloudypar']
datay = data['cloudygpp']
p1 = axs[1, 1].scatter(datax.loc[0:6], datay.loc[0:6],
                       c=time1, vmin=9,vmax=16, cmap='bwr', edgecolors='k', marker='o', s=60,)
p2 = axs[1, 1].scatter(datax.loc[7:15], datay.loc[7:15],
                       c=time2, vmin=9,vmax=16, cmap='bwr',  edgecolors='k', marker='o', s=60)
axs[1, 1].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
# axs[1, 1].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[1, 1].tick_params(labelsize=ticklabelsize)
axs[1,1].set_ylim(10,45)
axs[1,1].set_xlim(200,800)
axs[1,1].text((800-200)*0.05+200,45-(45-10)*0.1,'(d) Cloudy days',**axis_font)

cbar = fig.colorbar(p1, ax=axs.ravel().tolist())
cbar.set_label('Hour of day', rotation=90, **axis_font)
cbar.ax.set_yticklabels(['9','10','11','12','13','14','15','16'],**axis_font)

plt.show()

