# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 18:53:22 2020

@author: Lenovo
"""
"""
Horizontal analysis of Limit Order Book:
Given an initial order book status, the Horizontal Tests will simulate the first arrived order 10000 or even more times, 
and verify the distribution of each type of order.
"""
import numpy as np
import pandas as pd
import time
import math
import os
import sys
sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook


#os.chdir("C:\\Users\\Lenovo\\Desktop")

from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent



class HorizontalAnalysis:
    def __init__(self,SampleSize,OMSTest,ZIAgentTest):
        self.SampleSize = SampleSize
        self.OMSTest = OMSTest
        self.ZIAgentTest = ZIAgentTest
        self.TICK_SIZE = ZIAgentTest.TICK_SIZE
        self.qtysize = ZIAgentTest.qtysize
        self.PRICE_A_START = OMSTest.ask
        self.PRICE_B_START = OMSTest.bid
        self.MU_Est = ZIAgentTest.MU
        self.LAMBDA_Est = ZIAgentTest.LAMBDA
        self.THETA_Est = ZIAgentTest.THETA

    def OrderCollection(self, SampleSize, OMSTest, ZIAgentTest):    
    
        k = 0
        OrderIssued = [[]]
        ArrivalTime = []
    
        while(k < SampleSize):
            ZIAgentTest.Execute(OMSTest)                  # execute ZIAgent generator
            OrderIssued.append(ZIAgentTest.OrderIssued)
            ArrivalTime.append(ZIAgentTest.OrderArrivalTime)
            k += 1
    
        OrderIssued.pop(0)
        
        return(ArrivalTime, OrderIssued)

    def OrderClassify(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        if (Ordertype == 'limit' and Direction =='buy'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'limit' and OrderIssued[i][2]== 'buy'):
                    distance = round((self.PRICE_A_START-OrderIssued[i][4])/self.TICK_SIZE)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'limit' and Direction =='sell'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'limit' and OrderIssued[i][2]== 'sell'):
                    distance = round((OrderIssued[i][4]-self.PRICE_B_START)/self.TICK_SIZE)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec
        elif (Ordertype == 'cancel' and Direction =='buy'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'cancel' and OrderIssued[i][2]== 'buy'):
                    distance = round((self.PRICE_A_START-OrderIssued[i][4])/self.TICK_SIZE)
                    OrderRec.append([distance, ArrivalTime[i]])
                else:
                    OrderRec = OrderRec 
        elif (Ordertype == 'cancel' and Direction =='sell'):
            OrderRec = []
            for i in range(len(ArrivalTime)):
                if (OrderIssued[i][1]== 'cancel' and OrderIssued[i][2]== 'sell'):
                    distance = round((OrderIssued[i][4]-self.PRICE_B_START)/self.TICK_SIZE)
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


    def LimitOrderAnalysis(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        # Ordertype should be "limit" or "cancel"
        OrderRec = self.OrderClassify(Ordertype,Direction,OrderIssued,ArrivalTime)
        limitOrderCount = [[], [], [], [], [], []]
        # only collect distance from 1 to 6
        for i in range(len(OrderRec)):
            j = int(round(OrderRec[i][0]))
            limitOrderCount[j-1].append(OrderRec[i][1])

        OrderNum = pd.DataFrame(columns=('Distance', 'OrderNum'))
        OrderTime = pd.DataFrame(columns=('Distance', 'ArrivalTime_Mean', 'ArrivalTime_Std'))
        for i in range(len(limitOrderCount)):
            OrderNum.loc[i] = [i+1,len(limitOrderCount[i])] 
            OrderTime.loc[i] = [i+1, np.mean(limitOrderCount[i]),np.std(limitOrderCount[i])]
        
        OrderStat = pd.merge(OrderNum,OrderTime)
        
        return(OrderNum,OrderTime,OrderStat)
        

    def MarketOrderAnalysis(self, Ordertype,Direction,OrderIssued,ArrivalTime):
        
        OrderRec = self.OrderClassify(Ordertype,Direction,OrderIssued,ArrivalTime)
        OrderNum = pd.DataFrame(columns=('Distance', 'OrderNum'))
        OrderTime = pd.DataFrame(columns=('Distance', 'ArrivalTime_Mean', 'ArrivalTime_Std'))
        
        OrderNum.loc[0] = [0,len(OrderRec)] 
        OrderTime.loc[0] = [0, np.mean(OrderRec),np.std(OrderRec)]
        
        OrderStat = pd.merge(OrderNum,OrderTime)
        
        return(OrderNum,OrderTime,OrderStat)
        
    def BirthRate(self,distance, Lambda, Mu):
        if distance > 5:
            return 0
        elif distance > 0 and distance <= 5:
            return Lambda[distance -1]
        elif distance == 0:
            return Mu
    
    def DeathRate(self,distance, Theta):
        if distance > 5:
            return Theta[-1]
        elif distance <= 5:
            return Theta[distance-1]
        
    def AskOrderStat(self, OMSTest,OrderIssued,ArrivalTime):       
        AskOrder = pd.DataFrame(columns=('Distance', 'Qty','BirthRate',"DeathRate"))
        Distance_Ask = []
        birthrate = []
        for i in range(len(OMSTest.ask_book)):
            dis = int(round((OMSTest.ask_book[i][0]-self.PRICE_B_START)/self.TICK_SIZE))
            Distance_Ask.append(dis)
            
        Distance_Ask_Max = max(Distance_Ask)

        for i in range(Distance_Ask_Max+1):
            birthrate.append(self.BirthRate(i, self.LAMBDA_Est, self.MU_Est))
        
        AskOrder['Distance'] = list(range(Distance_Ask_Max+1))
        AskOrder['BirthRate'] = birthrate
        
        for i in range(len(OMSTest.ask_book)):
            distance = int(round((OMSTest.ask_book[i][0]-self.PRICE_B_START)/self.TICK_SIZE))
            for j in (range(Distance_Ask_Max+1)):
                if distance == j:
                    
                    qty = int(round(OMSTest.ask_book[i][1]/self.qtysize))
                    deathrate = self.DeathRate(distance,self.THETA_Est)*qty
                    AskOrder.Qty.iloc[j] = qty
                    AskOrder.DeathRate.iloc[j] = deathrate
        
        AskOrder = AskOrder.fillna(0)
        
        limitsell = self.LimitOrderAnalysis('limit','sell',OrderIssued,ArrivalTime)[0]
        marketsell = self.MarketOrderAnalysis('market','sell',OrderIssued,ArrivalTime)[0]
        cancelsell = self.LimitOrderAnalysis('cancel','sell',OrderIssued,ArrivalTime)[0]

        cancel0 = pd.DataFrame(columns=('Distance', 'CanceledNum'))
        cancel0.loc[0] = [0,0] # cancel number of marker order should be zero
        cancelsell.columns = ['Distance', 'CanceledNum']
        CanceledOrder = pd.concat([cancel0,cancelsell], axis=0 ,ignore_index=True) 


        GenOrder = pd.concat([marketsell,limitsell], axis=0 ,ignore_index=True) 
        GenOrder.columns = ['Distance', 'GeneratedNum']

        OrderNum = pd.merge(GenOrder,CanceledOrder)
        askorderstat = pd.merge(AskOrder,OrderNum)
        
        return(askorderstat)
        
    
    def BidOrderStat(self, OMSTest,OrderIssued,ArrivalTime):       
        BidOrder = pd.DataFrame(columns=('Distance', 'Qty','BirthRate',"DeathRate"))
        Distance_Bid = []
        birthrate = []
        for i in range(len(OMSTest.bid_book)):
            dis = int(round((self.PRICE_A_START-OMSTest.bid_book[i][0])/self.TICK_SIZE))
            Distance_Bid.append(dis)
            
        Distance_Bid_Max = max(Distance_Bid)

        for i in range(Distance_Bid_Max+1):
            birthrate.append(self.BirthRate(i, self.LAMBDA_Est, self.MU_Est))
        
        BidOrder['Distance'] = list(range(Distance_Bid_Max+1))
        BidOrder['BirthRate'] = birthrate
        
        for i in range(len(OMSTest.bid_book)):
            distance = int(round((self.PRICE_A_START-OMSTest.bid_book[i][0])/self.TICK_SIZE))
            for j in (range(Distance_Bid_Max+1)):
                if distance == j:                   
                    qty = int(round(OMSTest.bid_book[i][1]/self.qtysize))
                    deathrate = self.DeathRate(distance,self.THETA_Est)*qty
                    BidOrder.Qty.iloc[j] = qty
                    BidOrder.DeathRate.iloc[j] = deathrate
        
        BidOrder = BidOrder.fillna(0)
        
        limitbuy = self.LimitOrderAnalysis('limit','buy',OrderIssued,ArrivalTime)[0]
        marketbuy = self.MarketOrderAnalysis('market','buy',OrderIssued,ArrivalTime)[0]
        cancelbuy = self.LimitOrderAnalysis('cancel','buy',OrderIssued,ArrivalTime)[0]

        cancel0 = pd.DataFrame(columns=('Distance', 'CanceledNum'))
        cancel0.loc[0] = [0,0] # cancel number of marker order should be zero
        cancelbuy.columns = ['Distance', 'CanceledNum']
        CanceledOrder = pd.concat([cancel0,cancelbuy], axis=0 ,ignore_index=True) 


        GenOrder = pd.concat([marketbuy,limitbuy], axis=0 ,ignore_index=True) 
        GenOrder.columns = ['Distance', 'GeneratedNum']

        OrderNum = pd.merge(GenOrder,CanceledOrder)
        bidorderstat = pd.merge(BidOrder,OrderNum)
        
        return(bidorderstat)
        
    
    def ResultTest(self, OrderType, Direction, OMSTest,OrderIssued,ArrivalTime):
        askorder = self.AskOrderStat(OMSTest,OrderIssued,ArrivalTime)
        bidorder = self.BidOrderStat(OMSTest,OrderIssued,ArrivalTime)
        TotalRate = round(sum(askorder.BirthRate)+sum(askorder.DeathRate)\
                  +sum(bidorder.BirthRate)+sum(bidorder.DeathRate),2)
        Result = pd.DataFrame(columns=('Distance', 'TheoProb','RealProb', 'TheoStd', 'z_value','P_or_F'))
    
        if (Direction == 'buy' and OrderType == 'birth'):            
            Result['Distance'] = bidorder['Distance']
            Result['RealProb'] = bidorder.GeneratedNum/self.SampleSize #
            Result['TheoProb'] = bidorder.BirthRate/TotalRate #
        elif (Direction == 'buy' and OrderType == 'death'):
            Result['Distance'] = bidorder['Distance']
            Result['RealProb'] = bidorder.CanceledNum/self.SampleSize #
            Result['TheoProb'] = bidorder.DeathRate/TotalRate #
        elif (Direction == 'sell' and OrderType == 'birth'):
            Result['Distance'] = askorder['Distance']
            Result['RealProb'] = askorder.GeneratedNum/self.SampleSize #
            Result['TheoProb'] = askorder.BirthRate/TotalRate #
        elif (Direction == 'sell' and OrderType == 'death'):
            Result['Distance'] = askorder['Distance']
            Result['RealProb'] = askorder.CanceledNum/self.SampleSize #
            Result['TheoProb'] = askorder.DeathRate/TotalRate #
            
        Result['TheoStd'] = ((1-Result.TheoProb)*Result.TheoProb)**0.5 #
        Result = Result.fillna(0)
    
        for i in range(len(Result['Distance'])):
            if Result.TheoProb.loc[i] > 0:
                diff = (Result.TheoProb.loc[i]-Result.RealProb.loc[i])
                Result.z_value.loc[i] = (diff*math.sqrt(self.SampleSize))/Result.TheoStd.loc[i]
        
        for i in range(len(Result['z_value'])):
            if abs(Result.z_value.loc[i]) < 1.96:
                Result.P_or_F.loc[i] = 'PASS'
            elif abs(Result.z_value.loc[i]) >= 1.96:
                Result.P_or_F.loc[i] = 'FAIL'
        
        Result = Result.drop(columns = ['TheoStd'])
    
        return(Result)
       
        

if __name__ == "__main__": 
    
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

    SampleSize = 1000000
    OMSTest = OrderManagementSystem(PRICE_A_START,PRICE_B_START,TICK_SIZE,5,PRICE_START)
    ZIAgentTest = ZIAgent(NAME                =   "ZIagent", 
                          OMSinput            =   OMSTest, 
                          MAX_PRICE_LEVELS    =   MAX_PRICE_LEVELS, 
                          TICK_SIZE           =   TICK_SIZE, 
                          #QTYSIZE             =   qtysize, 
                          MU                  =   MU_Est, 
                          LAMBDA              =   LAMBDA_Est, 
                          THETA               =   THETA_Est, 
                          CurrentTime         =   CurrentTime, 
                          OrderCount          =   OrderCount, 
                          ZIOrderBook         =   ZIOrderBook)
       
    HorizontalTest = HorizontalAnalysis(SampleSize,OMSTest,ZIAgentTest)
    
    
    starttime=time.perf_counter()

    OrderBookSample = HorizontalTest.OrderCollection(SampleSize,OMSTest,ZIAgentTest)
    arrival_time = OrderBookSample[0]
    order_issued = OrderBookSample[1]
    endtime=time.perf_counter()
    print("the running cost:",endtime-starttime, " seconds")
    
    ### start analysis
    
   
    print("Ask Book Statistics:")
    print(HorizontalTest.AskOrderStat(OMSTest,order_issued,arrival_time))
    
    print("Bid Book Statistics:")
    print(HorizontalTest.BidOrderStat(OMSTest,order_issued,arrival_time))
    
    print("Limit&Market Buy Order Test:")
    print(HorizontalTest.ResultTest('birth', 'buy', OMSTest, order_issued, arrival_time))
    print("Limit&Market Sell Order Test:")
    print(HorizontalTest.ResultTest('birth', 'sell', OMSTest, order_issued, arrival_time))
    print("Cancel Buy Order Test:")
    print(HorizontalTest.ResultTest('death', 'buy', OMSTest, order_issued, arrival_time))
    print("Cancel Sell Order Test:")
    print(HorizontalTest.ResultTest('death', 'sell', OMSTest, order_issued, arrival_time))
    
    
    
    
    

