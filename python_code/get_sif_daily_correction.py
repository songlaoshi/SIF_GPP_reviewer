#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_sif_daily_correction.py
@time: 2019/3/7 22:15
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

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))
ticklabelsize = 15
markersize = 8
linewidth = 3

# def get
# -------------------SIF_PAR------------------------------

filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\sunny_cloudy_data'


vege = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_APAR_morning_afternoon_vege_dailycorrection.xlsx')
repro = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_APAR_morning_afternoon_repro_dailycorrection.xlsx')
ripen = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_APAR_morning_afternoon_ripen_dailycorrection.xlsx')
wholeseason = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_APAR_morning_afternoon_wholeseason_dailycorrection.xlsx')

fig, axs = plt.subplots(2, 4, figsize=(17, 8))
fig.subplots_adjust(hspace=0,wspace=0)
# fig.tight_layout()
t=13.5
## ------------------------vege---------------------
time=vege['time']
vegesif=vege['sunnysif']
vegepar=vege['sunnypar']
vege['sif/par']=vege['sunnysif']/vege['sunnypar']
factors=vege.loc[9,'sif/par']
vege['sif_reconstructed']=factors*vege['sunnypar']
vegesif_par=vege['sif/par']
vegesif_res=vege['sif_reconstructed']

p1, = axs[0, 0].plot(time, vegesif_par, c='gray', marker='o',label='Measured')
z=np.polyfit(time,vegesif_par,2)
p=np.poly1d(z)
yfit=np.polyval(p,time) # p(time)
p2, = axs[0, 0].plot(time, yfit, c='k',linestyle=':',label='Fitted',linewidth=2)
axs[0,0].plot(13.5,p(t),c='r',marker='o')
axs[0, 0].yaxis.set_major_formatter(fromatter)
axs[0, 0].tick_params(labelsize=ticklabelsize)
axs[0,0].set_xticks([])
axs[0,0].set_ylabel('Apparent SIF$_{yield}$',**axis_font)
axs[0,0].legend(frameon=False,loc=1)
axs[0,0].set_ylim(0,1.2e-3)
axs[0,0].set_yticks([0,3e-4,6e-4,9e-4])
axs[0,0].text(9,1.2e-3*0.9, '(a)', **axis_font)
axs[0,0].vlines(t,0,1.2e-3,color='r',linestyle=':',linewidth=2)
axs[0,0].set_title('vegetation stage',**title_font)
axs[0,0].axvspan(9,12,facecolor='gray',alpha=0.2)
cv=np.std(vegesif_par)/np.mean(vegesif_par)
axs[0,0].text(9,1.2e-3*0.1, 'CV=%.2f'%cv, **axis_font)
p3,=axs[1,0].plot(time,vegesif,c='gray',marker='o',linestyle='--',label='Measured')
p4,=axs[1,0].plot(time,p(t)*vegepar,c='k',marker='o',linestyle='--',label='Daily corrected')
temp=vegesif-p(t)*vegepar
sumsif1=np.sum(vegesif[0:6])
sumsif2=np.sum(vegesif)
# print(temp[0:9])
underest1=np.sum(temp[0:6])/sumsif1
# print(underest1)
underest2=np.sum(temp)/sumsif2
# print(underest2)
axs[1,0].text(9,0.15, 'Morning UE: %.2f'%(underest1*100)+'%', color='k',**axis_font)
axs[1,0].text(9,0.05, 'All day UE: %.2f'%(underest2*100)+'%', color='k',**axis_font)

axs[1, 0].tick_params(labelsize=ticklabelsize)
axs[1,0].set_xticks([9,11,14,16])
axs[1,0].set_ylabel(r"SIF "  + "$[mW/m^2/nm/sr]$",**axis_font)
axs[1,0].set_xlabel('Hour of day',**axis_font)
axs[1,0].legend(frameon=False,loc=1)
axs[1,0].set_ylim(0,2)
axs[1,0].set_yticks([0,0.5,1,1.5])
axs[1,0].text(9,2*0.9, '(e)', **axis_font)
axs[1,0].vlines(t,0,2,color='r',linestyle=':',linewidth=2)
axs[1,0].fill_between(time,vegesif,p(t)*vegepar,color='gray',alpha=0.5)
axs[1,0].axvspan(9,12,facecolor='gray',alpha=0.2)
# ------------------------repro---------------------
time=repro['time']
vegesif=repro['sunnysif']
vegepar=repro['sunnypar']
repro['sif/par']=repro['sunnysif']/repro['sunnypar']
factors=repro.loc[9,'sif/par']
repro['sif_reconstructed']=factors*repro['sunnypar']
vegesif_par=repro['sif/par']
vegesif_res=repro['sif_reconstructed']

