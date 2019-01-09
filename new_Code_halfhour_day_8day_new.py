#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-12 21:01:29
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


def funcp(p):
    if p < 0.001:
        return 0.001
    if p < 0.05 and p > 0.001:
        return 0.05
    if p > 0.05 and p < 0.1:
        return 0.1
    # if p > 0.1 and p < 1:
    #     return 1

def funcstar(p):
	if p<0.001:
		return '**'
	if p<0.05 and p>=0.001:
		return '*'
	else:
		return ''

def func(x, a, b, c):
    return a * np.power(x, b) + c
    # return a * x**b + c

# 线性回归
linreg = LinearRegression()

# 设置字体
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}
axis_font = {'fontname': 'Arial', 'size': 18,'color':'black'}
legend_font = {'fontname': 'Arial', 'size': 14}
marsize=8
lw=4
# tick_font = {'fontname': 'Times New Roman', 'size': 14, 'color': 'black'}
# legend_font = {'fontname': 'Times New Roman', 'size': 14, 'color': 'black'}

filepath = r'D:\Data\shangqiu data\shang\Results\GPP_PAR_APAR_SIF_8_18\ALLnew'

# daymean
data = pd.ExcelFile(
    filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_NIRv_CI_SIFyield_LUE_daymean_withnan.xlsx')
daymean = data.parse('Sheet1')
daymean = daymean.dropna()

sif1d = daymean['SFMlinear']
gpp1d = daymean['GPP']

# halfhour
data = pd.ExcelFile(
    filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_NIRv_CI_SIFyield_LUE_halfhour.xlsx')
hour = data.parse('Sheet1')

hour = hour.dropna()

sifhour = hour['SFMlinear']
gpphour = hour['GPP']

# 8daymean
data = pd.ExcelFile(
    filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_CI_SIFyield_LUE_8daymean_withnan.xlsx')
mean16 = data.parse('Sheet1')

sif16d = mean16['SFMlinear']
gpp16d = mean16['GPP']

# plot
fig, axs = plt.subplots(1, 3, figsize=(18, 5))
plt.subplots_adjust(bottom=0.14,top=0.91)

popt, pcov = curve_fit(func, sifhour, gpphour,maxfev=5000)  # popt 是拟合参数
temp = np.array(sifhour.copy())
temp.sort()
gpppred = func(temp, popt[0], popt[1], popt[2])
text = r"GPP=" + '%.3f' % popt[0] + ' x ' +\
    r'SIF^' + '%.3f' % popt[1] + '%.3f' % popt[2]
axs[0].plot(temp, gpppred, 'b', linewidth=lw)  # , label=text)
r, p = pearsonr(sifhour, gpphour)
r2 = '%.2f' % np.square(r)
text1 = r'0.5h: ' + '$R^2$= ' + r2 + funcstar(p)

# rmse='%.1f' % np.sqrt(((gpphour-gpppred)**2).mean())
# reg = linreg.fit(sifhour.values.reshape(-1, 1), gpphour)
# a, b = linreg.coef_, linreg.intercept_
# pred = reg.predict(sifhour.values.reshape(-1, 1))
# rmse1='%.1f' % np.sqrt(((gpphour-pred)**2).mean())
# axs[0].plot(sifhour.values.reshape(-1, 1), pred, color='orange',
#             linewidth=lw)  # , label=text)
# print(rmse,rmse1)

axs[0].scatter(sifhour, gpphour,
               edgecolors='b', facecolors='',marker='.', label=text)  # ,alpha=0.3

reg = linreg.fit(sif1d.values.reshape(-1, 1), gpp1d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif1d.values.reshape(-1, 1))
# 显示截距
print(reg.predict(0))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[0].plot(sif1d.values.reshape(-1, 1), pred, color='r',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif1d, gpp1d)
r2 = '%.2f' % np.square(r)
text2 = r'1d: ' + '$R^2$= ' + r2 + funcstar(p)+', k=' + '%.2f' % a 
axs[0].scatter(sif1d, gpp1d,
               edgecolors='r', facecolors='',marker='o', label=text)

reg = linreg.fit(sif16d.values.reshape(-1, 1), gpp16d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif16d.values.reshape(-1, 1))
# 显示截距
print(reg.predict(0))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[0].plot(sif16d.values.reshape(-1, 1), pred, color='k',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif16d, gpp16d)
r2 = '%.2f' % np.square(r)
text3 = r'8d: ' + '$R^2$= ' + r2 + funcstar(p)+', k=' + '%.2f' % a 
axs[0].plot(sif16d, gpp16d,
               color='k', marker='o', label=text,linestyle='',markersize=marsize)
axs[0].set_xlabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
axs[0].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[0].set_title('For all days', **title_font)
# axs[0].legend(frameon=True,loc=4,labelspacing=0.02,handletextpad=0.02,fontsize=11)
axs[0].tick_params(labelsize=18)
axs[0].set_xlim(0,np.max(sifhour)+0.1)
axs[0].set_ylim(0,np.max(gpphour)+5)
axs[0].text((np.max(sifhour)+0.1)*0.05,(np.max(gpphour)+5)*0.9,'(a)',**axis_font)
axs[0].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.18,text1,color='b',**legend_font)
axs[0].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.10,text2,color='r',**legend_font)
axs[0].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.02,text3,color='k',**legend_font)

