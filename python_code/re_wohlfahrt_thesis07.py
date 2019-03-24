#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: re_wohlfahrt_thesis07.py
@time: 2019/3/20 10:51
'''

import os
import numpy as np
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


def MaxMinNormalization(x, max, min):
    x = (x - min) / (max - min)
    return x


def plot_01(axs, x, y, c, xlabel, ylabel):
    r, p = get_pearsonr(x, y)
    p = axs.scatter(x, y, c=c, cmap='jet', marker='.', label='r= %.2f' % r + funcs_lzh.funcstar(p))
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)
    axs.legend()
    return p


def plot_02(axs, x, y, color, llabel):
    r, p = get_pearsonr(x, y)
    axs.scatter(x, y, color=color,
                marker='.', label=llabel + 'r= %.2f' % r + funcs_lzh.funcstar(p))


def plot_07(axs, data, xlabel, ylabel, clabel):
    # idx1 = data['PAR'] <= parthred1
    # idx2 = (data['PAR'] > parthred1) & (data['PAR'] <= parthred2)
    # idx3 = data['PAR'] > parthred2
    # idx1 = data['CI'] <= cithred1
    # idx2 = (data['CI'] > cithred1) & (data['CI'] <= cithred2)
    # idx3 = data['CI'] > cithred2
    # idx1 = data['ECI'] <= ecithred1
    # idx2 = (data['ECI'] > ecithred1) & (data['ECI'] <= ecithred2)
    # idx3 = data['ECI'] > ecithred2
    p = axs.scatter(data['sify'], data['lue'],
                    c=data[clabel], cmap='Blues', marker='.')
    axs.set_xlim([0, 0.002])
    axs.set_xlabel(xlabel)
    axs.set_ylabel(ylabel)
    return p


# 科学计数法
fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

axis_font = {'fontname': 'Arial', 'size': 14}
font1 = {'family': 'Times New Roman',
         'weight': 'normal',
         'size': 18, }
legend_font = {'fontname': 'Arial', 'size': 14}
ticklabelsize = 14

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
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = daymean.parse(0)
# daymean=daymean[daymean['CI']>0.8]

daymean = pd.concat([daymean['doy'], daymean['hour'], daymean['MTVI2'], daymean['CIgreen']
                        , daymean['SFM'], daymean['GPP'], daymean['PAR'],
                     daymean['SIFyieldgndvi'], daymean['LUEgndvi'], daymean['CI'],
                     daymean['greenNDVI'], daymean['VPD'], daymean['Ta'], daymean['PRI']], axis=1)
daymean = daymean.dropna()
daymean['apar'] = daymean['greenNDVI'] * daymean['PAR']
daymean['scaled_APAR'] = MaxMinNormalization(daymean['apar'], np.max(daymean['apar']), np.min(daymean['apar']))
daymean['scaled_VPD'] = MaxMinNormalization(daymean['VPD'], np.max(daymean['VPD']), np.min(daymean['VPD']))
daymean['scaled_Ta'] = MaxMinNormalization(daymean['Ta'], np.max(daymean['Ta']), np.min(daymean['Ta']))
daymean['eci'] = daymean['scaled_APAR'] + daymean['scaled_VPD'] + daymean['scaled_Ta']
daymean['ECI'] = MaxMinNormalization(daymean['eci'], np.max(daymean['eci']), np.min(daymean['eci']))

daymean['sify'] = daymean['SIFyieldgndvi']
daymean['lue'] = daymean['LUEgndvi']
x = daymean['MTVI2'].values.reshape(-1, 1)
y = daymean['sify']
a, b, r2score, pred1 = get_a_b_r2score(x, y)
daymean['rsify'] = y - pred1
daymean['ssify']=pred1
y = daymean['PRI']
a, b, r2score, pred1 = get_a_b_r2score(x, y)
print(r2score, a, b)
daymean['rpri'] = y - pred1
daymean['spri']=pred1

# 分阶段
vege = daymean[daymean['doy'] <= a2]
repro = daymean[(daymean['doy'] > a2) & (daymean['doy'] <= a3)]
ripen = daymean[daymean['doy'] > a3]
# # SIFyield,LUE,PRI与ECI,LAI&Cab是否有关系
# fig,axs=plt.subplots(3,2,figsize=(10,7))
# fig.subplots_adjust(hspace=0,wspace=0)
# plot_01(axs[0,0],daymean['ECI'],daymean['sify'],daymean['doy'],'','$SIF_{yield}$')
# axs[0,0].set_ylim([-0.001,0.003])
# plot_01(axs[0,1],daymean['MTVI2'],daymean['sify'],daymean['doy'],'','')
# axs[0,1].set_ylim([-0.001,0.003])
# axs[0,1].set_yticks([])
# axs[0,1].axvspan(0.25,0.42,facecolor='gray',alpha=0.2)
# plot_01(axs[1,0],daymean['ECI'],daymean['lue'],daymean['doy'],'','LUE')
# plot_01(axs[1,1],daymean['MTVI2'],daymean['lue'],daymean['doy'],'','')
# axs[1,1].set_yticks([])
# axs[1,1].axvspan(0.25,0.42,facecolor='gray',alpha=0.2)
# plot_01(axs[2,0],daymean['ECI'],daymean['PRI'],daymean['doy'],'ECI','PRI')
# p=plot_01(axs[2,1],daymean['MTVI2'],daymean['PRI'],daymean['doy'],'MTVI2','')
# axs[2,1].set_yticks([])
# cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
# cbar1=fig.colorbar(p, cax=cbar_ax)
# cbar1.set_label('DOY', rotation=90)
# ## ECI,MTVI2是否影响SIFyield与LUE的相关性
# fig,axs=plt.subplots(2,2,figsize=(12,6))
# fig.subplots_adjust(hspace=0.4)
# eci1=0.4
# eci2=0.7
# mtvi21=0.4
# mtvi22=0.6
# idx1=(daymean['ECI']<= eci1)
# idx11=(daymean['ECI']> eci2)
# idx2=(daymean['MTVI2']<=mtvi21)
# idx21=(daymean['MTVI2']>mtvi22)
#
# plot_02(axs[0,0],daymean.loc[idx1,'lue'],daymean.loc[idx1,'sify'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,0],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'sify'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,0],daymean.loc[idx11,'lue'],daymean.loc[idx11,'sify'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['sify'])
# axs[0,0].text(0,0.0025,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,0].set_ylim([-0.001,0.003])
# axs[0,0].set_xlabel('LUE')
# axs[0,0].set_ylabel('$SIF_{yield}$')
# axs[0,0].set_title('devided by ECI')
# axs[0,0].legend()
# plot_02(axs[0,1],daymean.loc[idx1,'lue'],daymean.loc[idx1,'PRI'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,1],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'PRI'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,1],daymean.loc[idx11,'lue'],daymean.loc[idx11,'PRI'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['PRI'])
# axs[0,1].text(0,0,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,1].set_xlabel('LUE')
# axs[0,1].set_ylabel('PRI')
# axs[0,1].set_title('devided by ECI')
# axs[0,1].legend()
#
# plot_02(axs[1,0],daymean.loc[idx2,'lue'],daymean.loc[idx2,'sify'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,0],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'sify'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,0],daymean.loc[idx21,'lue'],daymean.loc[idx21,'sify'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,0].set_ylim([-0.001,0.003])
# axs[1,0].set_xlabel('LUE')
# axs[1,0].set_ylabel('$SIF_{yield}$')
# axs[1,0].set_title('devided by MTVI2')
# axs[1,0].legend()
# plot_02(axs[1,1],daymean.loc[idx2,'lue'],daymean.loc[idx2,'PRI'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,1],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'PRI'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,1],daymean.loc[idx21,'lue'],daymean.loc[idx21,'PRI'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,1].set_xlabel('LUE')
# axs[1,1].set_ylabel('PRI')
# axs[1,1].legend()
# axs[1,1].set_title('devided by MTVI2')
# ## ECI,MTVI2是否影响rSIFyield与LUE的相关性
# fig,axs=plt.subplots(2,2,figsize=(12,6))
# fig.subplots_adjust(hspace=0.4)
# eci1=0.4
# eci2=0.7
# mtvi21=0.4
# mtvi22=0.6
# idx1=(daymean['ECI']<= eci1)
# idx11=(daymean['ECI']> eci2)
# idx2=(daymean['MTVI2']<=mtvi21)
# idx21=(daymean['MTVI2']>mtvi22)
#
# plot_02(axs[0,0],daymean.loc[idx1,'lue'],daymean.loc[idx1,'rsify'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,0],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'rsify'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,0],daymean.loc[idx11,'lue'],daymean.loc[idx11,'rsify'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['rsify'])
# axs[0,0].text(0,0.0025,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,0].set_ylim([-0.002,0.003])
# axs[0,0].set_xlabel('LUE')
# axs[0,0].set_ylabel('$rSIF_{yield}$')
# axs[0,0].set_title('devided by ECI')
# axs[0,0].legend()
# plot_02(axs[0,1],daymean.loc[idx1,'lue'],daymean.loc[idx1,'rpri'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,1],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'rpri'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,1],daymean.loc[idx11,'lue'],daymean.loc[idx11,'rpri'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['rpri'])
# axs[0,1].text(0,0.02,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,1].set_xlabel('LUE')
# axs[0,1].set_ylabel('rPRI')
# axs[0,1].set_title('devided by ECI')
# axs[0,1].legend()
#
# plot_02(axs[1,0],daymean.loc[idx2,'lue'],daymean.loc[idx2,'rsify'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,0],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'rsify'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,0],daymean.loc[idx21,'lue'],daymean.loc[idx21,'rsify'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,0].set_ylim([-0.002,0.003])
# axs[1,0].set_xlabel('LUE')
# axs[1,0].set_ylabel('$rSIF_{yield}$')
# axs[1,0].set_title('devided by MTVI2')
# axs[1,0].legend()
# plot_02(axs[1,1],daymean.loc[idx2,'lue'],daymean.loc[idx2,'rpri'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,1],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'rpri'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,1],daymean.loc[idx21,'lue'],daymean.loc[idx21,'rpri'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,1].set_xlabel('LUE')
# axs[1,1].set_ylabel('rPRI')
# axs[1,1].legend()
# axs[1,1].set_title('devided by MTVI2')

# ## ECI,MTVI2是否影响rSIFyield与LUE的相关性
# fig,axs=plt.subplots(2,2,figsize=(12,6))
# fig.subplots_adjust(hspace=0.4)
# eci1=0.4
# eci2=0.7
# mtvi21=0.4
# mtvi22=0.6
# idx1=(daymean['ECI']<= eci1)
# idx11=(daymean['ECI']> eci2)
# idx2=(daymean['MTVI2']<=mtvi21)
# idx21=(daymean['MTVI2']>mtvi22)
#
# plot_02(axs[0,0],daymean.loc[idx1,'lue'],daymean.loc[idx1,'ssify'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,0],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'ssify'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,0],daymean.loc[idx11,'lue'],daymean.loc[idx11,'ssify'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['ssify'])
# axs[0,0].text(0,0.0015,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,0].set_ylim([-0.001,0.002])
# axs[0,0].set_xlabel('LUE')
# axs[0,0].set_ylabel('$sSIF_{yield}$')
# axs[0,0].set_title('devided by ECI')
# axs[0,0].legend()
# plot_02(axs[0,1],daymean.loc[idx1,'lue'],daymean.loc[idx1,'spri'],'r','ECI<='+str(eci1)+',')
# plot_02(axs[0,1],daymean.loc[-(idx1 | idx11),'lue'],daymean.loc[-(idx1 | idx11),'spri'],'b',str(eci1)+'<ECI<='+str(eci2)+',')
# plot_02(axs[0,1],daymean.loc[idx11,'lue'],daymean.loc[idx11,'spri'],'k','ECI>'+str(eci2)+',')
# r,p=get_pearsonr(daymean['lue'],daymean['spri'])
# axs[0,1].text(0,0.01,'all,r= %.2f'%r+funcs_lzh.funcstar(p))
# axs[0,1].set_xlabel('LUE')
# axs[0,1].set_ylabel('sPRI')
# axs[0,1].set_title('devided by ECI')
# # axs[0,1].legend()
#
# plot_02(axs[1,0],daymean.loc[idx2,'lue'],daymean.loc[idx2,'ssify'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,0],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'ssify'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,0],daymean.loc[idx21,'lue'],daymean.loc[idx21,'ssify'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,0].set_ylim([-0.001,0.002])
# axs[1,0].set_xlabel('LUE')
# axs[1,0].set_ylabel('$sSIF_{yield}$')
# axs[1,0].set_title('devided by MTVI2')
# axs[1,0].legend()
# plot_02(axs[1,1],daymean.loc[idx2,'lue'],daymean.loc[idx2,'spri'],'r','MTVI2<='+str(mtvi21)+',')
# plot_02(axs[1,1],daymean.loc[-(idx2 | idx21),'lue'],daymean.loc[-(idx2 | idx21),'spri'],'b',str(mtvi21)+'<MTVI2<='+str(mtvi22)+',')
# plot_02(axs[1,1],daymean.loc[idx21,'lue'],daymean.loc[idx21,'spri'],'k','MTVI2>'+str(mtvi22)+',')
# axs[1,1].set_xlabel('LUE')
# axs[1,1].set_ylabel('sPRI')
# # axs[1,1].legend()
# axs[1,1].set_title('devided by MTVI2')

#
# # ## LUE/SIFyield 的diurnal内的斜率
# # fig, axs = plt.subplots(2, 1)
# # fig.subplots_adjust(hspace=0)
# fig=plt.figure(figsize=(14,8))
# ax=fig.add_subplot(122,projection='3d')
# # axs[1]=fig.gca(projection='3d')
# stats = pd.DataFrame(columns=['hour', 'a', 'b', 'r2score', 'pred', 'r', 'p'])
# hour = np.arange(9.0, 16.0, 0.5)
# stats['hour'] = hour
# for i in range(len(hour)):
#     t = hour[i]
#     idx = (daymean['hour'] >= t - 0.1) & (daymean['hour'] < t + 0.1)
#     x = daymean.loc[idx, 'sify'].values.reshape(-1, 1)
#     y = daymean.loc[idx, 'lue']
#     r, p = get_pearsonr(daymean.loc[idx, 'sify'], daymean.loc[idx, 'lue'])
#     stats.loc[i, 'r'] = r
#     stats.loc[i, 'p'] = p
#     print(t, x.shape[0])
#     if x.shape[0] != 0:
#         a, b, r2score, pred = get_a_b_r2score(x, y)
#         stats.loc[i, 'a'] = a
#         stats.loc[i, 'b'] = b
#         stats.loc[i, 'r2score'] = r2score
#         # stats.loc[i, 'pred'] = pred
#         # axs[0].scatter(x, y, label=str(t))
#         ax.scatter(x, y, zs=t, marker='.', label=str(t))
#         ax.plot(x, pred, zs=t)
#     else:
#         stats.loc[i, 'a'] = np.nan
#         stats.loc[i, 'b'] = np.nan
#         stats.loc[i, 'r2score'] = np.nan
#         stats.loc[i, 'pred'] = np.nan
#
# ax.view_init(elev=8,azim=-35)
# # ax.legend(loc=6,ncol=1)
# ax.set_xlim([-0.001,0.002])
# ax.set_xticks([-0.001,0,0.001,0.002])
# ax.set_yticks([0,0.05,0.1])
# # ax.set_ylim([0,0.15])
# ax.set_zlim([8.5,16.0])
# ax.xaxis.set_major_formatter(fromatter)
# ax.yaxis.set_major_formatter(fromatter)
# ax.set_xlabel('$SIF_{yield}$')
# ax.set_ylabel('LUE')
# ax.set_zlabel('Hour')
#
# #
# # print(stats['hour'])
# ax1=fig.add_subplot(221)
# ax1.scatter(stats['hour'], stats['a'],c='b',label='r2<=0.25')
# stats_idx = (stats['r2score'] > 0.25) & (stats['p'] < 0.05)
# ax1.scatter(stats.loc[stats_idx, 'hour'], stats.loc[stats_idx, 'a'], color='r',label='r2>0.25 and p<0.05')
# ax1.set_xlabel('Hour')
# ax1.set_ylabel('Slope of LUE vs $SIF_{yield}$')
# ax1.set_xlim([8.5, 16])
# ax1.set_xticks([9, 10, 11, 12, 13, 14, 15])
# ax1.grid()
# ax1.set_ylim(0,50)
# ax1.legend(loc=4)
# ax2=fig.add_subplot(223)
# ax2.scatter(stats['hour'], stats['b'], color='b', marker='^')
# ax2.scatter(stats.loc[stats_idx, 'hour'], stats.loc[stats_idx, 'b'], color='r', marker='^')
# ax2.set_ylabel('Intercept of LUE vs $SIF_{yield}$')
# ax2.set_ylim(0,0.1)
# ax2.grid()
# ax2.set_xlabel('Hour')
#
# # ## LUE/rSIFyield 的diurnal内的斜率
# stats=pd.DataFrame(columns=['hour','a','b','r2score','pred','r','p'])
# hour=np.arange(9.0,16.0,0.5)
# stats['hour']=hour
# fig,axs=plt.subplots(2,1,figsize=(6,8))
# for i in range(len(hour)):
#     t = hour[i]
#     idx = (daymean['hour'] >= t - 0.1) & (daymean['hour'] < t + 0.1)
#     x = daymean.loc[idx, 'rsify'].values.reshape(-1, 1)
#     y = daymean.loc[idx, 'lue']
#     r, p = get_pearsonr(daymean.loc[idx, 'rsify'], daymean.loc[idx, 'lue'])
#     stats.loc[i, 'r'] = r
#     stats.loc[i, 'p'] = p
#     print(t, x.shape[0])
#     if x.shape[0] != 0:
#         a, b, r2score, pred = get_a_b_r2score(x, y)
#         stats.loc[i, 'a'] = a
#         stats.loc[i, 'b'] = b
#         stats.loc[i, 'r2score'] = r2score
#         # stats.loc[i, 'pred'] = pred
#         # axs[0].scatter(x, y, label=str(t))
#     else:
#         stats.loc[i, 'a'] = np.nan
#         stats.loc[i, 'b'] = np.nan
#         stats.loc[i, 'r2score'] = np.nan
#         stats.loc[i, 'pred'] = np.nan
#
# # axs[0].set_xlim([-0.002,0.003])
# # axs[0].legend()
# #
# axs[0].scatter(stats['hour'], stats['a'], color='b', label='r2<=0.25')
# stats_idx = (stats['r2score'] > 0.25) & (stats['p'] < 0.05)
# axs[0].scatter(stats.loc[stats_idx, 'hour'], stats.loc[stats_idx, 'a'], color='r', label='r2>0.25 and p<0.05')
# axs[0].grid()
# axs[0].set_ylabel('Slope of LUE vs $rSIF_{yield}$')
# axs[0].set_xlabel('Hour')
#
# axs[1].scatter(stats['hour'], stats['b'], color='b', marker='^')
# axs[1].scatter(stats.loc[stats_idx, 'hour'], stats.loc[stats_idx, 'b'], color='r', marker='^')
# axs[1].set_ylabel('Intercept of LUE vs $rSIF_{yield}$')
# axs[1].set_xlabel('Hour')
# # print(stats)
# # axs[1].set_xlim([8.5, 16])
# # axs[1].set_xticks([9, 10, 11, 12, 13, 14, 15])
# axs[1].grid()
# axs[0].legend()


# ## SIFyield和LUE的diurnal平均，日变化和相关性
# # ## LUE/rSIFyield 的diurnal内的斜率
# daymean=daymean.loc[daymean['CI']>=0.55,:]
# stats=pd.DataFrame(columns=['hour','sif_dm','lue_dm','pri_dm','rsif_dm','rpri_dm','par_dm'])
# hour=np.arange(9.0,16.0,0.5)
# stats['hour']=hour
# for i in range(len(hour)):
#     t = hour[i]
#     idx = (daymean['hour'] >= t - 0.1) & (daymean['hour'] < t + 0.1)
#     sify = daymean.loc[idx, 'sify']
#     lue = daymean.loc[idx, 'lue']
#     pri = daymean.loc[idx, 'PRI']
#     rsify=daymean.loc[idx, 'rsify']
#     rpri=daymean.loc[idx, 'rpri']
#     par=daymean.loc[idx, 'PAR']
#     stats.loc[i,'sif_dm']=np.nanmean(sify,axis=0)
#     stats.loc[i, 'lue_dm'] = np.nanmean(lue,axis=0)
#     stats.loc[i, 'pri_dm'] = np.nanmean(pri,axis=0)
#     stats.loc[i, 'rsif_dm'] = np.nanmean(rsify,axis=0)
#     stats.loc[i, 'rpri_dm'] = np.nanmean(rpri,axis=0)
#     stats.loc[i, 'par_dm'] = np.nanmean(par,axis=0)
#
#
# fig,axs=plt.subplots(2,3,figsize=(8,6))
# plt.subplots_adjust(wspace=0.5)
# axs[0,0].plot(hour,stats['lue_dm'],marker='.',c='b')
# axs[0,0].twinx().plot(hour,stats['par_dm'],marker='.',c='r')
# axs[0,1].plot(hour,stats['rsif_dm'],marker='.',c='b')
# axs[0,1].twinx().plot(hour,stats['par_dm'],marker='.',c='r')
# axs[0,2].plot(hour,stats['rpri_dm'],marker='.',c='b')
# axs[0,2].twinx().plot(hour,stats['par_dm'],marker='.',c='r')
# axs[1,0].scatter(stats['lue_dm'],stats['rsif_dm'],c=hour,cmap='bwr')
# axs[1,0].set_ylim([-0.0002,0.0002])
# axs[1,0].set_xlim([0.03,0.06])
# axs[1,1].scatter(stats['lue_dm'],stats['rpri_dm'],c=hour,cmap='bwr')
# axs[1,1].set_ylim([-0.01,0.01])
# axs[1,1].set_xlim([0.03,0.06])
# p=axs[1,2].scatter(stats['rpri_dm'],stats['rsif_dm'],c=hour,cmap='bwr')
# axs[1,2].set_ylim([-0.0002,0.0002])
# axs[1,2].set_xlim([-0.01,0.01])
# cbar_ax = fig.add_axes([0.92, 0.1, 0.01, 0.4])
# cbar1=fig.colorbar(p, cax=cbar_ax)

## SIFyield与LUE每天的r
stats=pd.DataFrame(columns=['doy','pear_r','p','pear_rr','pr','ci_mean','eci_mean'])
doy1=int(daymean.loc[0,'doy'])
doy2=int(daymean.loc[daymean.index[-1],'doy'])
print(doy1,doy2)
doy=np.arange(doy1,doy2+1)
for i in range(len(doy)):
    day=doy[i]
    idx=(daymean['doy']>=day) & (daymean['doy']<day+1.0)
    data=daymean.loc[idx,:]
    r,p=get_pearsonr(data['SIFyieldgndvi'],data['LUEgndvi'])
    stats.loc[i, 'doy'] = day
    stats.loc[i,'pear_r']=r
    stats.loc[i,'p']=p
    r,p=get_pearsonr(data['rsify'],data['LUEgndvi'])
    stats.loc[i,'pear_rr']=r
    stats.loc[i,'pr']=p
    stats.loc[i,'ci_mean']=np.nanmean(data['CI'])
    stats.loc[i, 'eci_mean'] = np.nanmean(data['ECI'])
# print(stats)
fig,ax=plt.subplots(4,1,figsize=(10,7),sharex='col')
idxp=stats['p']<0.05
ax[0].bar(stats.loc[idxp,'doy'],stats.loc[idxp,'pear_r'],color='r',label='p<0.05')
ax[0].bar(stats.loc[-idxp,'doy'],stats.loc[-idxp,'pear_r'],color='k',label='p>=0.05')
ax[0].vlines(a2,-1,1,color='k', linestyle='--')
ax[0].vlines(a3,-1,1,color='k', linestyle='--')
ax[0].set_ylim(-1,1)
ax[0].tick_params(labelsize=ticklabelsize)
ax[0].set_ylabel('r of SIF$_{yield}$ vs LUE',**axis_font)
ax[0].legend(loc=3)
ax[0].grid()

idxp=stats['pr']<0.05
ax[1].bar(stats.loc[idxp,'doy'],stats.loc[idxp,'pear_rr'],color='r',label='p<0.05')
ax[1].bar(stats.loc[-idxp,'doy'],stats.loc[-idxp,'pear_rr'],color='k',label='p>=0.05')
ax[1].vlines(a2,-1,1,color='k', linestyle='--')
ax[1].vlines(a3,-1,1,color='k', linestyle='--')
ax[1].set_ylim(-1,1)
ax[1].tick_params(labelsize=ticklabelsize)
ax[1].set_ylabel('r of rSIF$_{yield}$ vs LUE',**axis_font)
ax[1].grid()

idxci=stats['ci_mean']>0.55
ax[2].bar(stats.loc[idxci,'doy'],stats.loc[idxci,'ci_mean'],color='r',label='CI>0.55')
ax[2].bar(stats.loc[-idxci,'doy'],stats.loc[-idxci,'ci_mean'],color='k',label='CI<=0.55')
ax[2].set_xlabel('DOY',**axis_font)
ax[2].vlines(a2,-1,1,color='k', linestyle='--')
ax[2].vlines(a3,-1,1,color='k', linestyle='--')
ax[2].set_ylim(0,1)
ax[2].tick_params(labelsize=ticklabelsize)
ax[2].set_ylabel('clearness index',**axis_font)
ax[2].grid()
ax[2].legend()

idxci=stats['eci_mean']>0.8
ax[3].bar(stats.loc[idxci,'doy'],stats.loc[idxci,'eci_mean'],color='r',label='ECI>0.8')
ax[3].bar(stats.loc[-idxci,'doy'],stats.loc[-idxci,'eci_mean'],color='k',label='ECI<=0.8')
ax[3].set_xlabel('DOY',**axis_font)
ax[3].vlines(a2,-1,1,color='k', linestyle='--')
ax[3].vlines(a3,-1,1,color='k', linestyle='--')
ax[3].set_ylim(0,1)
ax[3].tick_params(labelsize=ticklabelsize)
ax[3].set_ylabel('ECI',**axis_font)
ax[3].grid()
ax[3].legend()

print(stats['pear_r']) # 有-1,和1 ，仔细看一下
plt.show()
