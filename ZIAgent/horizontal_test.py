# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 23:44:23 2020

@author: Lenovo
"""

#import numpy as np
#import pandas as pd
import pytest
import time
#import math
import os
import sys
sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook


os.chdir("C:\\Users\\Lenovo\\Desktop")

from OMS.OMS import OrderManagementSystem 
from ZIAgent import ZIAgent
from HorizontalAnalysis import HorizontalAnalysis
        
MAX_PRICE_LEVELS = 200  # total number of price grids
TICK_SIZE = 0.1  # usually 1 or 0.1 or 0.01
QTYSIZE = 1000
    
PRICE_START =   9.7   
PRICE_A_START =  10.0  
PRICE_B_START =  9.8   
        
# parameters according to Cont paper
MU_Est = 0.94
LAMBDA_Est = [1.85,1.51,1.09,0.88,0.77]
THETA_Est = [0.71,0.81,0.68,0.56,0.47]
    
CurrentTime = 0
OrderCount = 0
ZIOrderBook = [[]]

SampleSize = 10000
OMSTest = OrderManagementSystem(PRICE_A_START,PRICE_B_START,TICK_SIZE,5,PRICE_START)
ZIAgentTest = ZIAgent("ZIagent",OMSTest,MAX_PRICE_LEVELS,TICK_SIZE,QTYSIZE,MU_Est,LAMBDA_Est,THETA_Est,\
                          CurrentTime,OrderCount,ZIOrderBook)
       
HorizontalTest = HorizontalAnalysis(SampleSize,OMSTest,ZIAgentTest)
    
    
starttime=time.perf_counter()

OrderBookSample = HorizontalTest.OrderCollection(SampleSize,OMSTest,ZIAgentTest)
arrival_time = OrderBookSample[0]
order_issued = OrderBookSample[1]
endtime=time.perf_counter()
print("the running cost:",endtime-starttime, " seconds")

#print("Limit&Market Buy Order Test:")
#print(HorizontalTest.ResultTest('birth', 'buy', OMSTest, order_issued, arrival_time))
#print("Limit&Market Sell Order Test:")
#print(HorizontalTest.ResultTest('birth', 'sell', OMSTest, order_issued, arrival_time))
#print("Cancel Buy Order Test:")
#print(HorizontalTest.ResultTest('death', 'buy', OMSTest, order_issued, arrival_time))
#print("Cancel Sell Order Test:")
#print(HorizontalTest.ResultTest('death', 'sell', OMSTest, order_issued, arrival_time))
    

class TestHorizontal:
    def test_Birth_Buy(self):
        z = abs(HorizontalTest.ResultTest('birth', 'buy', OMSTest, order_issued, arrival_time).z_value)
        for i in range(len(z)):
            assert z.loc[i] < 1.96
        
    def test_Birth_Sell(self):
        z = abs(HorizontalTest.ResultTest('birth', 'sell', OMSTest, order_issued, arrival_time).z_value)
        for i in range(len(z)):
            assert z.loc[i] < 1.96
    
                   
    def test_Death_Buy(self):
        z = abs(HorizontalTest.ResultTest('death', 'buy', OMSTest, order_issued, arrival_time).z_value)
        for i in range(len(z)):
            assert z.loc[i] < 1.96

    def test_Death_Sell(self):
        z = abs(HorizontalTest.ResultTest('death', 'sell', OMSTest, order_issued, arrival_time).z_value)
        for i in range(len(z)):
            assert z.loc[i] < 1.96
        


if __name__ == "__main__":
    
    pytest.main()
