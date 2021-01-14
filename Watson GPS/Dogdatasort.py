#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 15:15:15 2021

@author: Max
"""

import pandas as pd

data = pd.read_csv('track_points.csv')
data = pd.DataFrame(data)
data = data[['X','Y','ele','time','cmt']]
data = data.rename(columns={'cmt':'speed (m/s)'})
data['speed (m/s)'] = data['speed (m/s)'].str.replace('speed: ','')
data['time'] = data['time'].str[:-3]
print(data.dtypes)
data = data.set_index('time')
print(data.head(5))

#data.to_csv('dog_tracking.csv')
#%%

data.index = pd.to_datetime(data.index)
data['speed (m/s)'] = data['speed (m/s)'].astype(float)
print(data.dtypes)
#data.to_csv('data_check.csv')
#%%
data_hourly = data.resample('h').mean()
print(data_hourly.head(5))
data_hourly.to_csv('dog_tracking_hourly.csv')
