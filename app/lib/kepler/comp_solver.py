# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 14:34:00 2019

@author: Alexey.Sudbin
"""


import numpy as np
import pandas as pd
from scipy.signal import savgol_filter
from . import kepler_solver as ks

# import imp
# ks = imp.load_source('module.name', 'kepler_solver.py')


#%%



def solve(data):
    
    
    n = data['pos'].unique()
    
    regVal = np.zeros((len(n), 28))
    
    for count, p in enumerate(n):
        unit = data.loc[data['pos'] == p]
        
        resFreq = np.flip(np.array(unit.iloc[5:, 2]))
        
        normFreq = -1*(resFreq - np.mean(resFreq))
        
        peaks = ks.peak_finder(resFreq)
        
        initABCD = ks.init_comp_coeff_cal(peaks, normFreq)
        
        
        normFreqSmooth = savgol_filter(normFreq, 11, 3)
    
        finalABCD = ks.final_comp_coeff_cal(initABCD, normFreqSmooth)

        finalABCD = np.insert(finalABCD, [0,0], [int(unit.iloc[0,0]),p])
        finalABCD = np.append(finalABCD, 225)
        
        regVal[count,:] = finalABCD.astype(int)
        
    regVal = pd.DataFrame(regVal)
    regVal = regVal.rename(columns={0: 'DUT', 1: 'pos'})
    
    return regVal