p1, = axs[0, 1].plot(time, vegesif_par, c='gray', marker='o')
z=np.polyfit(time,vegesif_par,2)
p=np.poly1d(z)
yfit=np.polyval(p,time) # p(time)
p2, = axs[0, 1].plot(time, yfit, c='k',linestyle=':',linewidth=2)
axs[0,1].plot(13.5,p(t),c='r',marker='o')
axs[0, 1].yaxis.set_major_formatter(fromatter)
axs[0, 1].tick_params(labelsize=ticklabelsize)
axs[0,1].set_xticks([])
axs[0,1].set_ylim(0,1.2e-3)
axs[0,1].set_yticks([])
axs[0,1].text(9,1.2e-3*0.9, '(b)', **axis_font)
axs[0,1].vlines(t,0,1.2e-3,color='r',linestyle=':',linewidth=2)
axs[0,1].set_title('reproductive stage',**title_font)
axs[0,1].axvspan(9,12,facecolor='gray',alpha=0.2)
cv=np.std(vegesif_par)/np.mean(vegesif_par)
axs[0,1].text(9,1.2e-3*0.1, 'CV=%.2f'%cv, **axis_font)
# axs[0,1].set_ylabel('Apparent SIF$_{yield}$',**axis_font)
p3,=axs[1,1].plot(time,vegesif,c='gray',marker='o',linestyle='--')
p4,=axs[1,1].plot(time,p(t)*vegepar,c='k',marker='o',linestyle='--')
axs[1, 1].tick_params(labelsize=ticklabelsize)
axs[1,1].set_xticks([9,11,14,16])
# axs[1,1].set_ylabel(r"SIF "  + "$[mW/m^2/nm/sr]$",**axis_font)
axs[1,1].set_xlabel('Hour of day',**axis_font)
axs[1,1].set_ylim(0,2)
axs[1,1].set_yticks([])
axs[1,1].text(9,2*0.9, '(f)', **axis_font)
axs[1,1].vlines(t,0,2,color='r',linestyle=':',linewidth=2)
axs[1,1].fill_between(time,vegesif,p(t)*vegepar,color='gray',alpha=0.5)
axs[1,1].axvspan(9,12,facecolor='gray',alpha=0.2)

temp=vegesif-p(t)*vegepar
sumsif1=np.sum(vegesif[0:6])
sumsif2=np.sum(vegesif)
# print(temp[0:9])
underest1=np.sum(temp[0:6])/sumsif1
# print(underest1)
underest2=np.sum(temp)/sumsif2
# print(underest2)
axs[1,1].text(9,0.15, 'Morning UE: %.2f'%(underest1*100)+'%', color='k',**axis_font)
axs[1,1].text(9,0.05, 'All day UE: %.2f'%(underest2*100)+'%', color='k',**axis_font)
## ------------------------ripen---------------------
time=ripen['time']
vegesif=ripen['sunnysif']
vegepar=ripen['sunnypar']
ripen['sif/par']=ripen['sunnysif']/ripen['sunnypar']
factors=ripen.loc[9,'sif/par']
ripen['sif_reconstructed']=factors*ripen['sunnypar']
vegesif_par=ripen['sif/par']
vegesif_res=ripen['sif_reconstructed']

