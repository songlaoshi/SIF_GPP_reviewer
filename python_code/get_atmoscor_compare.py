#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_atmoscor_compare.py
@time: 2019/3/24 17:08
'''

# 比较大气校正前后的结果

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
# daymean
filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
daymean = pd.ExcelFile(
    filepath + '\\' + r'SIF_GPP_VI_ref_halfhourmean_sq2017corn.xlsx')
daymean = daymean.parse(0)

