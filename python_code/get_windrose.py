#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_windrose.py
@time: 2019/4/22 9:52
'''

import pandas as pd
import numpy as np
import windrose
import matplotlib.pyplot as plt

filepath=r'D:\Data\shangqiu data\flux data'
fluxdata=pd.ExcelFile(filepath+'\\SQ_EC.xlsx')
fluxdata=fluxdata.parse(0)
spec_path=r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data\spec_wind'
spec_wind=pd.ExcelFile(spec_path+'\\spec_wind.xlsx')
spec_wind=spec_wind.parse(0)

wind_speed=fluxdata['wind_speed']
max_wind_speed=fluxdata['max_wind_speed']
wind_dir=fluxdata['wind_dir']
ax=windrose.WindroseAxes.from_ax()
ax.contourf(wind_dir,wind_speed)
ax.set_legend()

wind_speed=spec_wind['wind_speed_10min_mean']
# max_wind_speed=spec_wind['max_wind_speed']
wind_dir=spec_wind['wind_dir']
ax=windrose.WindroseAxes.from_ax()
ax.contourf(wind_dir,wind_speed)
ax.set_legend()

plt.show()

