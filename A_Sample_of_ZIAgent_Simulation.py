# -*- coding: utf-8 -*-
"""
Created on Fri Apr 27 02:05:21 2020

@author: jackz
"""


import os
import sys
import time
sys.path.append(os.path.pardir)

os.chdir("C:\\Users\\jackz\\Desktop\\0427")

from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent


if __name__ == "__main__":  
    # initial settings
    n = 200  # total number of price grids
    PriceGridSize = 0.1  # usually 1 or 0.1 or 0.01
    TimeHorizon = 20
    deltaT = 1
    qtysize = 1000
    
    price_ini =   9.7   
    priceA_ini =  10.0  
    priceB_ini =  9.8   
        
    # parameters according to Cont paper
    Mu_Est = 0.94
    k_Est = 1.92
    Alpha_Est = 0.52
    Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
    Theta_Est = [0.71,0.81,0.68,0.56,0.47]
    Lambda_PowerLaw = [k_Est/(pow(j,Alpha_Est)) for j in range(1,6)] # Arrival rates according to power law 
    
    # set initial values for OMS and ZIAgent
    CurrentTime = 0
    OrderCount = 0
    ZIOrderBook = [[]]
        
    # ready for output
    OutputTxt = open("Output.txt","w")  # open the txt
    starttime=time.perf_counter()
    
    OMSTest = OrderManagementSystem(priceA_ini,priceB_ini,PriceGridSize,5,price_ini)
    ZIAgentTest = ZIAgent("ZIagent",OMSTest,n,PriceGridSize,Mu_Est,Lambda_Est,Theta_Est,deltaT,\
                          CurrentTime,OrderCount,ZIOrderBook)



    # during the trading period
    while (ZIAgentTest.CurrentTime <= TimeHorizon):
        ZIAgentTest.ZIAgentExecute(OMSTest)     # execute ZIAgent generator
        OMSTest.receive(ZIAgentTest.OrderIssued)  # output to OMS
        ZIAgentTest.ZIAgentUpdate(OMSTest)  # update ZIAgentTest
        
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) # print order and book results into the console
        ZIAgentTest.ZIAgentFilePrint(OMSTest,OutputTxt)    # print order and book results into the txt file
        if (ZIAgentTest.OrderCount % 200 == 0 ):
            print(ZIAgentTest.OrderCount, end=" ")   # show the progress
                
    OutputTxt.close()
        
    # report general results
    endtime=time.perf_counter()
        
    ZIAgentTest.ZIAgentPirceOrderPlot()
    ZIAgentTest.ZIAgentPirceTimePlot()
    ZIAgentTest.ZIAgentArrivalTimeFrequencyPlot()  
    ZIAgentTest.HistoryOrderBookPlot(10)      # after 10th order  
    print('4560987 in ask prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.AskPrice,4560987))
    print('0 in bid prices',ZIAgentTest.unique_index(ZIAgentTest.PricePathDF.BidPrice,0))
    
    print("the running cost:",endtime-starttime, " seconds")
    








