#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 15:18:13 2021

@author: Max
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import  mean_squared_error

df = pd.read_csv('datacombined.csv')
df = df.set_index('Time')
df.index = pd.to_datetime(df.index)
dog = df[['X','Y','ele','speed (m/s)']]
dog = dog.interpolate(method='time')
weather = df[['D','Dp','G','H','P','Pt','S','T','V','W']]
weather = weather.interpolate(method='time')
 #%%   
from statsmodels.tsa.arima_model import ARIMA
def forcast_ts(data, tt_ratio):
    X = data.values
    size = int(len(X) * tt_ratio)
    train, test = X[0:size], X[size:len(X)]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(5,1,0))
        model_fit = model.fit(disp=0)
        output = model_fit.forecast()
        yhat = output[0]
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('progress:%',round(100*(t/len(test))),'\t predicted=%f, expected=%f' % (yhat, obs), end="\r")
    error = mean_squared_error(test, predictions)
    print('\n Test MSE: %.3f' % error)

    plt.rcParams["figure.figsize"] = (25,10)
    preds = np.append(train, predictions)
    plt.plot(list(preds), color='orange', linewidth=3, label="Predicted Data")
    plt.plot(list(data), color='blue', linewidth=2, label="Original Data")
    plt.axvline(x=int(len(data)*tt_ratio)-1, linewidth=5, color='red')
    plt.legend()
    plt.show()
    #%%
data = weather['W']
tt_ratio = 0.7 # Train to Test ratio
forcast_ts(data, tt_ratio)
#%%
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
keras.__version__

w = weather['W']
z = 196*0.8 # Train to Test ratio
x_train = dog[:140]
y_train = w[:140]

x_test = dog[140:]
y_test = w[140:]

x_train = np.reshape(x_train.values, (x_train.shape[0], x_train.shape[1], 1))
x_test = np.reshape(x_test.values, (x_test.shape[0], x_test.shape[1], 1))

x_train.shape, y_train.shape, x_test.shape, y_test.shape
#%%
model = Sequential()
model.add(LSTM(units=32, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(units=32))
model.add(Dense(units = 1))
model.compile(optimizer = 'adam', loss = 'mean_squared_error')
model.summary()
#%%
model.fit(x_train, y_train, epochs = 16, batch_size = 32)
#%%
predictions = model.predict(x_test)
plt.figure(figsize=(25,10))
plt.plot(y_test.values, color='pink', label='Original Usage')
plt.plot(predictions[:,0] , color='turquoise', label='Predicted Usage')
plt.title('Weather Prediction')
plt.xlabel('Time')
plt.ylabel('Weather')
plt.legend()
plt.show()
