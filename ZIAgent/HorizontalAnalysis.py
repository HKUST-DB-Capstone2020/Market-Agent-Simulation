# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:53:22 2020

@author: Lenovo
"""
"""
Horizontal analysis of Limit Order Book:
The aim of Class OrderDistributionAnalysis is to analyze the first generated order. 
The class can simulate first generated order 10000 or even more times, and calculate the distribution of each type of order.
However, the criteria is subjective. That is, one may need to make judgement based on the output.
"""
import numpy as np
import pandas as pd
import pytest
import time
import os
import sys
sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook


os.chdir("C:\\Users\\Lenovo\\Desktop")

from OMS.OMS import OrderManagementSystem 
from ZIAgent import ZIAgent

class OrderDistributionAnalysis:
    def __init__(self,SampleSize):
        self.SampleSize = SampleSize
         
    def OrderCollection(self, SampleSize):    
     
        CurrentTime = 0
        OrderCount = 0
        ZIOrderBook = [[]]
    
        k = 0
        OrderIssued = [[]]
        ArrivalTime = []
        OMSTest = OrderManagementSystem(priceA_ini,priceB_ini,PriceGridSize,5,price_ini)
    
        while(k < SampleSize):
            ZIAgentTest = ZIAgent("ZIagent",OMSTest,n,PriceGridSize,Mu_Est,Lambda_Est,Theta_Est,deltaT,\
                          CurrentTime,OrderCount,ZIOrderBook)
            ZIAgentTest.ZIAgentExecute(OMSTest,n,PriceGridSize)
            OrderIssued.append(ZIAgentTest.OrderIssued)
            ArrivalTime.append(ZIAgentTest.OrderArrivalTime)
            k += 1
    
        OrderIssued.pop(0)
        
        return(ArrivalTime, OrderIssued)

    def OrderClassify(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        if (Ordertype == 'limit' and Direction =='buy'):
            OrderRec = [[]]
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'limit' and OrderIssued[i][2]== 'buy'):
                    distance = round((priceA_ini-OrderIssued[i][4])/PriceGridSize)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'limit' and Direction =='sell'):
            OrderRec = [[]]
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'limit' and OrderIssued[i][2]== 'sell'):
                    distance = round((OrderIssued[i][4]-priceB_ini)/PriceGridSize)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'cancel' and Direction =='buy'):
            OrderRec = [[]]
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'cancel' and OrderIssued[i][2]== 'buy'):
                    distance = round((priceA_ini-OrderIssued[i][4])/PriceGridSize)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec 
        elif (Ordertype == 'cancel' and Direction =='sell'):
            OrderRec = [[]]
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'cancel' and OrderIssued[i][2]== 'sell'):
                    distance = round((OrderIssued[i][4]-priceB_ini)/PriceGridSize)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'market' and Direction =='buy'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'market' and OrderIssued[i][2]== 'buy'):
                    OrderRec.append(ArrivalTime[i])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'market' and Direction =='sell'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'market' and OrderIssued[i][2]== 'sell'):
                    OrderRec.append(ArrivalTime[i])
                else:
                    OrderRec = OrderRec
    
        return(OrderRec)


    def limitOrderAnalysis(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        # Ordertype should be "limit" or "cancel"
        OrderRec = self.OrderClassify(Ordertype,Direction,OrderIssued,ArrivalTime)
        limitOrderCount = [[], [], [], [], [], []]
        for i in range(1,len(OrderRec)):
            j = int(round(OrderRec[i][0]))
            limitOrderCount[j-1].append(OrderRec[i][1])

        test = []
        testDF = pd.DataFrame(columns=('Distance', 'ArrivalTime_Mean', \
                                   'ArrivalTime_Std', 'OrderNum'))
        for i in range(len(limitOrderCount)):
            test.append([i+1, np.mean(limitOrderCount[i]),np.std(limitOrderCount[i]),\
                     len(limitOrderCount[i])])
            testDF.loc[i] = [i+1, np.mean(limitOrderCount[i]),np.std(limitOrderCount[i]),\
                      len(limitOrderCount[i])] 
        
        return(test,testDF)

    def marketOrderAnalysis(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        OrderRec = self.OrderClassify(Ordertype,Direction,OrderIssued,ArrivalTime)
        test = [0, np.mean(OrderRec), np.std(OrderRec),\
                len(OrderRec), len(OrderRec)/SampleSize ]
        testDF = pd.DataFrame(columns=('Distance', 'ArrivalTime_Mean', \
                                   'ArrivalTime_Std', 'OrderNum'))
        testDF.loc[0] = [0, np.mean(OrderRec), np.std(OrderRec),len(OrderRec)]
    
        return(test,testDF)


if __name__ == "__main__": 
    n = 200  # total number of price grids
    PriceGridSize = 0.1  # usually 1 or 0.1 or 0.01
    deltaT = 1
    qtysize = 1000
    
    price_ini =   9.7   
    priceA_ini =  10.0  
    priceB_ini =  9.8   
        
    # parameters according to Cont paper
    Mu_Est = 0.94
    Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
    Theta_Est = [0.71,0.81,0.68,0.56,0.47]

    SampleSize = 10000
    OrderBookTest = OrderDistributionAnalysis(SampleSize)
    
    starttime=time.perf_counter()

    OrderBookSample = OrderBookTest.OrderCollection(SampleSize)
    ArrivalTime = OrderBookSample[0]
    OrderIssued = OrderBookSample[1]
    endtime=time.perf_counter()
    print("the running cost:",endtime-starttime, " seconds")

    print(OrderBookTest.limitOrderAnalysis('limit','buy',OrderIssued,ArrivalTime)[1])
    print(OrderBookTest.limitOrderAnalysis('limit','sell',OrderIssued,ArrivalTime)[1])
    print(OrderBookTest.marketOrderAnalysis('market','buy',OrderIssued,ArrivalTime)[1])
    print(OrderBookTest.marketOrderAnalysis('market','sell',OrderIssued,ArrivalTime)[1])
    print(OrderBookTest.limitOrderAnalysis('cancel','buy',OrderIssued,ArrivalTime)[1])
    print(OrderBookTest.limitOrderAnalysis('cancel','sell',OrderIssued,ArrivalTime)[1])

