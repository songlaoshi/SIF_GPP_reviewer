#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: Plot_allparas.py
@time: 2019/3/1 17:22
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker
import funcs_lzh

def MaxMinNormalization(x,max,min):
    x=(x-min)/(max-min)
    return x

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

alphadot=0.5

axis_font = {'fontname': 'Arial', 'size': 10, 'color': 'black'}
ticklabelsize = 14
a1 = 192
a2 = 205
a3 = 255
a4 = 283

filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
figsavepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\result_figs'

datahalf=pd.ExcelFile(filepath+'\SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
datahalf=datahalf.parse(0)

##
# vpd=datahalf['VPD']
# scaled_vpd=MaxMinNormalization(vpd,np.max(vpd),np.min(vpd))
# ta=datahalf['Ta']
# scaled_ta=MaxMinNormalization(ta,np.max(ta),np.min(ta))
# apar=datahalf['APARgndvi']
# scaled_apar=MaxMinNormalization(apar,np.max(apar),np.min(apar))
# ECI=scaled_apar+scaled_ta+scaled_vpd
# datahalf['ECI']=MaxMinNormalization(ECI,np.max(ECI),np.min(ECI))
# datahalf.to_csv(filepath+'\SIF_GPP_VI_ref_halfhourmean_sq2017corn_addECI.csv',index=False,header=True)
#

## 计算太阳天顶角
# doy=list(map(int,data['doy'].values))
# hour=data['hour'].values
# sza=[]
# for i in range(len(hour)):
#     d=doy[i]
#     h=hour[i]
#     temp=funcs_lzh.get_solar_zenith_angle(115.5916,34.5199,d,h)
#     sza.append(temp)
#
# plt.plot(sza)
# plt.show()
##
#
day=pd.ExcelFile(filepath+'\SIF_GPP_VI_ref_daymean_sq2017corn.xlsx')
daymean=day.parse(0)
daystd=day.parse(1)
# ##
#
doyhalf=datahalf['doy']
vpdhalf=datahalf['VPD']
tahalf=datahalf['Ta']
sifhalf=datahalf['SFM']
gpphalf=datahalf['GPP']
parhalf=datahalf['PAR']
aparhalf=datahalf['APAR']
sifyieldhalf=datahalf['SFMSIFyield']
luehalf=datahalf['LUE']
mtcihalf=datahalf['MTCI']
MTVI2half=datahalf['MTVI2']
prihalf=datahalf['PRI']
cigreenhalf=datahalf['CIgreen']
cvihalf=datahalf['CVI']
ecihalf=datahalf['ECI']
#
# daily mean
doymean=daymean['doy']
vpdmean=daymean['VPD']
tamean=daymean['Ta']
sifmean=daymean['SFM']
gppmean=daymean['GPP']
parmean=daymean['PAR']
aparmean=daymean['APAR']
sifyieldmean=daymean['SFMSIFyield']
luemean=daymean['LUE']
mtcimean=daymean['MTCI']
MTVI2mean=daymean['MTVI2']
primean=daymean['PRI']
cigreenmean=daymean['CIgreen']
cvimean=daymean['CVI']
ecimean=daymean['ECI']
# std
vpdstd=daystd['VPD']
tastd=daystd['Ta']
sifstd=daystd['SFM']
gppstd=daystd['GPP']
parstd=daystd['PAR']
aparstd=daystd['APAR']
sifyieldstd=daystd['SFMSIFyield']
luestd=daystd['LUE']
mtcistd=daystd['MTCI']
MTVI2std=daystd['MTVI2']
pristd=daystd['PRI']
cigreenstd=daystd['CIgreen']
cvistd=daystd['CVI']
ecistd=daystd['ECI']
# #
fig, axs = plt.subplots(5,1,sharex=True,figsize=(10, 15))
fig.subplots_adjust(hspace=0)
#
#

axs[0].scatter(doyhalf,ecihalf,marker='.',edgecolors='',facecolors='k',alpha=alphadot)
axs[0].errorbar(doymean,ecimean,yerr=ecistd,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs[0].set_ylabel('ECI [-]',**axis_font)
twinx1=axs[0].twinx()
twinx1.fill_between(doymean,0,parmean,facecolors='orange',edgecolors='',alpha=0.1)
twinx1.set_ylabel('PAR '+'\n'+'[umol/m2/s]')

axs[1].scatter(doyhalf,sifhalf,marker='.',edgecolors='',facecolors='k',alpha=alphadot)
axs[1].errorbar(doymean,sifmean,yerr=sifstd,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs[1].set_ylabel('SIF'+'\n'+'[mW/m2/nm/sr]',**axis_font)

axs[2].scatter(doyhalf,gpphalf,marker='.',edgecolors='',facecolors='k',alpha=alphadot)
axs[2].errorbar(doymean,gppmean,yerr=gppstd,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs[2].set_ylabel('GPP'+'\n'+'[umol/m2/s]',**axis_font)
axs[3].scatter(doyhalf,sifyieldhalf,marker='.',edgecolors='',facecolors='k',alpha=alphadot)
axs[3].errorbar(doymean,sifyieldmean,yerr=sifyieldstd,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs[3].set_ylabel('SIFyield [-]',**axis_font)
axs1=axs[3].twinx()
axs1.scatter(doyhalf,luehalf,marker='.',edgecolors='',facecolors='r',alpha=alphadot)
axs1.errorbar(doymean,luemean,yerr=luestd,marker='o',markeredgecolor='r',markerfacecolor='r',linestyle='')
axs1.set_ylabel('LUE [-]',**axis_font)
axs[4].scatter(doyhalf,MTVI2half,marker='.',edgecolors='',facecolors='k',alpha=alphadot)
# axs[4].errorbar(doymean,MTVI2mean,yerr=MTVI2std,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs[4].set_ylabel('MTVI2 [-]',**axis_font)
axs2=axs[4].twinx()
axs2.scatter(doyhalf,prihalf,marker='.',edgecolors='',facecolors='r',alpha=alphadot)
# axs2.errorbar(doymean,primean,yerr=pristd,marker='o',markeredgecolor='k',markerfacecolor='k',linestyle='')
axs2.set_ylabel('PRI [-]',**axis_font)

axs[4].set_xlabel('DOY',**axis_font)
plt.show()



