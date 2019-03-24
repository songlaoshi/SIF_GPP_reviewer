#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-02-21 18:47:52
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

import os
import numpy as np
import pandas as pd
import pylab
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from matplotlib import ticker
import funcs_lzh

axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 12}
title_font = {'fontname': 'Times New Roman', 'size': 14, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}


def funcstar(p):
    if p < 0.001:
        return '**'
    if p < 0.05 and p >= 0.001:
        return '*'
    else:
        return ''

def plot_ifld_sfm(sif_sfm,sif_ifld,title,axs,xlabel,ylabel):
	x=sif_sfm
	y=sif_ifld
	a, b, pred_y = funcs_lzh.get_lingre(x.values.reshape(-1, 1), y)
	r, p = pearsonr(x, y)
	rmse,rrmse=funcs_lzh.get_rmse_rrmse(sif_sfm,sif_ifld)
	r2 = '%.2f' % np.square(r)
	text_line = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
	text_rsqu = '$R^2$= ' + r2 + funcstar(p)
	text_rmse='RMSE= '+'%.2f'%rmse
	text_rrmse='RRMSE= '+'%.2f'%(rrmse*100)
	axs.scatter(x, y, edgecolors='k',
	                facecolors='', label='')
	axs.plot(x, pred_y, label='', color='k')
	axs.set_xlabel(xlabel, **axis_font)
	axs.set_ylabel(ylabel, **axis_font)
	# axs.legend(frameon=False)
	axs.tick_params(labelsize=ticklabelsize)

	y=np.arange(0,3.5,0.1)
	axs.plot(y,y,'k--')
	axs.set_xlim(0,3)
	axs.set_ylim(0,3)
	axs.set_title(title,**title_font)
	axs.text(0.1,2.2,text_line+'\n'+text_rsqu+'\n'+text_rmse+'\n'+text_rrmse)

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))
ticklabelsize = 15
markersize = 15
linewidth = 3

a1 = 192
a2 = 205
a3 = 255
a4 = 283
# -------------------iFLD and SFM------------------------------

filepath = r'D:\Data\shangqiu data\shang\Results\GPP_PAR_APAR_SIF_8_18\ALLnew'

data_halfhour = pd.ExcelFile(
    filepath + '\GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_NIRv_CI_SIFyield_LUE_halfhour.xlsx')
data_halfhour = data_halfhour.parse(0)

sif_ifld=data_halfhour['iFLD']
sif_sfm=data_halfhour['SFMlinear']
doy=data_halfhour['DOY']
gpp=data_halfhour['GPP']
daymean=pd.concat([doy,gpp,sif_ifld,sif_sfm],axis=1)
daymean=daymean.dropna()

vege = daymean[daymean['DOY'] <= a2]
repro = daymean[(daymean['DOY'] > a2) & (daymean['DOY'] <= a3)]
ripen = daymean[daymean['DOY'] > a3]

# 


fig,axs=plt.subplots(1,4,figsize=(12,5))
# plt.subplots_adjust(left=0.19,bottom=0.15,right=0.88,top=0.76)

sif_ifld=vege['iFLD']
sif_sfm=vege['SFMlinear']
plot_ifld_sfm(sif_sfm,sif_ifld,'vegetation stage',axs[0],xlabel='SFM $[mW/m^2/nm/sr]$',ylabel='iFLD $[mW/m^2/nm/sr]$')
sif_ifld=repro['iFLD']
sif_sfm=repro['SFMlinear']
plot_ifld_sfm(sif_sfm,sif_ifld,'reproductive stage',axs[1],xlabel='SFM $[mW/m^2/nm/sr]$',ylabel='')
sif_ifld=ripen['iFLD']
sif_sfm=ripen['SFMlinear']
plot_ifld_sfm(sif_sfm,sif_ifld,'ripening stage',axs[2],xlabel='SFM $[mW/m^2/nm/sr]$',ylabel='')
sif_ifld=daymean['iFLD']
sif_sfm=daymean['SFMlinear']
plot_ifld_sfm(sif_sfm,sif_ifld,'whole season',axs[3],xlabel='SFM $[mW/m^2/nm/sr]$',ylabel='')


plt.show()

