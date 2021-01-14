#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:25:41 2021

@author: Max
"""


import pandas as pd

metdata = pd.read_csv('observation_data.csv')
metdata = metdata.set_index('Timestamp')
metdata.index = pd.to_datetime(metdata.index, format='%d/%m/%Y %H:%M')

metdata = metdata.drop_duplicates()
metdata.to_csv('metdata.csv')

