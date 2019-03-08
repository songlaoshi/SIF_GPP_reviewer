#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-25 11:01:56
# @Author  : Lzh (lizhaoh2015@gmail.com)
# @Link    : http://songlaoshi.github.io
# @Version : $Id$

import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

# daymean
data = pd.ExcelFile(
    filepath + '\\' + r'GPP_VPD_Ta_Tleaf_PAR_APAR_norain_SIF_VI_NIRv_CI_SIFyield_LUE_halfhour.xlsx')
daymean = data.parse('Sheet1')
daymean = daymean.dropna()

# 