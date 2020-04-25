# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 13:00:19 2020

@author: Alexey.Sudbin
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.signal import savgol_filter, argrelextrema
import csv
import datetime



#%%


def make_tanh_funcs(tanhNum):
    def tanh_funcs(x, *p):
        return sum([p[3*i]*np.tanh(p[3*i + 1]*(x - p[3*i + 2])) for i in range(tanhNum)]) + p[3*tanhNum]
    return tanh_funcs





def single_tanh_func(x,a=1.5,b=1,c=85,d=0):
    return a*np.tanh(b*(x - c)) + d




def final_comp_coeff_cal(initCoeff, normFreq):
#    finalCoeff = np.zeros(((len(peaks)+1)*3)+1)
    
    x = np.arange(len(normFreq))
    
    f = make_tanh_funcs(8)
    
    finalCoeffVector, pcov = curve_fit(f, x, normFreq, p0=initCoeff, maxfev=500000, ftol=1.49012e-04, xtol=1.49012e-04)

    return finalCoeffVector







def init_comp_coeff_cal(peaks, normFreq):
    
    initCoeffABCD = np.zeros((len(peaks)-1, 4))     
    
    for i in range(len(peaks)-1):
        initCoeffABCD[i,0] = abs(normFreq[peaks[i]] - normFreq[peaks[i+1]])/2
        initCoeffABCD[i,1] = 25 * (normFreq[peaks[i+1]] - normFreq[peaks[i]])/(peaks[i+1] - peaks[i])
        initCoeffABCD[i,2] = peaks[i] + (peaks[i+1] - peaks[i])/2
        initCoeffABCD[i,3] = normFreq[int(initCoeffABCD[i,2])]
        
        
    initCoeffD = np.sum(initCoeffABCD[:,3])
    
    initCoeffABC = np.delete(initCoeffABCD, 3, 1)
    initCoeffABC = initCoeffABC.ravel()
    
    initCoeffABCD = np.append(initCoeffABC, initCoeffD)
    f = make_tanh_funcs(8)
    cur = []
    for k in range(len(normFreq)):
        cur.append(f(k, *initCoeffABCD))
    
    initCoeffABCD[-1] = initCoeffABCD[-1] + (np.mean(normFreq) - np.mean(cur))
    
    return initCoeffABCD
    









def peak_finder(normFreq):

    normFreq = savgol_filter(normFreq, 7, 2)
    
    peaksMax = np.array(argrelextrema(normFreq, np.greater, order=8))
    peaksMin = np.array(argrelextrema(normFreq, np.less, order=8))
    
    peaksMax = peaksMax.ravel()
    peaksMin = peaksMin.ravel()
    
    peaks = np.concatenate([np.array([0]), peaksMax, peaksMin, np.array([len(normFreq)-1])])    
    
    peaks.sort()
    
    if len(peaks) < 9:
        while len(peaks) != 9:
            imax = np.argmax(np.abs(np.diff(normFreq[peaks])))
            peaks = np.insert(peaks, imax+1, peaks[imax] + int((peaks[imax+1] - peaks[imax])/2))
            
    elif len(peaks) > 9:
        while len(peaks) != 9:
            peaks = peaks[:-1]
                       
        #print("It happens!")
        
    #print(peaks)
    
    return peaks
           








def load_3_comp_xl(path):
    
    testData = {}
     
    z = pd.read_excel(path, "3-Comp.txt", usecols = "A:F")         #load "3-Comp Solver.xlsm" file 
    
    n = z['Unnamed: 0'][61]                     # number of DUTs
    firstIndex = 63
    lastIndex = (z.loc[z["Unnamed: 0"].str.contains('Script completed', regex=True) == True].index[0]) - 1
    
    z = z.loc[range(firstIndex,lastIndex), :]
    z = z.reset_index(drop=True)
    
    # clean up the datatime rubbish in the DUT number column
    for i in range(z.shape[0]):
        if type(z['Unnamed: 1'][i]) is datetime.datetime:
                z.at[i, 'Unnamed: 1'] = z.loc[(i-1), 'Unnamed: 1']
    if n > 15:
    
        k = 0
        for c in range(2):
            for u in range(15):
                
                      
                res = z.loc[(z['Unnamed: 0'] == c) & (z['Unnamed: 1'] == (u+1)) & pd.isnull(z['Unnamed: 4'])].apply(pd.to_numeric)
                if res.size == 0:
                    continue
                 
                res = res.drop(['Unnamed: 0','Unnamed: 1','Unnamed: 4', 'Unnamed: 5'], axis=1)
                res = res.rename(columns={'Unnamed: 2': 'temp', 'Unnamed: 3': 'resppm'})
                res['temp'] = res['temp'].round(0)
                res = res.reset_index(drop=True)
                
                data = z.loc[(z['Unnamed: 0'] == c) & (z['Unnamed: 1'] == (u+1)) & pd.notnull(z['Unnamed: 4'])].apply(pd.to_numeric)
                data = data.drop(['Unnamed: 0','Unnamed: 1','Unnamed: 3'], axis=1)
                data = data.rename(columns={'Unnamed: 2': 'temp', 'Unnamed: 4': 'coeffD', 'Unnamed: 5': 'chppm'})
                data['temp'] = data['temp'].round(0)
                data = data.reset_index(drop=True)
                data['resppm'] = res['resppm']
                
                data['chppm'] = data['chppm'] - data['resppm']

                k += 1                
                testData[k] = data
    else:
        
        k = 0
        for u in range(15):
                   
            res = z.loc[(z['Unnamed: 0'] == u) & pd.isnull(z['Unnamed: 3'])].apply(pd.to_numeric)
            if res.size == 0:
                continue
          
            res = res.drop(['Unnamed: 0','Unnamed: 3','Unnamed: 4', 'Unnamed: 5'], axis=1)
            res = res.rename(columns={'Unnamed: 1': 'temp', 'Unnamed: 2': 'resppm'})
            res['temp'] = res['temp'].round(0)
            res = res.reset_index(drop=True)
            
            data = z.loc[(z['Unnamed: 0'] == u) & pd.notnull(z['Unnamed: 3'])].apply(pd.to_numeric)
            data = data.drop(['Unnamed: 0','Unnamed: 5','Unnamed: 2'], axis=1)
            data = data.rename(columns={'Unnamed: 1': 'temp', 'Unnamed: 3': 'coeffD', 'Unnamed: 4': 'chppm'})
            data['temp'] = data['temp'].round(0)
            data = data.reset_index(drop=True)
            data['resppm'] = res['resppm']
            
            data['chppm'] = data['chppm'] - data['resppm']

            k += 1            
            testData[k] = data

    if k != n:
        print('k and n are not equel')

    return testData, n
















