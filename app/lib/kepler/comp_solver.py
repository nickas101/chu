# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:34:00 2019

@author: Alexey.Sudbin
"""


import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from . import kepler_solver as ks

#import imp
#ks = imp.load_source('module.name', 'kepler_solver.py')


#%%



def solve(data, cut):
    
    
    profile = ks.test_profiler(data)
    
    n = data['pos'].unique()
    
    #regVal = np.zeros((len(n), 28)).astype(int)
    regVal = np.zeros((len(n), 28))
    predCurve = pd.DataFrame(columns=['Temp'])
    
    lb = [-0.2, 0.025, -50] * 8
    lb.append(-0.5)
    ub = [0.2, 0.4, 200] * 8 
    ub.append(0.5)

    bounds = (lb, ub)
    
    for count, p in enumerate(n):
        unit = data.loc[data['pos'] == p]       
    
        bounds, pol2forA, ratioForB, pol2forC, pol2forCbase, chCoeff = ks.tanh_gen_characterisation(unit)
        
        originTemp = np.array(unit.iloc[cut:, 2])
        originFreq = np.array(unit.iloc[cut:, 3])
        resFreq = np.flip(originFreq)
        
        normFreq = -1*(resFreq - np.mean(resFreq))
        
        peaks = ks.peak_finder(resFreq)
        
        initABCD = ks.init_comp_coeff_cal(normFreq, peaks, bounds)
        
        
        normFreqSmooth = savgol_filter(normFreq, 11, 3)
    
        finalABCD = ks.final_comp_coeff_cal(normFreqSmooth, initABCD, bounds)
        
        DUTregVal, DUTpredCurve = ks.reg_val_predict(originTemp, originFreq, finalABCD, pol2forA, ratioForB, pol2forC, pol2forCbase)

        DUTregVal = np.insert(DUTregVal, [0,0], [int(unit.iloc[0,0]),p])
        DUTregVal = np.append(DUTregVal, 255)
        
        predCurve[str(p)] = DUTpredCurve
        
        #regVal[count,:] = DUTregVal.astype(int)
        regVal[count,:] = DUTregVal
        
    predCurve['Temp'] = originTemp
    regVal = pd.DataFrame(regVal)
    regVal = regVal.rename(columns={0: 'DUT', 1: 'pos'})
    
    return regVal, predCurve