## sunny and cloudy
sunny1d = daymean[daymean['CI'] >= 0.5]
cloudy1d = daymean[daymean['CI'] < 0.5]
sunnyh = hour[hour['CI'] >= 0.5]
cloudyh = hour[hour['CI'] < 0.5]
sunny16d = mean16[mean16['CI'] >= 0.5]
cloudy16d = mean16[mean16['CI'] < 0.5]

# sunny
sif1d = sunny1d['SFMlinear']
gpp1d = sunny1d['GPP']
sifhour = sunnyh['SFMlinear']
gpphour = sunnyh['GPP']
sif16d = sunny16d['SFMlinear']
gpp16d = sunny16d['GPP']

# plot
popt, pcov = curve_fit(func, sifhour, gpphour,maxfev=5000)  # popt 是拟合参数
temp = np.array(sifhour.copy())
temp.sort()
gpppred = func(temp, popt[0], popt[1], popt[2])
text = r"GPP=" + '%.3f' % popt[0] + ' x ' +\
    r'SIF^' + '%.3f' % popt[1] + '%.3f' % popt[2]
axs[1].plot(temp, gpppred, 'b', linewidth=lw)  # , label=text)
r, p = pearsonr(sifhour, gpphour)
r2 = '%.2f' % np.square(r)
text1 = r'0.5h: ' + '$R^2$= ' + r2 + funcstar(p)

# rmse='%.1f' % np.sqrt(((gpphour-gpppred)**2).mean())
# reg = linreg.fit(sifhour.values.reshape(-1, 1), gpphour)
# a, b = linreg.coef_, linreg.intercept_
# pred = reg.predict(sifhour.values.reshape(-1, 1))
# rmse1='%.1f' % np.sqrt(((gpphour-pred)**2).mean())
# axs[1].plot(sifhour.values.reshape(-1, 1), pred, color='orange',
#             linewidth=lw)  # , label=text)
# print(rmse,rmse1)

axs[1].scatter(sifhour, gpphour,
               edgecolors='b', facecolors='',marker='.', label=text)

reg = linreg.fit(sif1d.values.reshape(-1, 1), gpp1d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif1d.values.reshape(-1, 1))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[1].plot(sif1d.values.reshape(-1, 1), pred, color='r',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif1d, gpp1d)
r2 = '%.2f' % np.square(r)
text2 = r'1d: '+ '$R^2$= ' + r2 + funcstar(p)+', k=' + '%.2f' % a 
axs[1].scatter(sif1d, gpp1d,
               edgecolors='r', facecolors='',marker='o', label=text)

reg = linreg.fit(sif16d.values.reshape(-1, 1), gpp16d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif16d.values.reshape(-1, 1))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[1].plot(sif16d.values.reshape(-1, 1), pred, color='k',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif16d, gpp16d)
r2 = '%.2f' % np.square(r)
text3 = r'8d: ' + '$R^2$= ' + r2 + funcstar(p)+', k=' + '%.2f' % a 
axs[1].plot(sif16d, gpp16d,
               color='k', marker='o', label=text,linestyle='',markersize=marsize)
