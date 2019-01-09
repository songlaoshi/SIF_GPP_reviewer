#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-08 10:49:38
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

import os
import numpy as np
import pandas as pd
import datetime
import VIs_calculation_func

# ## calculate VIs
# filepath = r'D:\Data\shangqiu data\shang\Results_HRdata_recal\REF\HR_REF'
# files = os.listdir(filepath)
# savepath = r'D:\Data\shangqiu data\shang\Results_HRdata_recal\VI_HR_addMTVI2'

# for file in files:
#     data = pd.ExcelFile(filepath + '/' + file)
#     data = data.parse('Sheet1')
#     wl = data.columns[5:].values
#     refdata = data.iloc[:, 5:]
#     timedata = data.iloc[:, 1:5]
#     matlab_datenum = data.iloc[:, 4].values
#     python_datetime = map(lambda x: datetime.datetime.fromordinal(
# 	    int(x) - 366) + datetime.timedelta(days=x % 1), matlab_datenum)
#     # 因为matlab是从公元0年开始计算的，公元0年是一个闰年，因此需要减去366天
#     timedata.iloc[:,3]=list(python_datetime)
#     setup=VIs_calculation_func.get_vegetation_indices(wl,refdata)
#     # save VIs data
#     datestr=file[4:12]
#     columns=['hour','min','sec','datetime','NDVI','EVI','MTCI','MTVI2'
#     ,'PRI','greenNDVI','rededgeNDVI','CIgreen','CVI','SR']
#     savedata=pd.DataFrame((np.vstack([timedata.values.T,setup.NDVI,setup.EVI,
#     	setup.MTCI,setup.MTVI2,setup.PRI,setup.greenNDVI,setup.rededgeNDVI,
#         setup.CIgreen,setup.CVI,setup.SR]).T),columns=columns)
#     # print(savedata.shape)
#     savedata.to_csv(savepath+'/VIs_'+datestr+'.csv',index=False,header=True)
#     print(datestr+' is ok...')

# calculate halfhourly mean and daymean VIs
filepath = r'D:\Data\shangqiu data\shang\Results_HRdata_recal\VI_HR_addMTVI2'
savepath=r'D:\Data\shangqiu data\shang\Results_HRdata_recal'
files = os.listdir(filepath)

for file in files:
    data = pd.read_csv(filepath + '/' + file)
    datestr=file[4:12]
    doy=VIs_calculation_func.get_doy(datestr)
    hour = data['hour']
    mins = data['min']
    dhour=hour+mins/60
    # print(dhour)
    vis = data.iloc[:, 4:]
    # print(vis.shape)
    starthour=8
    endhour=18
    hourrange=np.arange(starthour, endhour,0.5)
    halfhourlymean=VIs_calculation_func.get_vi_halfhourlymean(starthour,endhour,dhour,vis)
    daymean=VIs_calculation_func.get_vi_daymean(starthour,endhour,dhour,vis)
    # print(halfhourlymean.shape)
    # print(halfhourlymean[0:5,:])
    if file==files[0]:
    	Half=np.hstack([(np.ones(hourrange.shape)*doy).reshape(-1,1),hourrange.reshape(-1,1),halfhourlymean])
    	Daymean=np.hstack([doy,daymean])
    else:
    	Half=np.vstack([Half,np.hstack([(np.ones(hourrange.shape)*doy).reshape(-1,1),hourrange.reshape(-1,1),halfhourlymean])])
    	Daymean=np.vstack([Daymean,np.hstack([doy,daymean])])

    print(file+' is ok...')

## save halfhourly and daymean VIS
columns=['doy','hour','NDVI','EVI','MTCI','MTVI2'
    ,'PRI','greenNDVI','rededgeNDVI','CIgreen','CVI','SR']
temp=pd.DataFrame(Half,columns=columns)
temp.to_csv(savepath+'/'+'VI_HR_addMTVI2_halfhourlymean.csv',index=False,header=True)
columns=['doy','NDVI','EVI','MTCI','MTVI2'
    ,'PRI','greenNDVI','rededgeNDVI','CIgreen','CVI','SR']
temp=pd.DataFrame(Daymean,columns=columns)
temp.to_csv(savepath+'/'+'VI_HR_addMTVI2_dailymean.csv',index=False,header=True)



