#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_SZA_cleandata.py     #计算SZA，并整合到数据中
@time: 2019/4/9 9:41
'''

import pandas as pd
import numpy as np
import funcs_lzh

filepath=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'
filepath1=r'D:\Data\shangqiu data\shang\Results_HRdata_recal'
data=pd.ExcelFile(filepath1+'\\'+'SIF_GPP_VI_ref_halfhourmean_sq2017corn_8-18.xlsx')
data=data.parse(0)

## 去掉一些植被指数的异常值
idx=[1480,1540,1560,1656,1657,1658,1659,1660,1720,1736,1737,1738,1739,1740]
for i in idx:
    data.iloc[i-1,16:]=np.nan

doy=np.fix(data['doy'])
time=data['hour']
lon=115.5916
lat=34.5199
sza=[]
for i in range(len(doy)):
    sza.append(funcs_lzh.get_solar_zenith_angle(lon, lat, doy[i], time[i]))

SZA=pd.DataFrame(sza,columns=['SZA'])
new=pd.concat([data,SZA],axis=1)
new.to_csv(filepath+'\\SIF_GPP_VI_ref_halfhourmean_sq2017corn_8-18_addSZA.csv',index=False)
