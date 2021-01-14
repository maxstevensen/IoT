#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 15:18:42 2021

@author: Max
"""

import pandas as pd
df = pd.read_csv('datacombined.csv')

a = df[df['speed (m/s)'] > 0.1]

x = a['W']
y = x[x<9].count()
z = x.count()
Watson_out_weather = (y/z)*100
print('There is an %.2f%% chance it is not raining, get on out there!' % Watson_out_weather)
#%%