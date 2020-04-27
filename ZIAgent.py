# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 18:15:21 2020

@author: jackz
"""


import os
import sys
import random
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.pardir)
from LOB.LOB import LimitOrderBook
from OMS.OMS import OrderManagementSystem 


class ZIAgent(object):
    def __init__(self,name,OMSinput,n,PriceGridSize,Mu,Lambda,Theta,deltaT,\
                 CurrentTime,OrderCount,ZIOrderBook):
        self.name = name
        self.OMSinput = OMSinput
        self.n = n
        self.PriceGridSize = PriceGridSize
        self.Mu = Mu
        self.Lambda = Lambda
        self.Theta = Theta
        self.deltaT = deltaT
        self.qtysize = 1000
        self.PriceDecimals = math.ceil(math.log10(1/PriceGridSize))
        self.AskBookHistory = [list(OMSinput.ask_book)]
        self.BidBookHistory = [list(OMSinput.bid_book)]
        self.PricePathDF =  pd.DataFrame({"AskPrice":[0.0],"AskP_2":[0.0],"BidPrice":[0.0],"BidP_2":[0.0],"MarketPrice":[0.0],\
                             "ArrivalTime":[0.0],"CumulatedTime":[0.0]},\
                               index = range(1),\
                               columns=['AskPrice','AskP_2','BidPrice','BidP_2','MarketPrice','ArrivalTime','CumulatedTime'])
        self.PricePathDF.AskPrice[0] = self.PricePathDF.AskP_2[0] = OMSinput.ask
        self.PricePathDF.BidPrice[0] = self.PricePathDF.BidP_2[0] = OMSinput.bid
        self.PricePathDF.MarketPrice[0] = (OMSinput.ask + OMSinput.bid)/2
        self.CurrentTime = CurrentTime
        self.OrderCount = OrderCount
        self.ZIOrderBook = ZIOrderBook
        self.OrderArrivalTime = deltaT
        self.OrderIssued = []
    
    
    def OneShotBirthDeath(self,x,b,d,deltaT):  
    # b = birth rate, d = death rate, x = current state
    # output = [Increment 1 or -1 or 0, ArrivalTime]
        if ((b == 0) and (d == 0)):  # no birth and death
            outcome = [0,deltaT]
    
        d_temp = d
        if (x == 0) :
            d_temp = 0  # birth only
        elif (x > 0) :
            d_temp = d
            
        try:
            h = random.expovariate(b + d_temp)   # time intervel before next arrival
        except ZeroDivisionError:
            h = deltaT
            
        if (h >= deltaT) :
            outcome = [0,deltaT]
        else:
            U = random.random()
            if U < b/(b + d_temp):
                # birth occurs
                outcome = [1,h] 
            else:
                # death occurs
                outcome = [-1,h]             
        return outcome



    def OneShotBuyOrderUpdate(self,y,p,pA,deltaT,Mu,Lambda,Theta):
        if p>pA:
            return self.OneShotBirthDeath(y,0,0,deltaT)
        elif p==pA:
            return self.OneShotBirthDeath(y,Mu,0,deltaT)
        else:
            return self.OneShotBirthDeath(y,Lambda,Theta*y,deltaT)



    def OneShotSellOrderUpdate(self,z,p,pB,deltaT,Mu,Lambda,Theta):
        if p<pB:
            return self.OneShotBirthDeath(z,0,0,deltaT)
        elif p==pB:
            return self.OneShotBirthDeath(z,Mu,0,deltaT)
        else:
            return self.OneShotBirthDeath(z,Lambda,Theta*z,deltaT)



    def OneShotZIOrderIssue_PD(self,Order,pA,pB,direction,qty):
    # Order = (PriceLevel,Series('OrderStorge','Qty','Increment','ArrivalTime'))
    # direction = "buy" or "sell"
    # output = ["ZIAgent",limit or market or cancel, buy or sell, quantity, price]
        p = Order[0]
        increment = int(Order[1].Increment)
        ordertype = ""
        
        if (increment == -1):
            ordertype = "cancel"
        else:
            if (( direction == "buy" and p<pA ) or ( direction == "sell" and p>pB )) :
                ordertype = "limit"
            if (( direction == "buy" and p==pA ) or ( direction == "sell" and p==pB )) :
                ordertype = "market"
    
        output = [self.name, ordertype, direction, qty, round(p*self.PriceGridSize,self.PriceDecimals)]        
        return output



    def GetParameter(self,Parameter_Est,distance,Parameter):
    # get birth rate and death rate of different price levels from Lambda_Est Theta_Est
    # 0 if out of the distance, in Cont paper, the valid distance is 5
        n = len(Parameter_Est)
        distance = int(round(distance,0))
        if Parameter == "lambda":
            if (distance <= n and distance > 0 ):
                return Parameter_Est[distance - 1]
            else:
                return 0
        elif Parameter == "theta":
            if (distance <= n and distance > 0 ):
                return Parameter_Est[distance - 1]
            elif (distance > n):
                return Parameter_Est[n - 1]
            else:
                return 0
        else:
            return 0
    


    def EarlierOrder_PD(self,YBookRecDF,ZBookRecDF,priceA,priceB):
        YFirstIndex = YBookRecDF.ArrivalTime.idxmin()
        YTime = YBookRecDF.ArrivalTime.min() 
        YOrderFirst = (YFirstIndex,YBookRecDF.loc[YFirstIndex])
        
        ZFirstIndex = ZBookRecDF.ArrivalTime.idxmin()
        ZTime = ZBookRecDF.ArrivalTime.min()
        ZOrderFirst = (ZFirstIndex,ZBookRecDF.loc[ZFirstIndex])
        
        if (YTime < ZTime):  
            OrderIssued = self.OneShotZIOrderIssue_PD(YOrderFirst,priceA,priceB,"buy",self.qtysize)
            OrderArrivalTime = YTime
        elif (YTime > ZTime):
            OrderIssued = self.OneShotZIOrderIssue_PD(ZOrderFirst,priceA,priceB,"sell",self.qtysize)
            OrderArrivalTime = ZTime
        else:
            tempU = random.random()
            if tempU < 0.5:
                OrderIssued = self.OneShotZIOrderIssue_PD(YOrderFirst,priceA,priceB,"buy",self.qtysize)
                OrderArrivalTime = YTime
            else:
                OrderIssued = self.OneShotZIOrderIssue_PD(ZOrderFirst,priceA,priceB,"sell",self.qtysize)
                OrderArrivalTime = ZTime
        output = (OrderIssued,OrderArrivalTime)
        return output



    def ZIAgentExecute(self,OMSinput):
        # input from OMS
        if (OMSinput.ask == 4560987):
            priceA = round( self.PricePathDF.AskP_2[len(self.PricePathDF)-1] / self.PriceGridSize )
        else:
            priceA = round( OMSinput.ask / self.PriceGridSize )
        if (OMSinput.bid == 0):
            priceB = round( self.PricePathDF.BidP_2[len(self.PricePathDF)-1] / self.PriceGridSize )
        else:
            priceB = round( OMSinput.bid / self.PriceGridSize )   
            
        YBookTemp = [0 for _ in range(self.n+1)]
        for j in OMSinput.bid_book:
            YBookTemp[int(round(j.price/self.PriceGridSize))] = j.qty // self.qtysize
        
        ZBookTemp = [0 for _ in range(self.n+1)]
        for j in OMSinput.ask_book:
            ZBookTemp[int(round(j.price/self.PriceGridSize))] = j.qty // self.qtysize
        
        # ZIagent generate
        YBookRec = [ [0,0] for _ in range(self.n+1)]  # YBookRec[PriceLevel] = [Increment, ArrivalTime]
        ZBookRec = [ [0,0] for _ in range(self.n+1)]  # ZBookRec[PriceLevel] = [Increment, ArrivalTime]
        
        YBookRec = list( map(lambda x: self.OneShotBuyOrderUpdate(YBookTemp[x],x,priceA,\
                                                                  self.deltaT,\
                                                                  self.Mu,\
                                                                  self.GetParameter(self.Lambda,priceA-x,"lambda"),\
                                                                  self.GetParameter(self.Theta,priceA-x,"theta")),\
                             [_ for _ in range(self.n+1)]) )    
        ZBookRec = list( map(lambda x: self.OneShotSellOrderUpdate(ZBookTemp[x],x,priceB,\
                                                                   self.deltaT,\
                                                                   self.Mu,\
                                                                   self.GetParameter(self.Lambda,x-priceB,"lambda"),\
                                                                   self.GetParameter(self.Theta,x-priceB,"theta")),\
                              [_ for _ in range(self.n+1)]) )
       
        YBookRecDF =  pd.DataFrame({"OrderStorge":[0],"QtyStorge":[0],"Increment":[0],"ArrivalTime":[1]},\
                                   index = range(self.n+1),\
                                   columns=['OrderStorge','QtyStorge','Increment','ArrivalTime'])
        
        ZBookRecDF =  pd.DataFrame({"OrderStorge":[0],"QtyStorge":[0],"Increment":[0],"ArrivalTime":[1]},\
                                   index = range(self.n+1),\
                                   columns=['OrderStorge','QtyStorge','Increment','ArrivalTime'])
        
        YBookRecDF.OrderStorge = YBookTemp
        YBookRecDF.Increment = [j[0] for j in YBookRec]
        YBookRecDF.ArrivalTime = [j[1] for j in YBookRec]
        ZBookRecDF.OrderStorge = ZBookTemp
        ZBookRecDF.Increment = [j[0] for j in ZBookRec]
        ZBookRecDF.ArrivalTime = [j[1] for j in ZBookRec]
           
        output = self.EarlierOrder_PD(YBookRecDF,ZBookRecDF,priceA,priceB)   
        self.OrderIssued = output[0]
        self.OrderArrivalTime = output[1]
        
        self.ZIOrderBook.append(self.OrderIssued) 
        self.CurrentTime += self.OrderArrivalTime
        self.OrderCount += 1   
        
        return  output



    def PricePathUpdate(self,OMSinput):
        AskPriceAppend = OMSinput.ask
        BidPriceAppend = OMSinput.bid
        MarketPriceAppend = (AskPriceAppend + BidPriceAppend) /2
        # MarketPriceAppend = OMStest.lastprice
        if (AskPriceAppend == 4560987):
            AskP2Append = self.PricePathDF.AskP_2[len(self.PricePathDF)-1]
        else:
            AskP2Append =  AskPriceAppend   
        if (BidPriceAppend == 0):
            BidP2Append = self.PricePathDF.BidP_2[len(self.PricePathDF)-1]
        else:
            BidP2Append = BidPriceAppend
  
        PricePathAppend = pd.Series([AskPriceAppend,AskP2Append,BidPriceAppend,BidP2Append,MarketPriceAppend,\
                                  #   self.OrderArrivalTime,self.CurrentTime+self.OrderArrivalTime], \
                                      self.OrderArrivalTime,self.CurrentTime], \
                   index = ['AskPrice','AskP_2','BidPrice','BidP_2','MarketPrice','ArrivalTime','CumulatedTime'])
        return PricePathAppend
    


    def ZIAgentUpdate(self,OMSinput):
        # update recording
        # self.ZIOrderBook.append(self.OrderIssued)     
        self.AskBookHistory.append(list(OMSinput.ask_book))
        self.BidBookHistory.append(list(OMSinput.bid_book))
        self.PricePathDF = self.PricePathDF.append(self.PricePathUpdate(OMSinput),ignore_index=True)   
        # self.CurrentTime += self.OrderArrivalTime
        # self.OrderCount += 1        
 


    def OrderBookPrint(self,Book,Booktype):
    # Booktype = "ask" or "bid"
        n = len(Book)
        PriceList = [" " for _ in range(n)]
        QtyList = [0 for _ in range(n)]
        for j in range(n):
            try:
                PriceList[j] = Book[j][0]
                QtyList[j] = Book[j][1]
            except IndexError:
                continue
        
        if (Booktype.lower() == "ask") :
            for j in range(n-1,-1,-1):
                print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1])
        elif (Booktype.lower() == "bid") :
           for j in range(n):
                print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1])
        else:
            print("Booktype should be 'ask' or 'bid'! ")
    #  OrderBookPrint(OMStest.LOB.askBook.askBook_public,"Ask")



    def FileOrderBookPrint(self,Book,Booktype,txt):
    # Booktype = "ask" or "bid"
        n = len(Book)
        PriceList = [" " for _ in range(n)]
        QtyList = [0 for _ in range(n)]
        for j in range(n):
            try:
                PriceList[j] = Book[j][0]
                QtyList[j] = Book[j][1]
            except IndexError:
                continue
        
        if (Booktype.lower() == "ask") :
            for j in range(n-1,-1,-1):
                print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1],file=txt)
        elif (Booktype.lower() == "bid") :
            for j in range(n):
                print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1],file=txt)
        else:
            print("Booktype should be 'ask' or 'bid'! ",file=txt)
    


    def ZIAgentConsolePrint(self,OMSinput):
        print("at kth order:", self.OrderCount)   
        print("the new order is:", self.OrderIssued)
        print("arrival time interval:", self.OrderArrivalTime )
        print("the cumulated time: ", self.CurrentTime)
        # print("the cumulated time: ", self.CurrentTime + self.OrderArrivalTime)
            
        self.OrderBookPrint(OMSinput.ask_book,"ask")
        self.OrderBookPrint(OMSinput.bid_book,"bid")
        print("askPrice:",OMSinput.ask)   
        print("bidPrice:",OMSinput.bid)    
        print("\n")



    def ZIAgentFilePrint(self,OMSinput,OUTPUTTXT):
        print("at kth order:", self.OrderCount,file=OUTPUTTXT)   
        print("the new order is:", self.OrderIssued,file=OUTPUTTXT)
        print("arrival time interval:", self.OrderArrivalTime,file=OUTPUTTXT )
        print("the cumulated time: ", self.CurrentTime,file=OUTPUTTXT)
        # print("the cumulated time: ", self.CurrentTime +  self.OrderArrivalTime,file=OutputTxt)
        
        self.FileOrderBookPrint(OMSinput.ask_book,"ask",OUTPUTTXT)
        self.FileOrderBookPrint(OMSinput.bid_book,"bid",OUTPUTTXT)
        print("askPrice:",OMSinput.ask,file=OUTPUTTXT)   
        print("bidPrice:",OMSinput.bid,file=OUTPUTTXT)    
        print("\n",file=OUTPUTTXT)



    def HistoryOrderBookPlot(self,k):   
        AskBook = self.AskBookHistory[k]
        BidBook = self.BidBookHistory[k]
        
        AskN = len(AskBook)
        AskPriceList = [" " for _ in range(AskN)]
        AskQtyList = [0 for _ in range(AskN)]
        for j in range(AskN):
            try:
                AskPriceList[j] = AskBook[j].price
                AskQtyList[j] = AskBook[j].qty
            except IndexError:
                continue
        
        AskBookDF =  pd.DataFrame({"Price":[0],"AskQty":[0]},\
                                   index = range(AskN),\
                                   columns=['Price','AskQty'])
        AskBookDF.Price = AskPriceList
        AskBookDF.AskQty = AskQtyList
    
        BidN = len(BidBook)
        BidPriceList = [" " for _ in range(BidN)]
        BidQtyList = [0 for _ in range(BidN)]
        for j in range(BidN):
            try:
                k = BidN - j -1
                BidPriceList[k] = BidBook[j].price
                BidQtyList[k] = BidBook[j].qty
            except IndexError:
                continue
        
        BidBookDF =  pd.DataFrame({"Price":[0],"BidQty":[0]},\
                                   index = range(BidN),\
                                   columns=['Price','BidQty'])
        BidBookDF.Price = BidPriceList
        BidBookDF.BidQty = BidQtyList
        
        try :
            AskPriceTemp = AskPriceList[0]
        except IndexError:
            AskPriceTemp = 4560987
       
        try :
            BidPriceTemp = BidPriceList[-1]
        except IndexError:
            BidPriceTemp = 0
        
        SpreadPriceList = []
        
        if (AskPriceTemp == 4560987) or (BidPriceTemp == 0):
            SpreadN = 0
        else:
            SpreadN = int(round((AskPriceTemp - BidPriceTemp)/self.PriceGridSize) - 1 )
        
        for j in range(1,SpreadN+1):
            SpreadPriceList.append(BidPriceTemp + self.PriceGridSize * j )
        
        SpreadBookDF =  pd.DataFrame({"Price":[0]},\
                                   index = range(SpreadN),\
                                   columns=['Price'])
        SpreadBookDF.Price = SpreadPriceList

        OrderBookDF = (BidBookDF.append(SpreadBookDF,ignore_index=True,sort=True)).append(\
                      AskBookDF,ignore_index=True,sort=True)
 
        ind = np.arange(len(OrderBookDF.Price))  # the x locations for the groups
        width = 0.35  # the width of the bars     
        fig, ax = plt.subplots()
        ax.bar(ind - width/2, OrderBookDF.BidQty, width, color='Red', label='Bid')
        ax.bar(ind + width/2, OrderBookDF.AskQty, width,color='Green', label='Ask')
        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_ylabel('Qty')
        ax.set_title('Order Book')
        plt.xticks(ind,OrderBookDF.Price)
        plt.title('After %d th order'%k)
        ax.legend()
        plt.show()
    
    
    
    def unique_index(self,L,f):
    # find all the indexs of f appeared in L
        return [i for (i,v) in enumerate(L) if v==f]    



    def ZIAgentPirceOrderPlot(self):
        plt.plot(self.PricePathDF.AskP_2,color ='green',lw=1) 
        plt.plot(self.PricePathDF.BidP_2,color ='red',lw=1) 
        # plt.plot(PricePathDF.MarketPrice,color ='yellow',lw=1) 
        plt.ylabel('Price')
        plt.xlabel('Order Sequence')
        plt.show()

    def ZIAgentPirceTimePlot(self):
        plt.plot(self.PricePathDF.CumulatedTime,self.PricePathDF.AskP_2,color ='green',lw=1)
        plt.plot(self.PricePathDF.CumulatedTime,self.PricePathDF.BidP_2,color ='red',lw=1)
        # plt.plot(PricePathDF.CumulatedTime,PricePathDF.MarketPrice,color ='yellow',lw=1)
        plt.ylabel('Price')
        plt.xlabel('Time')
        plt.show() 


    def ZIAgentArrivalTimeFrequencyPlot(self):
        print("Average arrival time: ",np.mean(self.PricePathDF.ArrivalTime))
        print("The frequency distribution of ArricalTime: \n")
        plt.hist(self.PricePathDF.ArrivalTime, bins = 20, range = (0,self.PricePathDF.ArrivalTime.max()) )
        plt.show()
    
    
