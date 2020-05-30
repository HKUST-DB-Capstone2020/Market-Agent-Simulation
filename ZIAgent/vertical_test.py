# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:46:10 2020

@author: Lenovo
"""

import pytest
import time
import os
import sys
sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook


os.chdir("C:\\Users\\Lenovo\\Desktop")

from OMS.OMS import OrderManagementSystem 
from ZIAgent import ZIAgent
from VerticalAnalysis import VerticalAnalysis
        
MAX_PRICE_LEVELS = 200  # total number of price grids
TICK_SIZE = 0.1  # usually 1 or 0.1 or 0.01
TimeHorizon = 3600
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

#### vertical test
starttime_v=time.perf_counter()

# during the trading period
while (ZIAgentTest.CurrentTime <= TimeHorizon):
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) 
        # ZIAgentTest.ZIAgentExecute(OMSTest) 
    ZIAgentTest.Execute(OMSTest)                  # execute ZIAgent generator
    OMSTest.receive(ZIAgentTest.OrderIssued)      # output to OMS
    ZIAgentTest.Update(OMSTest)                   # update ZIAgentTest
        
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) # print order and book results
    if (ZIAgentTest.OrderCount % 500 == 0 ):
        print(ZIAgentTest.OrderCount, end=" ")
                       
    # report general results
endtime_v=time.perf_counter()
print("the running cost:",endtime_v-starttime_v, " seconds")



VerticalTest = VerticalAnalysis(ZIAgentTest)


class TestVertical:
    # vertical test
    def test_Bid_Parameter(self):
        z = abs(VerticalTest.OrderAnalysis('buy').Para_Real-VerticalTest.OrderAnalysis('buy').Para_Est)
        for i in range(len(z)):
            assert z.loc[i] <= 0.05
        
    def test_Ask_Parameter(self):
        z = abs(VerticalTest.OrderAnalysis('sell').Para_Real-VerticalTest.OrderAnalysis('sell').Para_Est)
        for i in range(len(z)):
            assert z.loc[i] <= 0.05
    
if __name__ == "__main__":
    
    pytest.main()


    
    