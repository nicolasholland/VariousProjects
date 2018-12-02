#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 22:00:22 2018

@author: dutchman
"""
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import BaggingRegressor
from sklearn.svm import SVR


from pandas_datareader import data
sns.set()

def goog_close(tstamp, delta='30d'):
    """ goog close timeseries of last 30 days """
    start = tstamp - pd.Timedelta(delta)
    retval = data.DataReader('GOOG', start=start,
                           end=tstamp, data_source='iex')

    retval.index = pd.to_datetime(retval.index)
    return retval['close']

def create_forecasts(ts, plot=False):
    """ create a few forecasts by fitting models and extrapolating one time step """
    x = np.array([c for c in range(len(ts))])
    y = np.asarray(ts)

    def train_poly(degree):
        """ train linear regression """
        poly_model = make_pipeline(PolynomialFeatures(degree),
                                   LinearRegression())
        poly_model.fit(x[:, np.newaxis], y)
        return poly_model

    predictors = [train_poly(d) for d in [3, 4]]

    tree = DecisionTreeRegressor()
    bag = BaggingRegressor(tree, n_estimators=100, max_samples=0.8,
                        random_state=1)

    bag.fit(x[:, np.newaxis], y)
    predictors.append(bag)

    svm = SVR(kernel='rbf', gamma=0.01)
    svm.fit(x[:, np.newaxis], y)
    predictors.append(svm)

    xfit = np.array([i for i in range(len(ts)+1)])
    yfits = [p.predict(xfit[:, np.newaxis]) for p in predictors]

    if plot:
        plot_forecasts(x, y, yfits, xfit, predictors)

    retval = pd.DataFrame([yfits[c][-1] for c in range(4)]).T
    retval = retval.set_index(np.array([ts.index[-1] + pd.Timedelta('1d')]))
    return retval



def plot_forecasts(x, y, yfits, xfit, predictors):
    """ plot forecasts """
    plt.plot(x,y, label="NASDAQ: GOOG")
    for yf in range(len(yfits)):
        plt.plot(xfit, yfits[yf], label=str(type(predictors[yf])))
    plt.legend()

    upper = [max([yfits[c][t] for c in range(4)]) for t in xfit]
    lower = [min([yfits[c][t] for c in range(4)]) for t in xfit]

    plt.fill_between(xfit, lower, upper, facecolor='blue',
                     interpolate=True, alpha=.2)



# plot of one year
#goog_close(pd.Timestamp('2018-10-31'), delta='365d').plot(label="NASDAQ: GOOG")
#plt.legend()

#forecasts = pd.concat([create_forecasts(goog_close(d)) for d in pd.date_range('2018-10-01', periods=30)])
#upper = forecasts.T.max()
#lower = forecasts.T.min()

goog = goog_close(pd.Timestamp('2018-10-31'), delta='30d')

