#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-11-03 14:16:17
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

filepath = r'D:\Data\shangqiu data\shang\Results\GPP_PAR_APAR_SIF_8_18\ALLnew'


sunny = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_sunny_0.7.xlsx', header=None)
cloudy = pd.read_excel(
    filepath + '\\' + r'SIF_PAR_cloudy_0.7.xlsx', header=None)
data = pd.read_excel(
    filepath + '\\' + r'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_0.7.xlsx')

sunny = np.array(sunny)
cloudy = np.array(cloudy)
##
sunnyx = []
for i in range(sunny.shape[0]):
    sunnyy = []
    for j in range(0, sunny.shape[1], 5):
        sunnyy.append(np.nanmean(sunny[i, j:j + 5]))
    sunnyx.append(sunnyy)
cloudyx = []
for i in range(cloudy.shape[0]):
    cloudyy = []
    for j in range(0, cloudy.shape[1], 10):
        cloudyy.append(np.nanmean(cloudy[i, j:j + 10]))
    cloudyx.append(cloudyy)


# print(cloudyx)

##
fig, axs = plt.subplots(2, 2, figsize=(11, 8))
fig.subplots_adjust(wspace=0.3)
# fig.tight_layout()
linreg = LinearRegression()
# plot number 1
mory = np.array([])
morx = np.array([])
for i in range(0, 10):
    mory = np.hstack((mory, np.array(sunnyx[i])))
    morx = np.hstack((morx, np.array(sunnyx[i + 20])))
# print(mory)
time2 = np.array([])
for j in np.arange(8, 13, 0.5):
    time1 = [np.array(j)] * 5
    time2 = np.hstack((time2, time1))
# print(time2)
p1 = axs[0, 0].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)

cbar = fig.colorbar(p1, ax=axs.ravel().tolist())
cbar.set_label('Hour of day', rotation=90, **axis_font)
cbar.ax.set_yticklabels(['8','10','12','14','16','18'],**axis_font)

reg = linreg.fit(morx.reshape(-1, 1), mory)
a1, b = linreg.coef_, linreg.intercept_
# print(a,b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a1 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text1 = '$R^2$= ' + r2 + funcstar(p)+',' + 'k=' + '%.1e' % a1
# p2, = axs[0, 0].plot(morx.reshape(-1, 1), pred,
#                      color='b', linewidth=linewidth, label=text1)
print(b)
mory = np.array([])
morx = np.array([])
for i in range(10, 20):
    mory = np.hstack((mory, np.array(sunnyx[i])))
    morx = np.hstack((morx, np.array(sunnyx[i + 20])))
time2 = np.array([])
for j in np.arange(13, 18, 0.5):
    time1 = [np.array(j)] * 5
    time2 = np.hstack((time2, time1))
p3 = axs[0, 0].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
#
reg = linreg.fit(morx.reshape(-1, 1), mory)
a2, b = linreg.coef_, linreg.intercept_
# print(a,b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a2 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text2 = '$R^2$= ' + r2 +  funcstar(p)+',' + 'k=' + '%.1e' % a2
# p4, = axs[0, 0].plot(morx.reshape(-1, 1), pred,
#                      color='r', linewidth=linewidth, label=text2)
print(b)
# ## ---------------------------------
datax = data['sunnypar']
datay = data['sunnysif']
time1 = np.arange(8, 13, 0.5)
time2 = np.arange(13, 18, 0.5)

p5 = axs[0, 0].scatter(datax.loc[0:9], datay.loc[0:9],
                       c=time1, vmin=8,vmax=18, cmap='bwr', edgecolors='k', marker='o', s=60,)
p6 = axs[0, 0].scatter(datax.loc[10:20], datay.loc[10:20],
                       c=time2, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)
