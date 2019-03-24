#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: lizhaohui
@contact: lizhaoh2015@gmail.com
@file: get_irrad_rad_ref_plot.py
@time: 2019/3/7 22:53
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import ticker

axis_font = {'fontname': 'Arial', 'size': 13}
legend_font = {'fontname': 'Arial', 'size': 10}
ticklabelsize=12

fromatter = ticker.ScalarFormatter(useMathText=True)
fromatter.set_scientific(True)
fromatter.set_powerlimits((-1, 1))

filepath = r'D:\Shared_Folder\Lzh py\SifAnalysis\SIF_GPP_reviewer\data'

data = pd.ExcelFile(
    filepath + '\\' + r'irra_rad_apparent-reflectance_plot.xlsx')
daymean = data.parse('Sheet1')

wl = daymean.iloc[0]
irrad = daymean.iloc[1]*10
rad = daymean.iloc[2]*10
ref = daymean.iloc[3]

fig, axs = plt.subplots(2,1,figsize=(8, 8))
p1,=axs[0].plot(wl, irrad/np.pi, color='r', linewidth=1, label='Irradiance')
p2,=axs[0].plot(wl, rad, color='b', linewidth=1, label='Radiance')
axs[0].set_ylim(0,500)
axs[0].set_xlim(730,780)
axs[0].set_xlabel("Wavelength [nm]",**axis_font)
axs[0].set_ylabel("Irradiance or Radiance"+ '\n'+"$[mW/m^2/nm/sr]$",**axis_font)
axs[0].tick_params(labelsize=ticklabelsize)
axs1 = axs[0].twinx()
p3,=axs1.plot(wl, ref, color='k', linewidth=1, label='Reflectance')
axs1.set_ylim(0,0.55)
axs1.set_ylabel("Apparent reflectance",**axis_font)
axs1.tick_params(labelsize=ticklabelsize)
axs[0].axvspan(757,768,facecolor='gray',alpha=0.2)
axs[0].grid()
# axs1.set_yticks([0,0.2,0.4])
lines = [p1, p2, p3]
axs[0].legend(lines, [l.get_label() for l in lines],frameon=False,loc=2,prop={'size':11,'family':'Arial'})  # ,frameon=False 去掉图例边框
axs[0].yaxis.set_major_formatter(fromatter)
#
# # axs.title('20170911, 12h1min30sec')
# wl = daymean.iloc[4][452:1400]
# irrad = daymean.iloc[5][452:1400]*10
# rad = daymean.iloc[6][452:1400]*10
# ref = rad/irrad
# p1,=axs[1].plot(wl, irrad/np.pi, color='r', linewidth=1.5, label='Irradiance')
# p2,=axs[1].plot(wl, rad, color='b', linewidth=1.5, label='Radiance')
# # axs[1].set_ylim(0,45)
# axs[1].set_xlim(400,850)
# axs[1].set_xlabel("Wavelength [nm]",**axis_font)
# axs[1].set_ylabel("Irradiance or Radiance"+ '\n'+"$[mW/m^2/nm/sr]$",**axis_font)
# axs[1].tick_params(labelsize=ticklabelsize)
# axs1 = axs[1].twinx()
# p3,=axs1.plot(wl, ref, color='k', linewidth=1.5, label='Reflectance')
# # axs1.set_ylim(0,0.45)
# # axs1.set_yticks([0,0.2,0.4])
# axs1.set_ylabel("Apparent reflectance",**axis_font)
# axs1.tick_params(labelsize=ticklabelsize)
# lines = [p1, p2, p3]
# axs[1].legend(lines, [l.get_label() for l in lines],frameon=False,loc=2,prop={'size':14,'family':'Arial'})  # ,frameon=False 去掉图例边框
# axs[1].yaxis.set_major_formatter(fromatter)
#
plt.show()