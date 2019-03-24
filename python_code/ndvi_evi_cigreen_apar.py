#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: ndvi_evi_cigreen_apar.py
@time: 2019/3/2 16:37
'''

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit
from scipy.stats.stats import pearsonr
from sklearn import metrics
from matplotlib import ticker

# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))


def funcp(p):
    if p < 0.001:
        return 0.001
    if p < 0.05 and p > 0.001:
        return 0.05
    if p > 0.05 and p < 0.1:
        return 0.1


def funcstar(p):
    if p < 0.001:
        return '**'
    if p < 0.05 and p >= 0.001:
        return '*'
    else:
        return ''


filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'

axis_font = {'fontname': 'Arial', 'size': 18}
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 18, }
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize = 18
markersize = 8
linewidth = 3
######################################################
fig, axs = plt.subplots(2, 2, figsize=(9.5, 9))
plt.subplots_adjust(wspace=0.29, hspace=0.29, top=0.86)
linreg = LinearRegression()
# ------------------------------------------
# data = pd.ExcelFile(
#     filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_SIF_VI_CI_SIFyield_LUE_daymean_withnan-SIFyield delete d192-vi delete.xlsx')
data = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_daymean_sq2017corn.xlsx')
daymean = data.parse('Sheet1')

daymean1 = pd.concat([daymean['SFMSIFyield'], daymean['LUE']], axis=1)
daymean1 = daymean1.dropna()
daymean2 = pd.concat(
    [daymean['PAR'], daymean['SFM'], daymean['GPP'], daymean['NDVI'], daymean['EVI'], daymean['CVI']], axis=1)
daymean2 = daymean2.dropna()

PAR = daymean2['PAR']
print(PAR.shape)
# APAR = daymean['APAR']
SIF = daymean2['SFM']
GPP = daymean2['GPP']
CIgreen = daymean2['CVI']
NDVI = daymean2['NDVI']
EVI = daymean2['EVI']
# irrigated
fAPARchl_ndvi = 1.1 * NDVI - 0.27
fAPARchl_evi = 1.29 * EVI - 0.16
# fAPARchl_CIgreen = 0.12 * CIgreen - 0.1
fAPARchl_CIgreen = CIgreen

APARchl_ndvi = fAPARchl_ndvi * PAR
APARchl_evi = fAPARchl_evi * PAR
APARchl_CIgreen = fAPARchl_CIgreen * PAR

## -------------------SIF and GPP------------------------------
SIFyield = daymean1['SFMSIFyield']
LUE = daymean1['LUE']

p1, = axs[0, 0].plot(LUE, SIFyield,
                     color='k', marker='o', linestyle='', label='', markersize=markersize)
reg = linreg.fit(LUE.values.reshape(-1, 1), SIFyield)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(LUE.values.reshape(-1, 1))
text = 'y=' + '%.4f' % a + 'x' + '+' + '%.4f' % b
r, p = pearsonr(LUE, SIFyield)
r2 = '%.2f' % np.square(r)
text1 = r'$R^2$= ' + r2 + funcstar(p)
axs[0, 0].plot(LUE.values.reshape(-1, 1), pred,
               color='k', linewidth=2, label=text1)

axs[0, 0].set_xlabel(r"$GPP/APAR_{canopy}$", **axis_font)
axs[0, 0].set_ylabel(r"$SIF/APAR_{canopy}$", **axis_font)
# axs[0,1].set_xlabel(r"LUE",**axis_font)
# axs[0,1].set_ylabel(r"SIF$_{yield}$",**axis_font)
axs[0, 0].yaxis.set_major_formatter(fromatter)
# axs[0,1].set_ylim(0,1.1)
# axs[0,1].set_xlim(0,1.1)
axs[0, 0].tick_params(labelsize=ticklabelsize)
axs[0, 0].text((np.max(LUE) + 0.05) * 0.76, (np.max(SIFyield) + 0.0005) * 0.82, '(a)', **axis_font)
axs[0, 0].text(0, (np.max(SIFyield) + 0.0005) * 0.82, text1, color='k', **legend_font)
axs[0, 0].set_yticks([0, 0.001, 0.002, 0.003])
# --------------------NDVI---------------------------
## -------------------SIF and GPP------------------------------
SIFyield = SIF / APARchl_ndvi
LUE = GPP / APARchl_ndvi
p1, = axs[1, 0].plot(LUE, SIFyield,
                     color='k', marker='o', linestyle='', label='', markersize=markersize)
reg = linreg.fit(LUE.values.reshape(-1, 1), SIFyield)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(LUE.values.reshape(-1, 1))
text = 'y=' + '%.4f' % a + 'x' + '+' + '%.4f' % b
r, p = pearsonr(LUE, SIFyield)
r2 = '%.2f' % np.square(r)
text1 = r'$R^2$= ' + r2 + funcstar(p)
axs[1, 0].plot(LUE.values.reshape(-1, 1), pred,
               color='k', linewidth=2, label=text1)

axs[1, 0].set_xlabel(r"$GPP/APAR_{NDVI}$", **axis_font)
axs[1, 0].set_ylabel(r"$SIF/APAR_{NDVI}$", **axis_font)
axs[1, 0].yaxis.set_major_formatter(fromatter)
# axs[1,0].set_ylim(0,np.max(SIFyield)+0.0005)
# axs[1,0].set_xlim(0,np.max(LUE)+0.05)
axs[1, 0].tick_params(labelsize=ticklabelsize)
axs[1, 0].text((np.max(LUE) + 0.05) * 0.64, (np.max(SIFyield) + 0.0005) * 0.83, '(c)', **axis_font)
axs[1, 0].text((np.max(LUE) + 0.05) * 0.03, (np.max(SIFyield) + 0.0005) * 0.83, text1, color='k', **legend_font)
# axs[1,0].set_yticks([0,0.003,0.006,0.009])
# -----------------------------------------------
## -------------------SIF and GPP------------------------------
SIFyield = SIF / APARchl_evi
LUE = GPP / APARchl_evi
p1, = axs[1, 1].plot(LUE, SIFyield,
                     color='k', marker='o', linestyle='', label='', markersize=markersize)
reg = linreg.fit(LUE.values.reshape(-1, 1), SIFyield)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(LUE.values.reshape(-1, 1))
text = 'y=' + '%.4f' % a + 'x' + '+' + '%.4f' % b
r, p = pearsonr(LUE, SIFyield)
r2 = '%.2f' % np.square(r)
text1 = r'$R^2$= ' + r2 + funcstar(p)
axs[1, 1].plot(LUE.values.reshape(-1, 1), pred,
               color='k', linewidth=2, label=text1)

axs[1, 1].set_xlabel(r"$GPP/APAR_{EVI}$", **axis_font)
axs[1, 1].set_ylabel(r"$SIF/APAR_{EVI}$", **axis_font)
axs[1, 1].yaxis.set_major_formatter(fromatter)
# axs[1,1].set_ylim(0,np.max(SIFyield)+0.0005)
# axs[1,1].set_xlim(0,np.max(LUE)+0.05)
axs[1, 1].tick_params(labelsize=ticklabelsize)
axs[1, 1].text((np.max(LUE) + 0.05) * 0.64, (np.max(SIFyield) + 0.0005) * 0.84, '(d)', **axis_font)
axs[1, 1].text((np.max(LUE) + 0.05) * 0.04, (np.max(SIFyield) + 0.0005) * 0.84, text1, color='k', **legend_font)
axs[1, 1].set_xticks([0, 0.05, 0.1])
# -----------------------------------------------
## -------------------SIF and GPP------------------------------
SIFyield = SIF / APARchl_CIgreen
LUE = GPP / APARchl_CIgreen

p1, = axs[0, 1].plot(LUE, SIFyield,
                     color='k', marker='o', linestyle='', label='', markersize=markersize)
reg = linreg.fit(LUE.values.reshape(-1, 1), SIFyield)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(LUE.values.reshape(-1, 1))
text = 'y=' + '%.4f' % a + 'x' + '+' + '%.4f' % b
r, p = pearsonr(LUE, SIFyield)
r2 = '%.2f' % np.square(r)
text1 = r'$R^2$= ' + r2 + funcstar(p)
axs[0, 1].plot(LUE.values.reshape(-1, 1), pred,
               color='k', linewidth=2, label=text1)

axs[0, 1].set_xlabel(r"$GPP/APAR_{green}$", **axis_font)
axs[0, 1].set_ylabel(r"$SIF/APAR_{green}$", **axis_font)
axs[0, 1].yaxis.set_major_formatter(fromatter)
# axs[1,2].set_ylim(0,np.max(SIFyield)+0.0005)
# axs[1,2].set_xlim(0,np.max(LUE)+0.05)
axs[0, 1].tick_params(labelsize=ticklabelsize)
axs[0, 1].text((np.max(LUE) + 0.05) * 0.85, (np.max(SIFyield) + 0.0005) * 0.89, '(b)', **axis_font)
axs[0, 1].text((np.max(LUE) + 0.05) * 0.03, (np.max(SIFyield) + 0.0005) * 0.89, text1, color='k', **legend_font)
# axs[1,2].set_yticks([0,0.003,0.006,0.009])

# axs[0,0].remove()
# axs[0,2].remove()

plt.show()