axs[0,0].vlines(1070,0,0.88,color='k',linestyle=':',linewidth=2)
axs[0,0].hlines(0.88,0,1070,color='k',linestyle=':',linewidth=2)
axs[0,0].hlines(0.66,0,1070,color='k',linestyle=':',linewidth=2)
# axs[0, 0].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
axs[0, 0].set_ylabel(r"SIF " + "$[mW/m^2/nm/sr]$", **axis_font)
axs[0, 0].tick_params(labelsize=ticklabelsize)
axs[0,0].set_ylim(0,2)
axs[0,0].set_xlim(0,1900)
axs[0,0].text(1900*0.05,2*0.9,'(a) Sunny days',**axis_font)
axs[0,0].text(1900*0.05,2*0.8,text1,color='b',**legend_font)
axs[0,0].text(1900*0.05,2*0.7,text2,color='r',**legend_font)
# axs[0,0].text(1900*0.05,2*0.6,'%.2f'%((a1-a2)/a2*100),color='r',**legend_font)
# plot number 2
mory = np.array([])
morx = np.array([])
for i in range(0, 10):
    mory = np.hstack((mory, np.array(cloudyx[i])))
    morx = np.hstack((morx, np.array(cloudyx[i + 20])))
morx = morx[~np.isnan(mory)]
mory = mory[~np.isnan(mory)]
# print(np.isnan(mory))

time2 = np.array([])
for j in np.arange(8, 13, 0.5):
    if j == np.array(8.5):
        time1 = [np.array(j)] * 6
        time2 = np.hstack((time2, time1))
    else:
        time1 = [np.array(j)] * 7
        time2 = np.hstack((time2, time1))

# print(time2)
p1 = axs[0, 1].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
reg = linreg.fit(morx.reshape(-1, 1), mory)
a1, b = linreg.coef_, linreg.intercept_
# print(a, b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a1 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text1 = '$R^2$= ' + r2 + funcstar(p)+',' +'k=' + '%.1e' % a1
# p2, = axs[0, 1].plot(morx.reshape(-1, 1), pred,
#                      color='b', linewidth=linewidth, label=text1)

mory = np.array([])
morx = np.array([])
for i in range(10, 20):
    mory = np.hstack((mory, np.array(cloudyx[i])))
    morx = np.hstack((morx, np.array(cloudyx[i + 20])))
print(morx)
time2 = np.array([])
for j in np.arange(13, 18, 0.5):
    time1 = [np.array(j)] * 7
    time2 = np.hstack((time2, time1))
p3 = axs[0, 1].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
#
reg = linreg.fit(morx.reshape(-1, 1), mory)
a2, b = linreg.coef_, linreg.intercept_
# print(a, b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a2 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text2 = '$R^2$= ' + r2 + funcstar(p)+','+ 'k=' + '%.1e' % a2
# p4, = axs[0, 1].plot(morx.reshape(-1, 1), pred,
#                      color='r', linewidth=linewidth, label=text2)

# ## ---------------------------------
datax = data['cloudypar']
datay = data['cloudysif']
time1 = np.arange(8, 13, 0.5)
time2 = np.arange(13, 18, 0.5)

p5 = axs[0, 1].scatter(datax.loc[0:9], datay.loc[0:9],
                       c=time1, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)
p6 = axs[0, 1].scatter(datax.loc[10:20], datay.loc[10:20],
                       c=time2, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)

# axs[0, 1].set_xlabel(r"PAR " +"$[μmol /m^2/s]$", **axis_font)
# axs[0, 1].set_ylabel(r"SIF "+ "$[mW/m^2/nm/sr]$", **axis_font)
axs[0, 1].tick_params(labelsize=ticklabelsize)
axs[0,1].set_ylim(0,1)
axs[0,1].set_xlim(0,1300)
axs[0,1].text(1300*0.05,1*0.9,'(b) Cloudy days',**axis_font)
axs[0,1].text(1300*0.05,1*0.8,text1,color='b',**legend_font)
axs[0,1].text(1300*0.05,1*0.7,text2,color='r',**legend_font)
# axs[0,1].text(1300*0.05,1*0.6,'%.2f'%((a1-a2)/a2*100),color='r',**legend_font)
# -------------------GPP_PAR------------------------------
sunny = pd.read_excel(
    filepath + '\\' + r'GPP_PAR_sunny_0.7.xlsx', header=None)
