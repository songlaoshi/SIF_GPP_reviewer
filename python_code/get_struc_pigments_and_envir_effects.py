#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_struc&pigments_and_envir_effects.py
@time: 2019/4/9 19:58
'''
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
# from sklearn import preprocessing
from scipy.optimize import curve_fit
import math
from mpl_toolkits.mplot3d import Axes3D
import funcs_lzh
from scipy.stats.stats import pearsonr
from matplotlib import ticker

linreg = LinearRegression()


def get_a_b_r2score(x, y):
    reg = linreg.fit(x, y)
    a, b = linreg.coef_, linreg.intercept_
    pred = reg.predict(x)
    r2score = r2_score(y, pred)
    return a, b, r2score, pred

def get_pearsonr(x, y):
    r, p = pearsonr(x, y)  # 相关系数
    return r, p

# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize = 14
title_font = {'fontname': 'Times New Roman', 'size': 18, 'color': 'black',
              'weight': 'normal', 'verticalalignment': 'bottom'}

def plot_01(axs, x, y, c, xlabel, ylabel):
    r, p = get_pearsonr(x, y)
    p = axs.scatter(x, y, c=c, cmap='jet', marker='.', label='r= %.2f' % r + funcs_lzh.funcstar(p))
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)
    axs.legend()
    return p

def scatterplot(ax,x,y,c,xlim_range,ylim_range):
    r, p = get_pearsonr(x, y)
    label = 'r= %.2f' % r + funcs_lzh.funcstar(p)
    p=ax.scatter(x, y, c=c, vmin=0, vmax=1, cmap='jet', marker='o', label=label)
    ax.set_xlim(xlim_range)
    ax.set_ylim(ylim_range)
    return p

def scatterplot1(ax,x,y,xlim_range,ylim_range,marker,color,range_label):
    reg = linreg.fit(x.values.reshape(-1, 1), y)
    a, b = linreg.coef_, linreg.intercept_
    pred = reg.predict(x.values.reshape(-1, 1))
    text = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
    ax.plot(x.values.reshape(-1, 1), pred,
             color=color, linewidth=1, label='')
    r, p = get_pearsonr(x, y)
    label = 'R$^2$= %.2f' % np.square(r) + funcs_lzh.funcstar(p)
    p=ax.scatter(x, y, marker=marker, facecolor='',edgecolor=color,label=label+', '+range_label)
    ax.set_xlim(xlim_range)
    ax.set_ylim(ylim_range)
    return p

# growth stage
a1 = 192.0
a2 = 205.0
a3 = 255.0
a4 = 283.0
parthred1 = 450.0
parthred2 = 700.0
cithred1 = 0.4
cithred2 = 0.6
ecithred1 = 0.6
ecithred2 = 0.8
# daymean
filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
# daymean = pd.read_csv(
#     filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn_8-18_addSZA_norain.csv')
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_daymean_sq2017corn_8-18_addSZA_norain.xlsx')
daymean=daymean.parse(0)
# 去掉SZA>60的数据
daymean=daymean[daymean['SZA']<60]
# 选取晴天数据
daymean=daymean[daymean['CI']>0.5]
#
daymean = pd.concat([daymean['DOY'], daymean['hour'], daymean['MTVI2'], daymean['CIgreen'],daymean['EVI']
                        , daymean['rededgeNDVI'],daymean['greenNDVI'],daymean['SFMlinear'], daymean['GPP'], daymean['PAR'],daymean['CI']
                        , daymean['VPD'], daymean['Ta'], daymean['PRI'],daymean['CI']], axis=1)
daymean = daymean.dropna()


# 使用一个scaled的EVI当做fAPAR
# fAPARchl_evi = 1.29 * daymean['EVI'] - 0.16
daymean['apar'] = daymean['rededgeNDVI']* daymean['PAR']
# daymean['apar'] = (1.29 * daymean['EVI'] - 0.16 )* daymean['PAR']

# 计算ECI
daymean['scaled_APAR'] = funcs_lzh.MaxMinNormalization(daymean['apar'], np.max(daymean['apar']), np.min(daymean['apar']))
daymean['scaled_VPD'] = funcs_lzh.MaxMinNormalization(daymean['VPD'], np.max(daymean['VPD']), np.min(daymean['VPD']))
daymean['scaled_Ta'] = funcs_lzh.MaxMinNormalization(daymean['Ta'], np.max(daymean['Ta']), np.min(daymean['Ta']))
daymean['eci'] = daymean['scaled_APAR'] + daymean['scaled_VPD'] + daymean['scaled_Ta']
daymean['ECI'] = funcs_lzh.MaxMinNormalization(daymean['eci'], np.max(daymean['eci']), np.min(daymean['eci']))
# 计算光合和荧光效率
daymean['sify'] = daymean['SFMlinear']/daymean['apar']
daymean['lue'] = daymean['GPP']/daymean['apar']
# 去掉LUE异常值
daymean.loc[daymean['lue']>0.15,'lue']=np.nan
daymean=daymean.dropna()
# 去掉structural and pigment effects
meanMTVI2=np.mean(daymean['MTVI2'])
daymean['scaled_MTVI2']=daymean['MTVI2']/meanMTVI2
daymean['rsify']=daymean['sify']/daymean['scaled_MTVI2']
###################
eci1=0.4
eci2=0.9
mtvi21=0.4
mtvi22=0.6
idx1=(daymean['ECI']<= eci1)
idx11=(daymean['ECI']> eci2)
idx2=(daymean['MTVI2']<=mtvi21)
idx21=(daymean['MTVI2']>mtvi22)
##################
fig, axs = plt.subplots(3, 2, figsize=(10, 4.5))
fig.subplots_adjust(hspace=0,bottom=0.16,wspace=0.29)

ax=plt.subplot(121)
xrange=[-0.01,0.1]
yrange=[0,0.0025]
scatterplot1(ax,daymean.loc[idx1,'lue'],
             daymean.loc[idx1,'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='o',color='r',range_label='ECI<='+str(eci1))
scatterplot1(ax,daymean.loc[-(idx1 | idx11),'lue'],
             daymean.loc[-(idx1 | idx11),'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='d',color='b',range_label=str(eci1)+'<'+'ECI<='+str(eci2))
scatterplot1(ax,daymean.loc[idx11,'lue'],
             daymean.loc[idx11,'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='v',color='k',range_label='ECI>'+str(eci2))

ax.tick_params(labelsize=ticklabelsize)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Arial') for label in labels]
ax.set_xlabel('LUE', **axis_font)
ax.set_ylabel('SIFyield', **axis_font)
ax.legend()

ax1=plt.subplot(322)
ax1.hist(daymean.loc[idx1,'MTVI2']
              ,weights=np.zeros_like(daymean.loc[idx1,'MTVI2'])+1./daymean.loc[idx1,'MTVI2'].size
              ,color='r',alpha=0.5)
ax2=plt.subplot(324)
ax2.hist(daymean.loc[-(idx1 | idx11),'MTVI2']
              ,weights=np.zeros_like(daymean.loc[-(idx1 | idx11),'MTVI2'])+1./daymean.loc[-(idx1 | idx11),'MTVI2'].size
              ,color='b',alpha=0.5)
ax3=plt.subplot(326)
ax3.hist(daymean.loc[idx11,'MTVI2']
              ,weights=np.zeros_like(daymean.loc[idx11,'MTVI2'])+1./daymean.loc[idx11,'MTVI2'].size
              ,color='k',alpha=0.5)

for ax in [ax1,ax2,ax3]:
    ax.set_xlim([0,1])
    ax.set_ylim([0,0.3])
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    ax.set_xlabel('MTVI2', **axis_font)
    ax.set_ylabel('frequency', **axis_font)
    if ax !=ax3:
        ax.set_xticks([])


# #---------------------------------------------
fig, axs = plt.subplots(3, 2, figsize=(10, 4.5))
fig.subplots_adjust(hspace=0,bottom=0.16,wspace=0.29)
###########################################
ax=plt.subplot(121)
scatterplot1(ax,daymean.loc[idx2,'lue'],
             daymean.loc[idx2,'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='o',color='r',range_label='MTVI2<='+str(mtvi21))
scatterplot1(ax,daymean.loc[-(idx2 | idx21),'lue'],
             daymean.loc[-(idx2 | idx21),'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='o',color='b',range_label=str(mtvi21)+'<'+'MTVI2<='+str(mtvi22))
scatterplot1(ax,daymean.loc[idx21,'lue'],
             daymean.loc[idx21,'sify'],
             xlim_range=xrange,
             ylim_range=yrange,
             marker='o',color='k',range_label='MTVI2>'+str(mtvi22))
ax1=plt.subplot(322)
ax1.hist(daymean.loc[idx2,'ECI']
              ,weights=np.zeros_like(daymean.loc[idx2,'ECI'])+1./daymean.loc[idx2,'ECI'].size
              ,color='r',alpha=0.5)
ax2=plt.subplot(324)
ax2.hist(daymean.loc[-(idx2 | idx21),'ECI']
              ,weights=np.zeros_like(daymean.loc[-(idx2 | idx21),'ECI'])+1./daymean.loc[-(idx2 | idx21),'ECI'].size
              ,color='b',alpha=0.5)
ax3=plt.subplot(326)
ax3.hist(daymean.loc[idx21,'ECI']
              ,weights=np.zeros_like(daymean.loc[idx21,'ECI'])+1./daymean.loc[idx21,'ECI'].size
              ,color='k',alpha=0.5)

ax.tick_params(labelsize=ticklabelsize)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Arial') for label in labels]
ax.set_xlabel('LUE', **axis_font)
ax.set_ylabel('SIFyield', **axis_font)
ax.legend()

for ax in [ax1,ax2,ax3]:
    ax.set_xlim([0,1])
    ax.set_ylim([0,0.3])
    ax.tick_params(labelsize=ticklabelsize)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Arial') for label in labels]
    ax.set_xlabel('ECI', **axis_font)
    ax.set_ylabel('frequency', **axis_font)
    if ax !=ax3:
        ax.set_xticks([])


#########ECI敏感性分析###############
temp=pd.DataFrame(columns=['idx','r','p'])
step=0.1
range_data=np.arange(0.,1.0,step)
fig,axs=plt.subplots(2,1,figsize=(10,10))
for flag in range(2):
    if flag:
        vis_label='MTVI2'
        box_label='ECI'
    else:
        vis_label='ECI'
        box_label='MTVI2'
    box_data=[]
    for i in range(len(range_data)):
        idx=(daymean[vis_label]>=range_data[i]) & (daymean[vis_label]<range_data[i]+step)
        x=daymean.loc[idx,'lue']
        y=daymean.loc[idx,'sify']
        r,p=get_pearsonr(x,y)
        if (flag==1) & (i==1):
            temp.loc[i, 'idx'] = i + 1
            temp.loc[i, 'r'] = np.nan
            temp.loc[i, 'p'] = np.nan
        else:
            temp.loc[i, 'idx'] = i+1
            temp.loc[i, 'r'] = r
            temp.loc[i, 'p'] = p
        box_data.append(daymean.loc[idx,box_label])
    print(temp)
    axs[flag].bar(temp['idx'], temp['r'],bottom=0, color='k', width=0.5,alpha=0.5,label='r of SIF$_{yield}$-LUE')

    for num in temp['idx']:
        axs[flag].text(temp.loc[num-1,'idx'],0.5,
                       funcs_lzh.funcstar(temp.loc[num-1,'p']),
                       color='r',horizontalalignment='center')
    axs[flag].set_ylabel('r of SIF$_{yield}$-LUE',**axis_font)
    axs[flag].set_ylim([-0.5,2])
    axs[flag].set_yticklabels(['-0.5', '0', '0.5', '1', '', ''])
    par=axs[flag].twinx()
    bp1 = par.boxplot(box_data, labels=temp['idx'], showmeans=True)
    par.set_ylabel(box_label,**axis_font)
    par.set_ylim([-2,1.5])
    par.set_yticklabels(['','','','','0','0.5','1','1.5'])
    for ax in [axs[flag],par]:
        ax.tick_params(labelsize=ticklabelsize)
        labels = ax.get_xticklabels() + ax.get_yticklabels()
        [label.set_fontname('Arial') for label in labels]

axs[0].set_xlabel('ECI Interval',**axis_font)
str_list=[str(x)+'-'+str(x+step) for x in np.arange(0,1,step)]
axs[0].set_xticklabels(str_list)
axs[1].set_xlabel('MTVI2 Interval',**axis_font)
axs[1].set_xticklabels(str_list)
axs[0].legend()


plt.show()