# -*- coding: utf-8 -*-
"""
Created on Sun May 17 13:13:30 2020

@author: jackz
"""

import time
import random
import numpy as np


def random_index(rate):
    start = 0
    index = 0
    randnum = random.random() * sum(rate)
    for index, scope in enumerate(rate):
        start += scope
        if randnum <= start:
            break
    return index
    

if __name__ == "__main__":    
    RateListTemp = [ round(np.random.rand(),2) for _ in range(10)]
    
    Ratio =  [0 for _ in range(len(RateListTemp))]
    Count1 = [0 for _ in range(len(RateListTemp))]
    Count2 = [0 for _ in range(len(RateListTemp))]
    Count3 = [0 for _ in range(len(RateListTemp))]
    CountTotal = 100000
    
    RunningStartTime1=time.perf_counter()
    for k in range(CountTotal):
        Position1  = random_index(RateListTemp)
        Count1[Position1] = Count1[Position1] + 1
        # print(f"Position1 {Position1}")
    RunningEndTime1=time.perf_counter()
    
    
    RateListTemp_2 = [j/sum(RateListTemp) for j in RateListTemp] 
    LenRateListTemp = len(RateListTemp)
    RunningStartTime2=time.perf_counter()
    for k in range(CountTotal):
        Position2 = np.random.choice(range(LenRateListTemp), 1, p=RateListTemp_2)
        Position2 = int(Position2)
        Count2[Position2] = Count2[Position2] + 1
        # print(f"Position2 {Position2}")
    RunningEndTime2=time.perf_counter()
    
    Ratio1 = [round( (j / CountTotal) * sum(RateListTemp) ,4) for j in Count1]
    print(f"Ratio1 {Ratio1}")
    print(f"running time:{RunningEndTime1 - RunningStartTime1}s")
    
    Ratio2 = [round( (j / CountTotal) * sum(RateListTemp) ,4) for j in Count2]
    print(f"Ratio2 {Ratio2}")
    print(f"running time:{RunningEndTime2 - RunningStartTime2}s")
    
    print(f"True Rate {RateListTemp}")

