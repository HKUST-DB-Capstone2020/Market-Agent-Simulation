

import os
import sys
# import random
# import math
import time
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
sys.path.append(os.path.pardir)
os.chdir("C:\\Users\\jackz\\Desktop\\0514 draft")
# from LOB.LOB import LimitOrderBook
from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent



if __name__ == "__main__":  
    # initial settings
    MAX_PRICE_LEVELS = 200  # total number of price grids
    TICK_SIZE = 0.1  # usually 1 or 0.1 or 0.01
    TimeHorizon = 60
    qtysize = 1000
    
    PRICE_START =   9.7   
    PRICE_A_START =  10.0  
    PRICE_B_START =  9.8   
        
    # parameters according to Cont paper
    MU_Est = 0.94
    LAMBDA_Est = [1.85,1.51,1.09,0.88,0.77]
    THETA_Est = [0.71,0.81,0.68,0.56,0.47]
    """
    K_Est = 1.92
    ALPHA_Est = 0.52
    LAMBDA_PowerLaw = [K_Est/(pow(j,ALPHA_Est)) for j in range(1,6)] # Arrival rates according to power law 
    """
    
    # set initial values for OMS and ZIAgent
    CurrentTime = 0
    OrderCount = 0
    ZIOrderBook = [[]]
        
    # ready for output
    RunningStartTime=time.perf_counter()
    
    OMSTest = OrderManagementSystem(PRICE_A_START,PRICE_B_START,TICK_SIZE,5,PRICE_START)
    ZIAgentTest = ZIAgent("ZIagent",OMSTest,MAX_PRICE_LEVELS,TICK_SIZE,MU_Est,LAMBDA_Est,THETA_Est,\
                          CurrentTime,OrderCount,ZIOrderBook)


    with open("Output.txt","w") as OUTPUTTXT:
        # during the trading period
        while (ZIAgentTest.CurrentTime <= TimeHorizon):
            ZIAgentTest.Execute(OMSTest)                  # execute ZIAgent generator
            OMSTest.receive(ZIAgentTest.OrderIssued)      # output to OMS
            ZIAgentTest.Update(OMSTest)                   # update ZIAgentTest
            
            # ZIAgentTest.ConsolePrint(OMSTest)          # print order and book results into the console
            ZIAgentTest.FilePrint(OMSTest,OUTPUTTXT)     # print order and book results into the txt file
            if (ZIAgentTest.OrderCount % 500 == 0 ):
                print(ZIAgentTest.OrderCount, end=" ")   # show the progress in the console
                
        
    # report general results
    RunningEndTime=time.perf_counter()
        
    ZIAgentTest.PirceOrderPlot()
    ZIAgentTest.PirceTimePlot()
    ZIAgentTest.ArrivalTimeFrequencyPlot()  
    ZIAgentTest.HistoryOrderBookPlot(10)       # after 10th order  
    print('4560987 in ask prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.AskPrice,OMSTest.MAX_PRICE))
    print('0 in bid prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.BidPrice,OMSTest.MIN_PRICE))
        
    print(f"the running cost: {RunningEndTime - RunningStartTime} seconds")
    

