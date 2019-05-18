#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_sif_uncertainty.py
@time: 2019/4/27 19:13
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import funcs_lzh

axis_font = {'fontname': 'Arial', 'size': 12, 'color': 'black'}
legend_font = {'family': 'Arial', 'size': 11}
ticklabelsize = 14
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}

filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\sif_uncertainty'
data=pd.ExcelFile(filepath+'\\sif_uncertainty.xlsx')
data_cloudy=data.parse(0)
data_sunny=data.parse(1)
#
fig,axs=plt.subplots(2,1,figsize=(8,6))
fig.subplots_adjust(hspace=0.25,right=0.82)

axs[0].scatter((data_sunny['raw_doy']-255)*24,data_sunny['raw_sif'],marker='.',color='k',alpha=0.3)
p1=axs[0].errorbar((data_sunny['half_doy']-255)*24,data_sunny['half_mean'],yerr=data_sunny['half_std'],marker='o',mec='k'
                ,mfc='r',linestyle='',ecolor='k',capsize=3)
par1=axs[0].twinx()
p2=par1.scatter((data_sunny['half_doy']-255)*24,data_sunny['half_restd']*100,marker='v',edgecolor='b',facecolor='')
par2=axs[0].twinx()
par2.spines["right"].set_position(("axes", 1.1))
funcs_lzh.make_patch_spines_invisible(par2)
par2.spines["right"].set_visible(True)
p3,=par2.plot((data_sunny['par_doynew']-255)*24,data_sunny['par'],marker='o',color='k')
# 画天顶角
idx=data_sunny['raw_sza']<=60
doy=(data_sunny.loc[idx,'raw_doy']-255)*24
doy1=doy.iloc[0]
doy2=doy.iloc[-1]
# print(doy1,doy2)
p4=axs[0].axvspan(doy1, doy2, color='grey', alpha=0.2)
# 求SZA<60下的所有relative SD的平均值和标准差
idx_sd=(data_sunny['half_doy']>=doy1/24+255) & (data_sunny['half_doy']<=doy2/24+255)
mean_sd=np.nanmean(data_sunny.loc[idx_sd,'half_restd'])
std_sd=np.nanstd(data_sunny.loc[idx_sd,'half_restd'])
min_sd=np.nanmin(data_sunny.loc[idx_sd,'half_restd'])
max_sd=np.nanmax(data_sunny.loc[idx_sd,'half_restd'])
print(min_sd,max_sd,mean_sd,std_sd)

axs[0].legend([p1,p2,p3,p4],['SIF','relative SD','PAR','SZA<60°']
              ,prop=legend_font,frameon=False,bbox_to_anchor=(0.,1.05,1,0.1)
                  ,borderaxespad=0.,loc='center',mode='extend',
                  labelspacing=0.02,handletextpad=0.1,ncol=4)

axs[1].scatter((data_cloudy['raw_doy']-210)*24,data_cloudy['raw_sif'],marker='.',color='k',alpha=0.3)
p1=axs[1].errorbar((data_cloudy['half_doy']-210)*24,data_cloudy['half_mean'],yerr=data_cloudy['half_std'],marker='o',mec='k'
                ,mfc='r',linestyle='',ecolor='k',capsize=3)
par3=axs[1].twinx()
p2=par3.scatter((data_cloudy['half_doy']-210)*24,data_cloudy['half_restd']*100,marker='v',edgecolor='b',facecolor='')
par4=axs[1].twinx()
par4.spines["right"].set_position(("axes", 1.1))
funcs_lzh.make_patch_spines_invisible(par4)
par4.spines["right"].set_visible(True)
p3=par4.plot((data_cloudy['par_doynew']-210)*24,data_cloudy['par'],marker='o',color='k')
#
idx=data_cloudy['raw_sza']<=60
doy=(data_cloudy.loc[idx,'raw_doy']-210)*24
doy1=doy.iloc[0]
doy2=doy.iloc[-1]
# print(doy1,doy2)
axs[1].axvspan(doy1, doy2, color='grey', alpha=0.2)
# axs[1].legend([p1,p2,p3],['SIF','PAR','relative SD'],prop=legend_font,frameon=False,loc=2)
# 求SZA<60下的所有relative SD的平均值和标准差
idx_sd=(data_cloudy['half_doy']>=doy1/24+210) & (data_cloudy['half_doy']<=doy2/24+210)
mean_sd=np.nanmean(data_cloudy.loc[idx_sd,'half_restd'])
std_sd=np.nanstd(data_cloudy.loc[idx_sd,'half_restd'])
min_sd=np.nanmin(data_cloudy.loc[idx_sd,'half_restd'])
max_sd=np.nanmax(data_cloudy.loc[idx_sd,'half_restd'])
print(min_sd,max_sd,mean_sd,std_sd)


for ax in axs:
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    ax.set_ylabel('SIF'+'\n'+'[$mW/m^2/nm/sr$]',**axis_font)
    ax.set_xlabel('Hour',**axis_font)
    ax.set_xlim([6,18])
    ax.set_ylim([0,1.5])

for ax in [par1 ,par2 ,par3,par4]:
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    if (ax==par1) | (ax==par3):
        ax.set_ylabel('relative SD of SIF [%]',**axis_font)
        ax.set_ylim([0,70])
    if (ax==par2) | (ax==par4):
        ax.set_ylabel('PAR [$\mu mol/m^2/s$]', **axis_font)
    if ax==par2:
        ax.set_ylim([0,1600])
    if ax==par4:
        ax.set_ylim([0, 600])
axs[0].text(6.2,1.3,'(a) DOY=255, sunny',**axis_font)
axs[1].text(6.2,1.3,'(b) DOY=210, cloudy',**axis_font)

plt.show()
