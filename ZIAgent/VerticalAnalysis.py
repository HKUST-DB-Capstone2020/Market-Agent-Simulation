# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 02:02:29 2020

@author: Lenovo
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

# Analysis for limit and market order
class OrderBookAnalysis:
    def __init__(self,ZIOrderBook):
        self.ZIOrderBook = ZIOrderBook
    
    
    def OrderClassify(self,Ordertype,Direction,ZIOrderBook):
        if (Ordertype == 'limit' and Direction =='buy'):           
            OrderRec = [[]]
            for i in range(1,len(ZIOrderBook)):
                if (ZIOrderBook[i][1]== 'limit' and ZIOrderBook[i][2]== 'buy'):
                    distance = round((AskPricePath[i-1]-ZIOrderBook[i][4])/PriceGridSize)
                    OrderRec.append([distance, CumArTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'limit' and Direction =='sell'):            
            OrderRec = [[]]
            for i in range(1,len(ZIOrderBook)):                
                 if (ZIOrderBook[i][1]== 'limit' and ZIOrderBook[i][2]== 'sell'):
                     distance = round((ZIOrderBook[i][4]-BidPricePath[i-1])/PriceGridSize)
                     OrderRec.append([distance, CumArTime[i]])
                 else:
                     OrderRec = OrderRec
        elif (Ordertype == 'cancel' and Direction =='buy'):
            OrderRec = [[]]
            for i in range(1,len(ZIOrderBook)):
                if (ZIOrderBook[i][1]== 'cancel' and ZIOrderBook[i][2]== 'buy'):
                    distance = round((AskPricePath[i-1]-ZIOrderBook[i][4])/PriceGridSize)
                    OrderRec.append([distance, CumArTime[i]])
                else:
                    OrderRec = OrderRec 
        elif (Ordertype == 'cancel' and Direction =='sell'):
            OrderRec = [[]]
            for i in range(1,len(ZIOrderBook)):
                if (ZIOrderBook[i][1]== 'cancel' and ZIOrderBook[i][2]== 'sell'):
                    distance = round((ZIOrderBook[i][4]-BidPricePath[i-1])/PriceGridSize)
                    OrderRec.append([distance, CumArTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'market' and Direction =='buy'):
            OrderRec = []
            for i in range(1,len(ZIOrderBook)):
                if (ZIOrderBook[i][1]== 'market' and ZIOrderBook[i][2]== 'buy'):
                    OrderRec.append(CumArTime[i])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'market' and Direction =='sell'):
            OrderRec = []
            for i in range(1,len(ZIOrderBook)):
                if (ZIOrderBook[i][1]== 'market' and ZIOrderBook[i][2]== 'sell'):
                    OrderRec.append(CumArTime[i])
                else:
                    OrderRec = OrderRec
    
        return(OrderRec)
        

    def limitOrderAnalysis(self,Ordertype,Direction,ZIOrderBook):
        OrderRec = self.OrderClassify(Ordertype,Direction,ZIOrderBook)
        limitOrderCount = [[], [], [], [], []]
        for i in range(1,len(OrderRec)):
            j = int(round(OrderRec[i][0]))
            limitOrderCount[j-1].append(OrderRec[i][1])

        test = []
        testDF = pd.DataFrame(columns=('Distance', 'Para_Est', 'OrderNum'))
        for i in range(len(limitOrderCount)):
            test.append([i+1, len(limitOrderCount[i])/limitOrderCount[i][-1],\
                     len(limitOrderCount[i])])
            testDF.loc[i] = [i+1, len(limitOrderCount[i])/limitOrderCount[i][-1],\
                      len(limitOrderCount[i])]
        
        return(test,testDF,limitOrderCount)


    def marketOrderAnalysis(self,Ordertype,Direction,ZIOrderBook):
        OrderRec = self.OrderClassify(Ordertype,Direction,ZIOrderBook)
        test = [0, len(OrderRec)/OrderRec[-1], len(OrderRec)]
        testDF = pd.DataFrame(columns=('Distance', 'Para_Est', 'OrderNum'))
        testDF.loc[0] = [0, len(OrderRec)/OrderRec[-1], len(OrderRec)]
        
        return(test,testDF)
    
    def CancelOrderCount(self,Ordertype,Direction,ZIOrderBook):
        OrderRec = self.OrderClassify(Ordertype,Direction,ZIOrderBook)
        cancelOrderCount = [[], [], [], [], [], [], [], [], [], []]
        for i in range(1,len(OrderRec)):
            j = int(round(OrderRec[i][0]))
            cancelOrderCount[j-1].append(OrderRec[i][1])
    
        count = []
        countDF = pd.DataFrame(columns=('Distance', 'OrderNum'))
        for i in range(len(cancelOrderCount)):
            count.append([i+1, len(cancelOrderCount[i])])
            countDF.loc[i] = [i+1, len(cancelOrderCount[i])]
        
        return(count,countDF,cancelOrderCount)   
        
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
    Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
    Theta_Est = [0.71,0.81,0.68,0.56,0.47]
    
    # set initial values for OMS and ZIAgent
    CurrentTime = 0
    OrderCount = 0
    ZIOrderBook = [[]]
        
    OMSTest = OrderManagementSystem(priceA_ini,priceB_ini,PriceGridSize,5,price_ini)
    ZIAgentTest = ZIAgent("ZIagent",OMSTest,n,PriceGridSize,Mu_Est,Lambda_Est,Theta_Est,deltaT,\
                          CurrentTime,OrderCount,ZIOrderBook)
    # ready for output
    starttime=time.perf_counter()

    # during the trading period
    while (ZIAgentTest.CurrentTime <= TimeHorizon):
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) 
        # ZIAgentTest.ZIAgentExecute(OMSTest) 
        ZIAgentTest.ZIAgentExecute(OMSTest,n,PriceGridSize) # execute ZIAgent generator
        OMSTest.receive(ZIAgentTest.OrderIssued)  # output to OMS
        ZIAgentTest.ZIAgentUpdate(OMSTest)  # update ZIAgentTest
        
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) # print order and book results
        if (ZIAgentTest.OrderCount % 200 == 0 ):
            print(ZIAgentTest.OrderCount, end=" ")
                       
    # report general results
    endtime=time.perf_counter()
    print("the running cost:",endtime-starttime, " seconds")
    
    
    ZIOrderBookTest = ZIAgentTest.ZIOrderBook
    CumArTime = ZIAgentTest.PricePathDF.CumulatedTime
    AskPricePath = ZIAgentTest.PricePathDF.AskP_2
    BidPricePath = ZIAgentTest.PricePathDF.BidP_2
    
    Res = OrderBookAnalysis(ZIOrderBookTest)
    TotalLimitBid = len(Res.OrderClassify('limit','buy',ZIOrderBookTest))-1
    TotalLimitAsk = len(Res.OrderClassify('limit','sell',ZIOrderBookTest))-1
    TotalMarketBid = len(Res.OrderClassify('market','buy',ZIOrderBookTest))
    TotalMarketAsk = len(Res.OrderClassify('market','sell',ZIOrderBookTest))
    TotalCancelBid = len(Res.OrderClassify('cancel','buy',ZIOrderBookTest))-1
    TotalCancelAsk = len(Res.OrderClassify('cancel','sell',ZIOrderBookTest))-1
    TotalOrderNum = len(ZIOrderBookTest)-1
    
    print("Total Limit Bid Order: ",TotalLimitBid)
    print("Total Limit Ask Order: ",TotalLimitAsk)
    print("Total Market Bid Order: ",TotalMarketBid)
    print("Total Market Ask Order: ",TotalMarketAsk)
    print("Total Cancel Bid Order: ",TotalCancelBid)
    print("Total Cancel Ask Order: ",TotalCancelAsk)
    print("Total Order Number:", TotalOrderNum)
    

    BidlimitRes = Res.limitOrderAnalysis('limit','buy',ZIOrderBookTest)[1]
    AsklimitRes = Res.limitOrderAnalysis('limit','sell',ZIOrderBookTest)[1]

    BidmarketRes = Res.marketOrderAnalysis('market','buy',ZIOrderBookTest)[1]
    AskmarketRes = Res.marketOrderAnalysis('market','sell',ZIOrderBookTest)[1]
   
    BidOrderRes = pd.concat([BidmarketRes,BidlimitRes])
    AskOrderRes = pd.concat([AskmarketRes,AsklimitRes])
    
    
    print(BidOrderRes)
    print(AskOrderRes)
    
    BidcancelCount = Res.CancelOrderCount('cancel','buy',ZIOrderBookTest)[1]
    AskcancelCount = Res.CancelOrderCount('cancel','sell',ZIOrderBookTest)[1]

    
    TotalcancelBid = np.sum(BidcancelCount.OrderNum)
    TotalcancelAsk = np.sum(AskcancelCount.OrderNum)
    
    print(BidcancelCount)
    print(AskcancelCount)
   