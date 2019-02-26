#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-12 20:37:41
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

from sklearn.linear_model import LinearRegression
from scipy.stats.stats import pearsonr
import numpy as np
import pandas as pd
import math
import datetime
import matplotlib.pyplot as plt 

ticklabelsize = 14
axis_font = {'fontname': 'Arial', 'size': 14}
legend_font = {'fontname': 'Arial', 'size': 14}


def funcstar(p):
    '''
    置信系数级别
    '''
    if p < 0.001:
        return "**"
    elif p < 0.05:
        return "*"
    else:
        return ""


def get_lingre(x, y):
    '''
    计算一次线性回归参数
    '''
    lingre = LinearRegression()
    reg = lingre.fit(x, y)
    a, b = lingre.coef_, lingre.intercept_
    pred_y = reg.predict(x)
    return a, b, pred_y


def plot_xy(x, y, xlabel, ylabel, axs):
    '''
    画x,y的散点图,及线性拟合线，求r2
    '''
    temp = pd.concat([x, y], axis=1)
    # print(temp)
    temp = temp.dropna()
    x = temp[x.name]
    y = temp[y.name]
    a, b, pred_y = get_lingre(x.values.reshape(-1, 1), y)
    r, p = pearsonr(x, y)
    r2 = '%.2f' % np.square(r)
    text_line = 'y=' + '%.2f' % a + 'x' + '+' + '%.2f' % b
    text_rsqu = '$R^2$= ' + r2 + funcstar(p)
    axs.scatter(x, y, edgecolors='k',
                facecolors='', label=text_rsqu)
    axs.plot(x, pred_y, label=text_line, color='k')
    axs.set_xlabel(xlabel, **axis_font)
    axs.set_ylabel(ylabel, **axis_font)
    axs.legend(frameon=False)
    axs.tick_params(labelsize=ticklabelsize)


def bar_xy(x, y, xlabel, ylabel, legendlabel, alpha, axs):
    p = axs.bar(x, y, label=legendlabel, alpha=alpha)
    axs.set_ylabel(ylabel, **axis_font)
    axs.set_xlabel(xlabel, **axis_font)
    axs.tick_params(labelsize=ticklabelsize)
    axs.legend()
    return p


def scatter_xy(x, y, xlabel, ylabel, mk, ec, fc, legendlabel, axs):
    p = axs.scatter(x, y, marker=mk,
                    edgecolors=ec, facecolors=fc, label=legendlabel)
    axs.set_ylabel(ylabel, **axis_font)
    axs.set_xlabel(xlabel, **axis_font)
    axs.tick_params(labelsize=ticklabelsize)
    axs.legend()
    return p


def get_par(date_data, lon, lat):
    '''
    计算太阳辐射
    '''
    hs_format_time = date_data.hour + date_data.mins / 60 + date_data.sec / 3600
    meant = hs_format_time
    equationt = (120 - lon) / 15
    realt = meant + equationt
    t = (realt - 12) * 15
    N = date_data.doy
    b = 2 * np.pi * (N - 1) / 365
    delta = 0.006918 - 0.399912 * math.cos(b) + 0.070257 * math.sin(b) - 0.006758 * math.cos(
        2 * b) + 0.000907 * math.sin(2 * b) - 0.002697 * math.cos(3 * b) + 0.00148 * math.sin(3 * b)

    So = 1367  # unit W/m2
    phi = lat
    sza = 180 * math.asin(abs(math.sin(phi / 180 * np.pi)*math.sin(delta / 180 * np.pi)
                         + math.cos(phi / 180 * np.pi)*math.cos(delta / 180 * np.pi)*math.cos(t / 180 * np.pi)))
    sza = 90 - sza
    Ro = So * (1 + 0.033 * math.cos(360 * N / 365))*math.cos(sza/180*np.pi)
    return Ro

def get_rmse_rrmse(targets,predictions):
    """
    计算均方根误差,相对均方根误差
    """
    rmse=np.sqrt(((predictions-targets)**2).mean())
    rrmse=rmse/np.nanmean(targets)
    return rmse,rrmse


def heatmap(data, text,row_labels, col_labels, ax=None, rotation=0,cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Arguments:
        data       : A 2D numpy array of shape (N,M)
        row_labels : A list or array of length N with the labels
                     for the rows
        col_labels : A list or array of length M with the labels
                     for the columns
    Optional arguments:
        ax         : A matplotlib.axes.Axes instance to which the heatmap
                     is plotted. If not provided, use current axes or
                     create a new one.
        cbar_kw    : A dictionary with arguments to
                     :meth:`matplotlib.Figure.colorbar`.
        cbarlabel  : The label for the colorbar
    All other arguments are directly passed on to the imshow call.
    """
    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel(cbarlabel, rotation=90, va="top")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=rotation, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=1)
    ax.tick_params(which="minor", bottom=False, left=False)

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            text = ax.text(j, i, '%.2f' % data.iloc[
                        i, j], ha='center', va='center', color='w')

    return im, cbar

def get_matlab2py_doy(mattime):
    '''
    把matlab格式datenum时间转换成doy
    只能转换一个值，数组的话用map吧
    '''
    python_datetime = datetime.datetime.fromordinal(
        int(mattime) - 366) + datetime.timedelta(days=mattime % 1)
    doy = python_datetime.timetuple().tm_yday + mattime % 1
    return doy