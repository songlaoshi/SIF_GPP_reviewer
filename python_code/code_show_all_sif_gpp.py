#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-04 14:06:22
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

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 18}
legend_font = {'fontname': 'Arial', 'size': 14}
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}
ticklabelsize = 18
markersize = 8
linewidth = 3


def funcp(p):
    if p < 0.001:
        return 0.001
    if p < 0.05 and p > 0.001:
        return 0.05
    if p > 0.05 and p < 0.1:
        return 0.1
    else:
        return 1

a1 = 192
a2 = 205
a3 = 255
a4 = 283

#################### SIF&VPD halfhour #######################
filepath = r'D:\Data\shangqiu data\shang\results\GPP_PAr_APAr_SIF_8_18\ALLnew'

data = pd.ExcelFile(
    filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_NIRv_CI_SIFyield_LUE_halfhour.xlsx')
daymean = data.parse('Sheet1')
# daymean=pd.concat([daymean['DOY'],daymean['GPP'],daymean['SFMlinear'],daymean['CI']],axis=1)
daymean = daymean.dropna()

plt.figure(figsize=(15, 10))
doy = daymean['DOY']

plt.subplot(411)
# plt.scatter(daymean['DOY'],daymean['SFMlinear'])
plt.scatter(daymean.loc[doy < 215, 'DOY'],
            daymean.loc[doy < 215, 'SFMlinear'], marker='.')
plt.subplot(412)
plt.scatter(daymean.loc[(doy > 215) & (doy < 235), 'DOY'],
            daymean.loc[(doy > 215) & (doy < 235), 'SFMlinear'], marker='.')
plt.subplot(413)
plt.scatter(daymean.loc[(doy > 235) & (doy < 260), 'DOY'],
            daymean.loc[(doy > 235) & (doy < 260), 'SFMlinear'], marker='.')
plt.subplot(414)
plt.scatter(daymean.loc[doy >= 260, 'DOY'],
            daymean.loc[doy >= 260, 'SFMlinear'], marker='.')
plt.show()