cloudy = pd.read_excel(
    filepath + '\\' + r'GPP_PAR_cloudy_0.7.xlsx', header=None)
data = pd.read_excel(
    filepath + '\\' + r'SIF_GPP_VPD_Ta_PAR_APAR_morning_afternoon_0.7.xlsx')

sunny = np.array(sunny)
cloudy = np.array(cloudy)
##
sunnyx = []
for i in range(sunny.shape[0]):
    sunnyy = []
    for j in range(0, sunny.shape[1], 5):
        sunnyy.append(np.nanmean(sunny[i, j:j + 5]))
    sunnyx.append(sunnyy)
cloudyx = []
for i in range(cloudy.shape[0]):
    cloudyy = []
    for j in range(0, cloudy.shape[1], 10):
        cloudyy.append(np.nanmean(cloudy[i, j:j + 10]))
    cloudyx.append(cloudyy)

# plot number 1
mory = np.array([])
morx = np.array([])
for i in range(0, 10):
    mory = np.hstack((mory, np.array(sunnyx[i])))
    morx = np.hstack((morx, np.array(sunnyx[i + 20])))
# print(mory)
time2 = np.array([])
for j in np.arange(8, 13, 0.5):
    time1 = [np.array(j)] * 5
    time2 = np.hstack((time2, time1))
# print(time2)
p1 = axs[1, 0].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)

reg = linreg.fit(morx.reshape(-1, 1), mory)
a1, b = linreg.coef_, linreg.intercept_
# print(a,b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a1 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text1 = '$R^2$= ' + r2 + funcstar(p)+','+ 'k=' + '%.1e' % a1
# p2, = axs[1, 0].plot(morx.reshape(-1, 1), pred,
#                      color='b', linewidth=linewidth, label=text1)

mory = np.array([])
morx = np.array([])
for i in range(10, 20):
    mory = np.hstack((mory, np.array(sunnyx[i])))
    morx = np.hstack((morx, np.array(sunnyx[i + 20])))
time2 = np.array([])
for j in np.arange(13, 18, 0.5):
    time1 = [np.array(j)] * 5
    time2 = np.hstack((time2, time1))
p3 = axs[1, 0].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
#
reg = linreg.fit(morx.reshape(-1, 1), mory)
a2, b = linreg.coef_, linreg.intercept_
# print(a,b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a2 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text2 = '$R^2$= ' + r2 + funcstar(p)+','+ 'k=' + '%.1e' % a2
# p4, = axs[1, 0].plot(morx.reshape(-1, 1), pred,
#                      color='r', linewidth=linewidth, label=text2)

# ## ---------------------------------
datax = data['sunnypar']
datay = data['sunnygpp']
time1 = np.arange(8, 13, 0.5)
time2 = np.arange(13, 18, 0.5)

p5 = axs[1, 0].scatter(datax.loc[0:9], datay.loc[0:9],
                       c=time1, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)
p6 = axs[1, 0].scatter(datax.loc[10:20], datay.loc[10:20],
                       c=time2, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)
