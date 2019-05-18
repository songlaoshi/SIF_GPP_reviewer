#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_eci_reason.py
@time: 2019/5/16 16:07
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import funcs_lzh
import math

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

alphadot=0.5

axis_font = {'fontname': 'Arial', 'size': 12, 'color': 'black'}
legend_font = {'family': 'Arial', 'size': 11}
ticklabelsize = 12
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}

def scatter_half_day(ax,x,y,ylabel,color):
    ax.scatter(x,y,marker='.',edgecolors=''
               ,facecolors=color,alpha=alphadot)
    ax.set_ylabel(ylabel,**axis_font)

def scatter_errorbar(ax,x,y,yerr,color,marker):
    h=ax.errorbar(x,y,yerr=yerr,marker=marker,mec='k'
                ,mfc=color,linestyle='',ecolor='k',
                capsize=3)
    return h
# ======================================
filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
figsavepath=r'D:\Thesis writing\SQ2017\Reviews\figures'

datahalf=pd.ExcelFile(filepath+'\SIF_GPP_VI_ref_halfhourmean_sq2017corn_8-18_addSZA_norain_all_lueclean.xlsx')
datahalf=datahalf.parse(0)
## 去掉太阳天顶角>60
datahalf.loc[datahalf['SZA']>60,:]=np.nan
#
day=pd.ExcelFile(filepath+'\SIF_GPP_VI_ref_daymean_sq2017corn_8-18_addSZA_norain_all.xlsx')
daymean=day.parse(0)
daystd=day.parse(1)
#
doymean=daymean['DOY']
doyhalf=datahalf['DOY']
# # #
fig, axs = plt.subplots(4,1,sharex=True,figsize=(10, 8))
fig.subplots_adjust(hspace=0,left=0.1,right=0.95,top=0.95)
#
scatter_half_day(axs[0],doyhalf,datahalf['ECI'],'ECI [-]','k')
scatter_errorbar(axs[0],doymean,daymean['ECI'],daystd['ECI'],color='r',marker='o')
#
scatter_half_day(axs[1],doyhalf,datahalf['VPD'],'VPD [kPa]','k')
scatter_errorbar(axs[1],doymean,daymean['VPD'],daystd['VPD'],color='r',marker='o')

scatter_half_day(axs[2],doyhalf,datahalf['Ta'],'Ta [°C]','k')
scatter_errorbar(axs[2],doymean,daymean['Ta'],daystd['Ta'],color='r',marker='o')

scatter_half_day(axs[3],doyhalf,datahalf['apar'],'APAR [$\mu mol/m^2/s$]','k')
scatter_errorbar(axs[3],doymean,daymean['apar'],daystd['apar'],color='r',marker='o')

# 画ECI<0.4的所有半小时数据的阴影
eci_threld=0.4
idx=datahalf['ECI']<0.4
doy_eci=doyhalf[idx]
print(doy_eci.shape)
# for x in range(len(doy_eci)-1):
#     if doy_eci.iloc[x+1]-doy_eci.iloc[x]<0.6/24:
#         axs[0].axvspan(doy_eci.iloc[x],doy_eci.iloc[x+1],facecolor='k',alpha=0.5)

for x in doy_eci:
    axs[0].axvline(x=x,color='orange',alpha=0.2)
    axs[1].axvline(x=x, color='orange', alpha=0.2)
    axs[2].axvline(x=x, color='orange',alpha=0.2)
    axs[3].axvline(x=x, color='orange', alpha=0.2)


p=axs[0].axhline(y=0.4,color='k',linestyle='--')
axs[0].set_yticks([0,0.4,0.8])
axs[0].set_yticklabels(['0','0.4','0.8'])
#
label_text=['(a)','(b)','(c)','(d)']
for i in range(len(axs)):
    ax=axs[i]
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    ax.text(188, (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.88 + ax.get_ylim()[0], label_text[i], **axis_font)

axs[3].set_xlabel('DOY',**axis_font)

plt.savefig(figsavepath+'\\sup_fig1.png',dpi=300)

plt.show()