axs[1].set_xlabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
# axs[1].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[1].set_title('For clear sky days', **title_font)
# axs[1].legend(frameon=True,loc=4,labelspacing=0.02,handletextpad=0.02,fontsize=11)
axs[1].tick_params(labelsize=18)
axs[1].set_xlim(0,np.max(sifhour)+0.1)
axs[1].set_ylim(0,np.max(gpphour)+5)
axs[1].text((np.max(sifhour)+0.1)*0.05,(np.max(gpphour)+5)*0.9,'(b)',**axis_font)
axs[1].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.18,text1,color='b',**legend_font)
axs[1].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.10,text2,color='r',**legend_font)
axs[1].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.02,text3,color='k',**legend_font)

# cloudy
sif1d = cloudy1d['SFMlinear']
gpp1d = cloudy1d['GPP']
sifhour = cloudyh['SFMlinear']
gpphour = cloudyh['GPP']
sif16d = cloudy16d['SFMlinear']
gpp16d = cloudy16d['GPP']

# plot
popt, pcov = curve_fit(func, sifhour, gpphour,maxfev=5000)  # popt 是拟合参数
temp = np.array(sifhour.copy())
temp.sort()
gpppred = func(temp, popt[0], popt[1], popt[2])
text = r"GPP=" + '%.3f' % popt[0] + ' x ' +\
    r'SIF^' + '%.3f' % popt[1] + '%.3f' % popt[2]
axs[2].plot(temp, gpppred, 'b', linewidth=lw)  # , label=text)
r, p = pearsonr(sifhour, gpphour)
r2 = '%.2f' % np.square(r)
text1 = r'0.5h: ' + '$R^2$= ' + r2 + funcstar(p)

# rmse='%.1f' % np.sqrt(((gpphour-gpppred)**2).mean())
# reg = linreg.fit(sifhour.values.reshape(-1, 1), gpphour)
# a, b = linreg.coef_, linreg.intercept_
# pred = reg.predict(sifhour.values.reshape(-1, 1))
# rmse1='%.1f' % np.sqrt(((gpphour-pred)**2).mean())
# axs[2].plot(sifhour.values.reshape(-1, 1), pred, color='orange',
#             linewidth=lw)  # , label=text)
# print(rmse,rmse1)

axs[2].scatter(sifhour, gpphour,
               edgecolors='b', facecolors='',marker='.', label=text)

reg = linreg.fit(sif1d.values.reshape(-1, 1), gpp1d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif1d.values.reshape(-1, 1))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[2].plot(sif1d.values.reshape(-1, 1), pred, color='r',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif1d, gpp1d)
r2 = '%.2f' % np.square(r)
text2 = r'1d: '+ '$R^2$= ' + r2 + funcstar(p)+', k=' + '%.2f' % a 
axs[2].scatter(sif1d, gpp1d,
               edgecolors='r', facecolors='',marker='o', label=text)

reg = linreg.fit(sif16d.values.reshape(-1, 1), gpp16d)
a, b = linreg.coef_, linreg.intercept_
pred = reg.predict(sif16d.values.reshape(-1, 1))
# 显示截距
print(reg.predict(0))
text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
axs[2].plot(sif16d.values.reshape(-1, 1), pred, color='k',
            linewidth=lw)  # , label=text)
r, p = pearsonr(sif16d, gpp16d)
r2 = '%.2f' % np.square(r)
text3 = r'8d: ' + '$R^2$= ' + r2 + funcstar(p)+' , k=' + '%.2f' % a 
axs[2].plot(sif16d, gpp16d,
               color='k', marker='o', label=text,linestyle='',markersize=marsize)
axs[2].set_xlabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
# axs[2].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[2].set_title('For cloudy sky days', **title_font)
# axs[2].legend(frameon=True,loc=4,labelspacing=0.02,handletextpad=0.02,fontsize=11)
axs[2].tick_params(labelsize=18)
axs[2].set_xlim(0,np.max(sifhour)+0.1)
axs[2].set_ylim(0,np.max(gpphour)+5)
axs[2].text((np.max(sifhour)+0.1)*0.05,(np.max(gpphour)+5)*0.9,'(c)',**axis_font)
axs[2].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.18,text1,color='b',**legend_font)
axs[2].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.10,text2,color='r',**legend_font)
axs[2].text((np.max(sifhour)+0.1)*0.47,(np.max(gpphour)+5)*0.02,text3,color='k',**legend_font)


plt.show()
