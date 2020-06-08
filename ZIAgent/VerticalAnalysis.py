# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 02:02:29 2020

@author: Lenovo
"""

"""
Given a time horizon, the Vertical Test will examine whether orders generated during this period is normal, 
and further estimate parameter MU and LAMBDA. Vertical test cannot estimate parameter THETA.
"""
#import numpy as np
import pandas as pd
import time
import os
import sys
sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook


#os.chdir("C:\\Users\\Lenovo\\Desktop")

from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent

# Analysis for limit and market order
class VerticalAnalysis:
    def __init__(self,ZIAgentTest):
        self.ZIAgentTest = ZIAgentTest
        self.ZIOrderBook = ZIAgentTest.ZIOrderBook
        # self.CumArTime = ZIAgentTest.PricePathDF.CumulatedTime
        # self.AskPricePath = ZIAgentTest.PricePathDF.AskP_2
        # self.BidPricePath = ZIAgentTest.PricePathDF.BidP_2
        
        self.CumArTime = ZIAgentTest.CurrentTimePath
        self.AskPricePath = ZIAgentTest.AskPricePath
        self.BidPricePath = ZIAgentTest.BidPricePath        
        
        self.TICK_SIZE = ZIAgentTest.TICK_SIZE
        self.MU = ZIAgentTest.MU
        self.LAMBDA = ZIAgentTest.LAMBDA
        self.THETA = ZIAgentTest.THETA
    
    
    
    def OrderClassify(self,Ordertype,Direction):
        if (Ordertype == 'limit' and Direction =='buy'):           
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):
                if (self.ZIOrderBook[i][1]== 'limit' and self.ZIOrderBook[i][2]== 'buy'):
                    distance = round((self.AskPricePath[i-1]-self.ZIOrderBook[i][4])/self.TICK_SIZE)
                    OrderRec.append([i,distance,self.CumArTime[i],self.AskPricePath[i-1],self.ZIOrderBook[i][4]])
                else:
                    OrderRec = OrderRec
            
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','Distance','ArrivalTime','AskPrice', 'QuotePrice'])
            
        elif (Ordertype == 'limit' and Direction =='sell'):            
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):                
                 if (self.ZIOrderBook[i][1]== 'limit' and self.ZIOrderBook[i][2]== 'sell'):
                     distance = round((self.ZIOrderBook[i][4]-self.BidPricePath[i-1])/self.TICK_SIZE)
                     OrderRec.append([i,distance,self.CumArTime[i],self.BidPricePath[i-1],self.ZIOrderBook[i][4]])
                 else:
                     OrderRec = OrderRec
            
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','Distance','ArrivalTime','BidPrice', 'QuotePrice'])
        elif (Ordertype == 'cancel' and Direction =='buy'):
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):
                if (self.ZIOrderBook[i][1]== 'cancel' and self.ZIOrderBook[i][2]== 'buy'):
                    distance = round((self.AskPricePath[i-1]-self.ZIOrderBook[i][4])/self.TICK_SIZE)
                    OrderRec.append([i,distance,self.CumArTime[i],self.AskPricePath[i-1],self.ZIOrderBook[i][4]])
                else:
                    OrderRec = OrderRec 
            
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','Distance','ArrivalTime','AskPrice', 'QuotePrice'])
            
        elif (Ordertype == 'cancel' and Direction =='sell'):
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):
                if (self.ZIOrderBook[i][1]== 'cancel' and self.ZIOrderBook[i][2]== 'sell'):
                    distance = round((self.ZIOrderBook[i][4]-self.BidPricePath[i-1])/self.TICK_SIZE)
                    OrderRec.append([i,distance,self.CumArTime[i],self.BidPricePath[i-1],self.ZIOrderBook[i][4]])
                else:
                    OrderRec = OrderRec
                    
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','Distance','ArrivalTime','BidPrice', 'QuotePrice'])
            
        elif (Ordertype == 'market' and Direction =='buy'):
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):
                if (self.ZIOrderBook[i][1]== 'market' and self.ZIOrderBook[i][2]== 'buy'):
                    OrderRec.append([i,self.CumArTime[i]])
                else:
                    OrderRec = OrderRec
            
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','ArrivalTime'])
            
        elif (Ordertype == 'market' and Direction =='sell'):
            OrderRec = []
            for i in range(1,len(self.ZIOrderBook)):
                if (self.ZIOrderBook[i][1]== 'market' and self.ZIOrderBook[i][2]== 'sell'):
                    OrderRec.append([i,self.CumArTime[i]])
                else:
                    OrderRec = OrderRec
            OrderRec = pd.DataFrame(OrderRec,\
                       columns=['OrderID','ArrivalTime'])
    
        return(OrderRec)
        

    def OrderAnalysis(self, Direction):
        
        if (Direction == 'sell'):
            LimitOrderRec = self.OrderClassify('limit', 'sell')
            MarketOrderRec = self.OrderClassify('market', 'sell')
        if (Direction == 'buy'):
            LimitOrderRec = self.OrderClassify('limit', 'buy')
            MarketOrderRec = self.OrderClassify('market', 'buy')
            
        limitOrderCount = [[], [], [], [], []]
        for i in range(len(LimitOrderRec.Distance)):
            j = int(round(LimitOrderRec.Distance.loc[i]))
            limitOrderCount[j-1].append(LimitOrderRec.ArrivalTime.loc[i])

        LimitResult = pd.DataFrame(columns=('Distance', 'Para_Real', 'Para_Est', 'OrderNum','P_or_F'))
        for i in range(len(limitOrderCount)):
            
            LimitResult.loc[i] = [i+1, self.LAMBDA[i], len(limitOrderCount[i])/limitOrderCount[i][-1],\
                      len(limitOrderCount[i]),0]
              
        MarketArrivalTime = []
        for i in range(len(MarketOrderRec.ArrivalTime)):
            MarketArrivalTime.append(MarketOrderRec.ArrivalTime.loc[i])
            
        MarketResult = pd.DataFrame(columns=('Distance','Para_Real', 'Para_Est', 'OrderNum','P_or_F'))
        MarketResult.loc[0] = [0, self.MU, len(MarketArrivalTime)/MarketArrivalTime[-1], len(MarketArrivalTime),0]
        
        Result = pd.concat([MarketResult,LimitResult],ignore_index=True)
        for i in range(len(Result['Distance'])):
            if (abs(Result.Para_Real.loc[i]-Result.Para_Est.loc[i]) <= 0.05):
                Result.P_or_F.loc[i] = 'PASS'
            elif (abs(Result.Para_Real.loc[i]-Result.Para_Est.loc[i]) > 0.05):
                Result.P_or_F.loc[i] = 'FAIL'
                
        return(Result)

    
    def CancelOrderCount(self,Direction):
        OrderRec = self.OrderClassify('cancel',Direction)
        Distance_Max = int(round(max(OrderRec.Distance)))
        OrderCount = pd.DataFrame(columns=('Distance', 'OrderNum'))
        OrderCount['Distance'] = list(range(1, Distance_Max+1))
        
        OrderCount = OrderCount.fillna(0)
        for i in range(len(OrderRec.Distance)):
            j = int(round(OrderRec.Distance.loc[i]))
            OrderCount.OrderNum.iloc[j-1] = OrderCount.OrderNum.iloc[j-1]+1
          
        return(OrderCount)   
        
        
if __name__ == "__main__":  
     # initial settings
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
    
    # set initial values for OMS and ZIAgent
    CurrentTime = 0
    OrderCount = 0
    ZIOrderBook = [[]]
        
    OMSTest = OrderManagementSystem(PRICE_A_START,PRICE_B_START,TICK_SIZE,5,PRICE_START)
    ZIAgentTest = ZIAgent(NAME                =   "ZIagent", 
                          OMSinput            =   OMSTest, 
                          MAX_PRICE_LEVELS    =   MAX_PRICE_LEVELS, 
                          TICK_SIZE           =   TICK_SIZE, 
                          # QTYSIZE             =   qtysize, 
                          MU                  =   MU_Est, 
                          LAMBDA              =   LAMBDA_Est, 
                          THETA               =   THETA_Est, 
                          CurrentTime         =   CurrentTime, 
                          OrderCount          =   OrderCount, 
                          ZIOrderBook         =   ZIOrderBook)
    

    # ready for output
    starttime=time.perf_counter()

    # during the trading period
    while (ZIAgentTest.CurrentTime <= TimeHorizon):
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) 
        # ZIAgentTest.ZIAgentExecute(OMSTest) 
        ZIAgentTest.Execute(OMSTest)                  # execute ZIAgent generator
        OMSTest.receive(ZIAgentTest.OrderIssued)      # output to OMS
        ZIAgentTest.Update(OMSTest)                   # update ZIAgentTest
        
        # ZIAgentTest.ZIAgentConsolePrint(OMSTest) # print order and book results
        if (ZIAgentTest.OrderCount % 5000 == 0 ):
            print(ZIAgentTest.OrderCount, end=" ")
                       
    # report general results
    endtime=time.perf_counter()
    print("the running cost:",endtime-starttime, " seconds")
    
    
    VerticalTest = VerticalAnalysis(ZIAgentTest)
    
    # verify order number
    TotalLimitBid = len(VerticalTest.OrderClassify('limit','buy'))
    TotalLimitAsk = len(VerticalTest.OrderClassify('limit','sell'))
    TotalMarketBid = len(VerticalTest.OrderClassify('market','buy'))
    TotalMarketAsk = len(VerticalTest.OrderClassify('market','sell'))
    TotalCancelBid = len(VerticalTest.OrderClassify('cancel','buy'))
    TotalCancelAsk = len(VerticalTest.OrderClassify('cancel','sell'))
    TotalOrderNum = len(ZIAgentTest.ZIOrderBook)-1
    
    print("Total Limit Bid Order: ",TotalLimitBid)
    print("Total Limit Ask Order: ",TotalLimitAsk)
    print("Total Market Bid Order: ",TotalMarketBid)
    print("Total Market Ask Order: ",TotalMarketAsk)
    print("Total Cancel Bid Order: ",TotalCancelBid)
    print("Total Cancel Ask Order: ",TotalCancelAsk)
    print("Total Order Number:", TotalOrderNum)
    
    #  parameter test result
    print("Bid Limit&Market Parameter Test Result:")
    print(VerticalTest.OrderAnalysis('buy'))
    print("Ask Limit&Market Parameter Test Result:")
    print(VerticalTest.OrderAnalysis('sell'))
    
    # cancel order count
    print("Bid Cancel Order Count:")
    print(VerticalTest.CancelOrderCount('buy'))
    print("Ask Cancel Order Count:")
    print(VerticalTest.CancelOrderCount('sell'))

    
    
    
    
   
    
    
    
   
