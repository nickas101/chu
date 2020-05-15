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
import datetime



#%%

def single_tanh_func(x,a=1.5,b=1,c=85,d=0):
    return a*np.tanh(b*(x - c)) + d



def make_tanh_funcs(tanhNum):
    def tanh_funcs(x, *p):
        return sum([p[3*i]*np.tanh(p[3*i + 1]*(x - p[3*i + 2])) for i in range(tanhNum)]) + p[3*tanhNum]
    return tanh_funcs


def pol1(x,a=1,b=0):
    return a*x + b


def pol2(x,a=1,b=1,c=0):
    return a*(x**2) + b*x + c


def ratio(x, m=1, c=1, rVal=31):
    return 1/(m*x + c/((0.0625 + 0.00336 * rVal) / (1 - 0.0269 * rVal)))


def test_profiler(data):
    
    profile = {}
    
    profile['positionsList'] = data['pos'].unique()
    profile['amountDUTs'] = len(profile['positionsList'])
    profile['tempVector'] = data['temp'].unique()
    profile['tempMax'] = profile['tempVector'].max()
    profile['tempMin'] = profile['tempVector'].min()
    profile['chCoeffCset'] = data['coeffC'].unique()
    profile['tanhAmpMax'] = data['chppm'].max()
    profile['tanhAmpMin'] = data['chppm'].min()
    
    return profile
    
    



def reg_val_predict(originTemp, originFreq, finalABCD, pol2forA, ratioForB, pol2forC, pol2forCbase):
    
    DUTregVal = np.zeros(25)
    predictABCD = np.zeros(25)
    
    for i in range(0,24,3):  
        tempPoint = originTemp[-1] + finalABCD[i+2]
        
        DUTregVal[i] = np.around(31*finalABCD[i]/pol2(tempPoint, *pol2forA))
        if DUTregVal[i] > 31:    DUTregVal[i] = 31
        if DUTregVal[i] < -31:    DUTregVal[i] = -31
        
        DUTregVal[i+1] = np.around(31*(finalABCD[i+1] - ratio(tempPoint, *ratioForB, 0))/(ratio(tempPoint, *ratioForB) - ratio(tempPoint, *ratioForB, 0)))
        if DUTregVal[i+1] > 31:    DUTregVal[i+1] = 31
        if DUTregVal[i+1] < 0:    DUTregVal[i+1] = 0
        
        DUTregVal[i+2] = np.around(pol2(tempPoint, *pol2forC))
        if DUTregVal[i+2] > 63:    DUTregVal[i+2] = 63
        if DUTregVal[i+2] < 0:    DUTregVal[i+2] = 0
        
        
        predTempPoint = pol2(DUTregVal[i+2], *pol2forCbase)
        predictABCD[i+2] = predTempPoint# - tempMin
        predictABCD[i+1] = (DUTregVal[i+1]/31)*(ratio(predTempPoint, *ratioForB) - ratio(predTempPoint, *ratioForB, 0)) + ratio(predTempPoint, *ratioForB, 0)
        predictABCD[i] = (DUTregVal[i]/31)*pol2(predTempPoint, *pol2forA)
    

    f = make_tanh_funcs(8)
    cur = []
    for k in originTemp:
        cur.append(f(k, *predictABCD))
        
    res = originFreq + cur
    m = -np.mean(res)
    
    DUTregVal[24] = np.around(31*m/pol2(25, *pol2forA))
    if DUTregVal[24] > 31:    DUTregVal[24] = 31
    if DUTregVal[24] < -31:    DUTregVal[24] = -31

    predictABCD[24] = m
    
    cur = []
    for k in originTemp:
        cur.append(f(k, *predictABCD))
    
    DUTpredCurve = originFreq + cur
    
    
    # plt.figure()
    # plt.plot(originTemp, originFreq)
    # plt.plot(originTemp, cur)
    # plt.plot(originTemp, originFreq + cur)
    # plt.show()

    return DUTregVal, DUTpredCurve




def tanh_gen_characterisation(unit):
    # a = 1.6
    b0 = 0.5
    # c = [-38,-6,26,56,85]
    d0 = 0 
    
    c = unit['coeffC'].unique()  
    chCoeff = np.zeros([len(c),4])
    
    for i, regC in enumerate(c):
        test = unit.loc[unit['coeffC'] == regC]
        
        a0 = test['chppm'].iloc[1]
        c0 = test['temp'].iloc[int(len(test)/2)]
        try:   
            chCoeff[i,:], _ = curve_fit(single_tanh_func, test['temp'], test['chppm'], p0=[a0,b0,c0,d0])
        except:
            chCoeff[i,:] = np.zeros(4)*np.nan
    
    chCoeff[:,0] *= 1/8  
    
    p0 = [1,1,0]
    try:
        pol2forA, _ = curve_fit(pol2, chCoeff[:,2],chCoeff[:,0], p0=p0)
        ratioForB, _ = curve_fit(lambda x, a, b: ratio(x, a, b, 31), chCoeff[:,2],chCoeff[:,1], p0=(0.01,2))
        pol2forC, _ = curve_fit(pol2, chCoeff[:,2],c, p0=p0)
        pol2forCbase, _ = curve_fit(pol2, c, chCoeff[:,2], p0=p0)
    except:
        pol2forA = np.zeros(3)*np.nan
        ratioForB = np.zeros(2)*np.nan
        pol2forC = np.zeros(3)*np.nan
        pol2forCbase = np.zeros(3)*np.nan
    
    lb = [-min(chCoeff[:,0]), ratio(min(chCoeff[:,2]), *ratioForB, 0), -50] * 8
    lb.append(-0.5)
    ub = [min(chCoeff[:,0]), min(chCoeff[:,1]), 200] * 8 
    ub.append(0.5)

    bounds = (lb, ub)    
    
    return bounds, pol2forA, ratioForB, pol2forC, pol2forCbase, chCoeff






def final_comp_coeff_cal(normFreq, initCoeff, bounds):
#    finalCoeff = np.zeros(((len(peaks)+1)*3)+1)
    
    x = np.arange(len(normFreq))
    
    f = make_tanh_funcs(8)
    
    try:
        finalCoeffVector, pcov = curve_fit(f, x, normFreq, p0=initCoeff, maxfev=500000, ftol=1e-10, xtol=1e-10, bounds=bounds)
    except:
        finalCoeffVector = np.zeros(25)*np.nan

    return finalCoeffVector







def init_comp_coeff_cal(normFreq, peaks, bounds):
    
    initCoeffABCD = np.zeros((len(peaks)-1, 4))     
    
    for i in range(len(peaks)-1):
        initCoeffABCD[i,0] = (normFreq[peaks[i+1]] - normFreq[peaks[i]])/2
        initCoeffABCD[i,1] = 25 * abs(normFreq[peaks[i+1]] - normFreq[peaks[i]])/(peaks[i+1] - peaks[i])
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
    
    initCoeffABCD = np.clip(initCoeffABCD, bounds[0], bounds[1])
    
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
