p1, = axs[0, 2].plot(time, vegesif_par, c='gray', marker='o')
z=np.polyfit(time,vegesif_par,2)
p=np.poly1d(z)
yfit=np.polyval(p,time) # p(time)
p2, = axs[0, 2].plot(time, yfit, c='k',linestyle=':',linewidth=2)
axs[0,2].plot(13.5,p(t),c='r',marker='o')
axs[0, 2].yaxis.set_major_formatter(fromatter)
axs[0, 2].tick_params(labelsize=ticklabelsize)
axs[0,2].set_xticks([])
axs[0,2].set_ylim(0,1.2e-3)
axs[0,2].set_yticks([])
axs[0,2].text(9,1.2e-3*0.9, '(c)', **axis_font)
axs[0,2].vlines(t,0,1.2e-3,color='r',linestyle=':',linewidth=2)
axs[0,2].set_title('ripening stage',**title_font)
axs[0,2].axvspan(9,12,facecolor='gray',alpha=0.2)
cv=np.std(vegesif_par)/np.mean(vegesif_par)
axs[0,2].text(9,1.2e-3*0.1, 'CV=%.2f'%cv, **axis_font)
# axs[0,2].set_ylabel('Apparent SIF$_{yield}$',**axis_font)
p3,=axs[1,2].plot(time,vegesif,c='gray',marker='o',linestyle='--')
p4,=axs[1,2].plot(time,p(t)*vegepar,c='k',marker='o',linestyle='--')
axs[1, 2].tick_params(labelsize=ticklabelsize)
axs[1,2].set_xticks([9,11,14,16])
# axs[1,2].set_ylabel(r"SIF "  + "$[mW/m^2/nm/sr]$",**axis_font)
axs[1,2].set_xlabel('Hour of day',**axis_font)
axs[1,2].set_ylim(0,2)
axs[1,2].set_yticks([])
axs[1,2].text(9,2*0.9, '(g)', **axis_font)
axs[1,2].vlines(t,0,2,color='r',linestyle=':',linewidth=2)
axs[1,2].fill_between(time,vegesif,p(t)*vegepar,color='gray',alpha=0.5)
axs[1,2].axvspan(9,12,facecolor='gray',alpha=0.2)
temp=vegesif-p(t)*vegepar
sumsif1=np.sum(vegesif[0:6])
sumsif2=np.sum(vegesif)
# print(temp[0:9])
underest1=np.sum(temp[0:6])/sumsif1
# print(underest1)
underest2=np.sum(temp)/sumsif2
# print(underest2)
axs[1,2].text(9,0.15, 'Morning UE: %.2f'%(underest1*100)+'%', color='k',**axis_font)
axs[1,2].text(9,0.05, 'All day UE: %.2f'%(underest2*100)+'%', color='k',**axis_font)
## ------------------------wholeseason---------------------
time=wholeseason['time']
vegesif=wholeseason['sunnysif']
vegepar=wholeseason['sunnypar']
wholeseason['sif/par']=wholeseason['sunnysif']/wholeseason['sunnypar']
factors=wholeseason.loc[9,'sif/par']
wholeseason['sif_reconstructed']=factors*wholeseason['sunnypar']
vegesif_par=wholeseason['sif/par']
vegesif_res=wholeseason['sif_reconstructed']

p1, = axs[0, 3].plot(time, vegesif_par, c='gray', marker='o')
z=np.polyfit(time,vegesif_par,2)
p=np.poly1d(z)
yfit=np.polyval(p,time) # p(time)
p2, = axs[0, 3].plot(time, yfit, c='k',linestyle=':',linewidth=2)
axs[0,3].plot(13.5,p(t),c='r',marker='o')
axs[0, 3].yaxis.set_major_formatter(fromatter)
axs[0, 3].tick_params(labelsize=ticklabelsize)
axs[0,3].set_xticks([])
axs[0,3].set_ylim(0,1.2e-3)
axs[0,3].set_yticks([])
axs[0,3].text(9,1.2e-3*0.9, '(d)', **axis_font)
axs[0,3].vlines(t,0,1.2e-3,color='r',linestyle=':',linewidth=2)
axs[0,3].set_title('whole season',**title_font)
axs[0,3].axvspan(9,12,facecolor='gray',alpha=0.2)
cv=np.std(vegesif_par)/np.mean(vegesif_par)
axs[0,3].text(9,1.2e-3*0.1, 'CV=%.2f'%cv, **axis_font)
# axs[0,3].set_ylabel('Apparent SIF$_{yield}$',**axis_font)
p3,=axs[1,3].plot(time,vegesif,c='gray',marker='o',linestyle='--')
p4,=axs[1,3].plot(time,p(t)*vegepar,c='k',marker='o',linestyle='--')
axs[1, 3].tick_params(labelsize=ticklabelsize)
axs[1,3].set_xticks([9,11,14,16])
# axs[1,3].set_ylabel(r"SIF "  + "$[mW/m^2/nm/sr]$",**axis_font)
axs[1,3].set_xlabel('Hour of day',**axis_font)
axs[1,3].set_ylim(0,2)
axs[1,3].set_yticks([])
axs[1,3].text(9,2*0.9, '(h)', **axis_font)
axs[1,3].vlines(t,0,2,color='r',linestyle=':',linewidth=2)
axs[1,3].fill_between(time,vegesif,p(t)*vegepar,color='gray',alpha=0.5)
axs[1,3].axvspan(9,12,facecolor='gray',alpha=0.2)
temp=vegesif-p(t)*vegepar
sumsif1=np.sum(vegesif[0:6])
sumsif2=np.sum(vegesif)
# print(temp[0:9])
underest1=np.sum(temp[0:6])/sumsif1
# print(underest1)
underest2=np.sum(temp)/sumsif2
# print(underest2)
axs[1,3].text(9,0.15, 'Morning UE: %.2f'%(underest1*100)+'%', color='k',**axis_font)
axs[1,3].text(9,0.05, 'All day UE: %.2f'%(underest2*100)+'%', color='k',**axis_font)

plt.show()