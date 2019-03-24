#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_integration_of_sifarea.py
@time: 2019/3/6 22:00
'''

import numpy as np
import pandas as pd
from scipy.integrate import simps

data=pd.ExcelFile(r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\Flshape3.xlsx')
data=data.parse(0)

wl=data.iloc[:,0]
sif=data.iloc[:,1]
print(wl.shape,sif)

area=np.trapz(sif,wl)
print(area)
area=simps(sif,wl)
print(area)

sif760=0.042624

folds=area/sif760
print(folds)