axs[1,0].vlines(1070,0,43,color='k',linestyle=':',linewidth=2)
axs[1,0].hlines(43,0,1070,color='k',linestyle=':',linewidth=2)
axs[1,0].hlines(40,0,1070,color='k',linestyle=':',linewidth=2)
axs[1, 0].set_xlabel(r"PAR " + "$[μmol /m^2/s]$", **axis_font)
axs[1, 0].set_ylabel(r"GPP " + "$[μmol CO_2/m^2/s]$", **axis_font)
axs[1, 0].tick_params(labelsize=ticklabelsize)
axs[1,0].set_ylim(0,80)
axs[1,0].set_xlim(0,1900)
axs[1,0].text(1900*0.05,80*0.9,'(c) Sunny days',**axis_font)
axs[1,0].text(1900*0.05,80*0.8,text1,color='b',**legend_font)
axs[1,0].text(1900*0.05,80*0.7,text2,color='r',**legend_font)
# axs[1,0].text(1900*0.05,80*0.6,'%.2f'%((a1-a2)/a2*100),color='r',**legend_font)
# plot number 2
mory = np.array([])
morx = np.array([])
for i in range(0, 10):
    mory = np.hstack((mory, np.array(cloudyx[i])))
    morx = np.hstack((morx, np.array(cloudyx[i + 20])))
# morx=morx[~np.isnan(mory)]
# mory=mory[~np.isnan(mory)]
# print(np.isnan(mory))

time2 = np.array([])
for j in np.arange(8, 13, 0.5):
    time1 = [np.array(j)] * 7
    time2 = np.hstack((time2, time1))

# print(time2)
p1 = axs[1, 1].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
reg = linreg.fit(morx.reshape(-1, 1), mory)
a1, b = linreg.coef_, linreg.intercept_
# print(a, b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a1 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text1 = '$R^2$= ' + r2 + funcstar(p)+','+ 'k=' + '%.1e' % a1
# p2, = axs[1, 1].plot(morx.reshape(-1, 1), pred,
#                      color='b', linewidth=linewidth, label=text1)

mory = np.array([])
morx = np.array([])
for i in range(10, 20):
    mory = np.hstack((mory, np.array(cloudyx[i])))
    morx = np.hstack((morx, np.array(cloudyx[i + 20])))
print(morx)
time2 = np.array([])
for j in np.arange(13, 18, 0.5):
    time1 = [np.array(j)] * 7
    time2 = np.hstack((time2, time1))
p3 = axs[1, 1].scatter(morx, mory, c=time2, vmin=8,
                       vmax=18, cmap='bwr', marker='o',s=markersize,alpha=0.5)
#
reg = linreg.fit(morx.reshape(-1, 1), mory)
a2, b = linreg.coef_, linreg.intercept_
# print(a, b)
pred = reg.predict(morx.reshape(-1, 1))
text = 'y=' + '%.4f' % a2 + 'x' + '+' + '%.4f' % b
r, p = pearsonr(morx, mory)
r2 = '%.2f' % np.square(r)
text2 = '$R^2$= ' + r2 + funcstar(p)+','+ 'k=' + '%.1e' % a2
# p4, = axs[1, 1].plot(morx.reshape(-1, 1), pred,
#                      color='r', linewidth=linewidth, label=text2)

# ## ---------------------------------
datax = data['cloudypar']
datay = data['cloudygpp']
time1 = np.arange(8, 13, 0.5)
time2 = np.arange(13, 18, 0.5)

p5 = axs[1, 1].scatter(datax.loc[0:9], datay.loc[0:9],
                       c=time1, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)
p6 = axs[1, 1].scatter(datax.loc[10:20], datay.loc[10:20],
                       c=time2, vmin=8,vmax=18, cmap='bwr',  edgecolors='k', marker='o', s=60)

axs[1, 1].set_xlabel(r"PAR " + "$[μmol /m^2/s]$", **axis_font)
axs[1, 1].tick_params(labelsize=ticklabelsize)
axs[1,1].set_ylim(0,60)
axs[1,1].set_xlim(0,1300)
axs[1,1].text(1300*0.05,60*0.9,'(d) Cloudy days',**axis_font)
axs[1,1].text(1300*0.05,60*0.8,text1,color='b',**legend_font)
axs[1,1].text(1300*0.05,60*0.7,text2,color='r',**legend_font)
# axs[1,1].text(1300*0.05,60*0.6,'%.2f'%((a1-a2)/a2*100),color='r',**legend_font)

plt.show()
