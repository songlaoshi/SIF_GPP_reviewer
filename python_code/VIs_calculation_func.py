#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-08 10:52:59
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

import os
import numpy as np
import datetime


class VI_container(object):
	"""docstring for VI_container:
	植被指数类，保存植被指数计算结果
	NDVI=(Rnir-Rred)/(Rnir+Rred),
	EVI=...
	MTCI=...
	MTVI2=1.5[1.2(R800-R550)-2.5(R670-R550)]/sqrt((2R800+1)^2-(6R800-5sqrt(R670))-0.5)
	CVI=(nir/green)*(red/green) where nir=760-900,red=630-690,green=520-600

	"""

	def __init__(self):
		super(VI_container, self).__init__()
	NDVI = np.array([])
	EVI = np.array([])
	MTCI = np.array([])
	MTVI2 = np.array([])
	PRI = np.array([])
	greenNDVI = np.array([])
	rededgeNDVI = np.array([])
	CIgreen = np.array([])
	CVI = np.array([])
	SR = np.array([])
	Rblue=np.array([])
	Rgreen=np.array([])
	Rred=np.array([])
	Rnir=np.array([])
	Rrededge=np.array([])



def get_vegetation_indices(wl, ref):
	'''
	计算植被指数
	'''
	iblue = (wl > 430) & (wl < 450)
	igreen = (wl > 540) & (wl < 570)
	ired = (wl > 650) & (wl < 680)
	iNIR = (wl > 770) & (wl < 790)
	irededge = (wl > 700) & (wl < 710)
	iband10 = (wl > 753.75 - 7.5 / 2) & (wl < 753.75 + 7.5 / 2)
	iband9 = (wl > 708.75 - 10 / 2) & (wl < 708.75 + 10 / 2)
	iband8 = (wl > 681.25 - 7.5 / 2) & (wl < 681.25 + 7.5 / 2)
	i_lamda_800 = (wl > 800 - 1.5) & (wl < 800 + 1.5)
	i_lamda_550 = (wl > 550 - 1.5) & (wl < 550 + 1.5)
	i_lamda_670 = (wl > 670 - 1.5) & (wl < 670 + 1.5)
	i_lamda_531 = (wl > 531 - 0.5) & (wl < 531 + 0.5)
	i_lamda_570 = (wl > 570 - 0.5) & (wl < 570 + 0.5)
	# get average ref
	Rblue = np.nanmean(ref.loc[:, iblue], axis=1)
	Rgreen = np.nanmean(ref.loc[:, igreen], axis=1)
	Rred = np.nanmean(ref.loc[:, ired], axis=1)
	Rnir = np.nanmean(ref.loc[:, iNIR], axis=1)
	Rrededge = np.nanmean(ref.loc[:, irededge], axis=1)
	R10 = np.nanmean(ref.loc[:, iband10], axis=1)
	R9 = np.nanmean(ref.loc[:, iband9], axis=1)
	R8 = np.nanmean(ref.loc[:, iband8], axis=1)
	R_lamda_800 = np.nanmean(ref.loc[:, i_lamda_800], axis=1)
	R_lamda_550 = np.nanmean(ref.loc[:, i_lamda_550], axis=1)
	R_lamda_670 = np.nanmean(ref.loc[:, i_lamda_670], axis=1)
	R_lamda_531 = np.nanmean(ref.loc[:, i_lamda_531], axis=1)
	R_lamda_570 = np.nanmean(ref.loc[:, i_lamda_570], axis=1)
    # get VIS
	setup = VI_container()
	setup.NDVI = (Rnir - Rred) / (Rnir + Rred)
	setup.EVI = (2.5 * (Rnir - Rred) / (Rnir + 6 * Rred - 7.5 * Rblue + 1))
	setup.MTCI = (R10 - R9) / (R9 - R8)
	temp = (2 * R_lamda_800 + 1)**2 - \
	        (6 * R_lamda_800 - 5 * np.sqrt(R_lamda_670)) - 0.5
	setup.MTVI2 = 1.5 * (1.2 * (R_lamda_800 - R_lamda_550) -
	                     2.5 * (R_lamda_670 - R_lamda_550)) / np.sqrt(temp)
	setup.PRI = (R_lamda_531 - R_lamda_570) / (R_lamda_531 + R_lamda_570)
	setup.greenNDVI = (Rnir - Rgreen) / (Rnir + Rgreen)
	setup.rededgeNDVI = (Rnir - Rrededge) / (Rnir + Rrededge)
	setup.CIgreen = Rnir / Rgreen - 1
	setup.CVI = Rnir * Rred / Rgreen / Rgreen
	setup.SR = Rnir / Rred
	setup.Rblue=Rblue
	setup.Rgreen=Rgreen
	setup.Rred=Rred
	setup.Rnir=Rnir
	setup.Rrededge=Rrededge

	return setup


def get_vi_halfhourlymean(starthour, endhour, dhour, vidata):
	'''
	计算植被指数的半小时平均值
	starthour:选取的开始时间
	endhour:选取的结束时间
	dhour:一天内的小时数，如dhour=8.5指8点30分
	vidata:植被指数数据，二维数组，行为时间，列为各个植被指数值
	'''
	halfhourlymean = []
	hourrange = np.arange(starthour, endhour, 0.5)
	for hour_num in hourrange:
		idx = (dhour >= hour_num) & (dhour < hour_num + 0.5)
		if hour_num == starthour:
			halfhourlymean = np.nanmean(vidata.loc[idx, :], axis=0)
		else:
		    halfhourlymean = np.vstack(
		        [halfhourlymean, np.nanmean(vidata.loc[idx, :], axis=0)])
	return halfhourlymean


def get_vi_daymean(starthour,endhour,dhour,vidata):
	'''
	计算植被指数的日平均值
	'''
	idx=(dhour>=starthour) & (dhour<=endhour)
	daymean=np.nanmean(vidata.loc[idx,:],axis=0)
	return daymean
	

def get_doy(datestr):
	'''
	计算day of year
	datestr: e.g. 20170707
	'''
	year=int(datestr[0:4])
	month=int(datestr[4:6])
	day=int(datestr[6:8])
	doy=datetime.date(year,month,day).timetuple().tm_yday
	return doy









