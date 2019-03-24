#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: re_wohlfahrt_thesis02.py
@time: 2019/3/4 15:26
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit
from matplotlib import ticker
import math
import funcs_lzh
from scipy.stats.stats import pearsonr

# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))
# 字符格式
axis_font = {'fontname': 'Arial', 'size': 18}
font1={'family':'Times New Roman',
'weight':'normal',
'size':18,}
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize=18

# daymean
filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
data = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = data.parse(0)
daymean['fPAR']=daymean['greenNDVI']
daymean['fPAR1']=daymean['APAR']/daymean['PAR']

daymean['SIFyield']=daymean['SFM']/(daymean['fPAR']*daymean['PAR'])
daymean['lue']=daymean['GPP']/(daymean['fPAR']*daymean['PAR'])


# a1 = 192
# a2 = 205
# a3 = 255
# a4 = 283
#
# vege = daymean[daymean['doy'] <= a2]
# repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] < a3+1)]
# ripen = daymean[daymean['doy'] > a3]
#
# fig,axs=plt.subplots(1,1)
# plt1=axs.twinx()
# axs.scatter(vege['doy'],vege['fPAR'],marker='.',color='r')
# plt1.scatter(vege['doy'],vege['fPAR1'],marker='v',color='r')
# axs.scatter(repro['doy'],repro['fPAR'],marker='.',color='g')
# plt1.scatter(repro['doy'],repro['fPAR1'],marker='v',color='g')
# axs.scatter(ripen['doy'],ripen['fPAR'],marker='.',color='b')
# plt1.scatter(ripen['doy'],ripen['fPAR1'],marker='v',color='b')
# fig,axs=plt.subplots(1,1)
# axs.scatter(vege['fPAR1'],vege['fPAR'],marker='.',color='r')
# axs.scatter(repro['fPAR1'],repro['fPAR'],marker='.',color='g')
# axs.scatter(ripen['fPAR1'],ripen['fPAR'],marker='.',color='b')

daymean=pd.concat([daymean['doy'],daymean['PRI'],daymean['MTVI2'],daymean['SIFyield'],daymean['lue'],daymean['CI']],axis=1)
daymean=daymean.dropna()

doy=daymean['doy']
pri=daymean['PRI']
mtvi2=daymean['MTVI2']
sify=daymean['SIFyield']
lue=daymean['lue']
sPRI=0.1726*mtvi2-0.1346
sFY760=0.001*mtvi2**2+0.0006*mtvi2+0.0001
sLUE=0.035*mtvi2**2+0.0655*mtvi2-0.0009
daymean['rpri']=pri-sPRI
daymean['rsify']=sify-sFY760
daymean['rlue']=lue-sLUE


ci=daymean['CI']
idx=ci>0.55
sunny=daymean[idx]
cloudy=daymean[~idx]
#sunny
sunny_doy=sunny['doy']
sunny_pri=sunny['PRI']
sunny_mtvi2=sunny['MTVI2']
sunny_sify=sunny['SIFyield']
sunny_lue=sunny['lue']
sunny_rpri=sunny['rpri']
sunny_rsify=sunny['rsify']
sunny_rlue=sunny['rlue']

#cloudy
cloudy_doy=cloudy['doy']
cloudy_pri=cloudy['PRI']
cloudy_mtvi2=cloudy['MTVI2']
cloudy_sify=cloudy['SIFyield']
cloudy_lue=cloudy['lue']
cloudy_rpri=cloudy['rpri']
cloudy_rsify=cloudy['rsify']

## Section02-计算rPRI和rFY760，求与LUE的相关性
## sifyield & lue
fig,axs=plt.subplots(1,1,figsize=(6,4))
# axs.scatter(sunny_lue, sunny_sify, color='r')
funcs_lzh.plot_xy(sunny_lue,sunny_sify,'LUE','SIFyield',axs)
axs.set_ylim([0,0.002])
axs.yaxis.set_major_formatter(fromatter)
# axs.set_xlabel('LUE')
# axs.set_ylabel('SIFyield')
# axs.set_ylim([-0.001,0.001])
## pri & mtvi2
fig,axs=plt.subplots(2,2,figsize=(12,8))
funcs_lzh.plot_xy(sunny_mtvi2, sunny_pri, 'MTVI2','PRI',axs[0,0])
funcs_lzh.plot_xy(sunny_mtvi2, sunny_rpri,'MTVI2','rPRI',axs[0,1])
axs[0,1].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_mtvi2,sunny_sify,'MTVI2','SIFyield',axs[1,0])
axs[1,0].set_ylim([0,0.0025])
axs[1,0].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_mtvi2,sunny_rsify,'MTVI2','rSIFyield',axs[1,1])
axs[1,1].set_ylim([-0.002,0.0025])
axs[1,1].yaxis.set_major_formatter(fromatter)
## rsify/rPRI & LUE
fig1,axs=plt.subplots(2,3,figsize=(12,8))
funcs_lzh.plot_xy(sunny_lue,sunny_rsify,'LUE','rSIFyield',axs[0,0])
axs[0,0].set_ylim([-0.002,0.0025])
axs[0,0].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_lue,sunny_rpri,'LUE','rPRI',axs[0,1])
axs[0,1].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_rpri,sunny_rsify,'rPRI','rSIFyield',axs[0,2])
axs[0,2].set_ylim([-0.002,0.0025])
axs[0,2].yaxis.set_major_formatter(fromatter)

# -------daymean--------------
data = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_daymean_sq2017corn.xlsx')
daymean = data.parse(0)
daymean['fPAR']=daymean['greenNDVI']
daymean['fPAR1']=daymean['APAR']/daymean['PAR']

daymean['SIFyield']=daymean['SFM']/(daymean['fPAR']*daymean['PAR'])
daymean['lue']=daymean['GPP']/(daymean['fPAR']*daymean['PAR'])
daymean=pd.concat([daymean['doy'],daymean['PRI'],daymean['MTVI2'],daymean['SIFyield'],daymean['lue'],daymean['CI']],axis=1)
daymean=daymean.dropna()

# doy=daymean['doy']
pri=daymean['PRI']
mtvi2=daymean['MTVI2']
sify=daymean['SIFyield']
lue=daymean['lue']
sPRI=0.1726*mtvi2-0.1346
sFY760=0.001*mtvi2**2+0.0006*mtvi2+0.0001
daymean['rpri']=pri-sPRI
daymean['rsify']=sify-sFY760

ci=daymean['CI']
idx=ci>0.55
sunny=daymean[idx]
cloudy=daymean[~idx]
#sunny
# sunny_doy=sunny['doy']
sunny_pri=sunny['PRI']
sunny_mtvi2=sunny['MTVI2']
sunny_sify=sunny['SIFyield']
sunny_lue=sunny['lue']
sunny_rpri=sunny['rpri']
sunny_rsify=sunny['rsify']

funcs_lzh.plot_xy(sunny_lue,sunny_rsify,'LUE','rSIFyield',axs[1,0])
axs[1,0].set_ylim([-0.002,0.0025])
axs[1,0].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_lue,sunny_rpri,'LUE','rPRI',axs[1,1])
axs[1,1].yaxis.set_major_formatter(fromatter)
funcs_lzh.plot_xy(sunny_rpri,sunny_rsify,'rPRI','rSIFyield',axs[1,2])
axs[1,2].set_ylim([-0.002,0.0025])
axs[1,2].yaxis.set_major_formatter(fromatter)

plt.show()