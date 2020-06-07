# -*- coding: utf-8 -*-
"""
Created on Tue May 19 02:33:41 2020

@author: jackz
"""



# import os
# import sys
import random
import math
# import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# sys.path.append(os.path.pardir)
# from LOB.LOB import LimitOrderBook
from OMS.OMS import OrderManagementSystem 

import numba as nb

@nb.jit('int_(float64[:])')
def rand_nb(prob):
    return np.searchsorted(np.cumsum(prob)/prob.sum(), np.random.random(), side="right")
    


class ZIAgent(object):
    def __init__(self,NAME,OMSinput,MAX_PRICE_LEVELS,TICK_SIZE,MU,LAMBDA,THETA,\
                 CurrentTime,OrderCount,ZIOrderBook,QTYSIZE=1000,ALPHA=0.52,K=1.92,):
        self.NAME = NAME
        self.OMSinput = OMSinput
        self.MAX_PRICE_LEVELS = MAX_PRICE_LEVELS
        self.TICK_SIZE = TICK_SIZE
        self.MU = MU
        self.LAMBDA = LAMBDA
        self.THETA = THETA
        self.qtysize = QTYSIZE
        self.PriceDecimals = math.ceil(math.log10(1/TICK_SIZE))
        self.ALPHA = ALPHA
        self.K = K
        
        self.LAMBDA_PowerLaw = np.array([self.K/(pow(j,self.ALPHA)) for j in range(1,6)] )
        self.AskBookHistory = [list(OMSinput.ask_book)]
        self.BidBookHistory = [list(OMSinput.bid_book)]
        self.CurrentTime = CurrentTime
        self.OrderCount = OrderCount
        self.ZIOrderBook = ZIOrderBook
        self.OrderArrivalTime = 0
        self.OrderIssued = []
        self.AskPricePath = np.array([OMSinput.ask])
        self.BidPricePath = np.array([OMSinput.bid])
        self.CurrentTimePath = np.array(CurrentTime)
        self.ArrivalTimePath = np.array(0)
    
     
    def Execute(self,OMSinput):
        if (OMSinput.ask == OMSinput.MAX_PRICE):
        # if (OMSinput.ask == 4560987):
            self.priceA = int(round( self.AskPricePath[-1] / self.TICK_SIZE ))
        else:
            self.priceA = int(round( OMSinput.ask / self.TICK_SIZE ))
        
        if (OMSinput.bid  == OMSinput.MIN_PRICE):
        # if (OMSinput.bid == 0):
            self.priceB = int(round( self.BidPricePath[-1] / self.TICK_SIZE ))
        else:
            self.priceB = int(round( OMSinput.bid / self.TICK_SIZE )) 
        
        
        priceRange = np.arange(0, self.MAX_PRICE_LEVELS)
        
        
        """
        # use power law to calculate limit order rates
        bidLimitRate = np.zeros(self.MAX_PRICE_LEVELS)
        bidLimitRate[self.priceA-5:self.priceA] = self.LAMBDA_PowerLaw[::-1]

        askLimitRate = np.zeros(self.MAX_PRICE_LEVELS)
        askLimitRate[self.priceB+1 : self.priceB+1+5] = self.LAMBDA_PowerLaw   
        
        """
        
        # use Estimated values of limit order rates
        bidLimitRate = np.zeros(self.MAX_PRICE_LEVELS)
        bidValidDist = self.priceA - max(1,self.priceA-5)
        bidLimitRate[self.priceA-bidValidDist : self.priceA] = self.LAMBDA[:bidValidDist:][::-1]
        
        askLimitRate = np.zeros(self.MAX_PRICE_LEVELS)
        askLimitRate[self.priceB+1:self.priceB+1+5] = self.LAMBDA
        
        
        # cancel order rates
        BidBookArray = np.zeros(self.MAX_PRICE_LEVELS,dtype=np.int64)
        for j in OMSinput.bid_book:
            BidBookArray[int(round(j.price/self.TICK_SIZE))] = j.qty // self.qtysize
    
        AskBookArray = np.zeros(self.MAX_PRICE_LEVELS,dtype=np.int64)
        for j in OMSinput.ask_book:
            AskBookArray[int(round(j.price/self.TICK_SIZE))] = j.qty // self.qtysize            
        
        bidCancelTheta = self.THETA[-1] * (self.priceA-5 > priceRange) 
        bidCancelTheta[self.priceA-bidValidDist : self.priceA] = self.THETA[:bidValidDist:][::-1]
        bidCancelRate = bidCancelTheta * BidBookArray
        
        askcancelTheta = self.THETA[-1] * (self.priceB+5 < priceRange) 
        askcancelTheta[self.priceB+1 : self.priceB+1+5] = self.THETA
        askCancelRate = askcancelTheta * AskBookArray    
        
        # market order rates
        bidMarketOrderRate = self.MU
        askMarketOrderRate = self.MU     
        
        
        totalRate =   bidLimitRate.sum() + askLimitRate.sum()       \
                    + bidCancelRate.sum() + askCancelRate.sum()         \
                    + bidMarketOrderRate + askMarketOrderRate           
        
        Pchoice = np.array([bidLimitRate.sum()  , askLimitRate.sum()  , \
                            bidCancelRate.sum() , askCancelRate.sum() , \
                            bidMarketOrderRate  , askMarketOrderRate]) / totalRate
        # index = np.random.choice(6, p = Pchoice )
        index = rand_nb(Pchoice)
        
        orderDirection = ""
        orderType = ""
        
        
        if index == 0:
        # bid limit order
            orderDirection = "buy"
            orderType = "limit"
            orderPrice = round(self.TICK_SIZE * rand_nb(bidLimitRate/bidLimitRate.sum()),self.PriceDecimals)
        elif index == 1:
        # ask limit order
            orderDirection = "sell"
            orderType = "limit"
            orderPrice = round(self.TICK_SIZE * rand_nb(askLimitRate/askLimitRate.sum()),self.PriceDecimals)
        elif index == 2:
        # bid cancel order
            orderDirection = "buy"
            orderType = "cancel"
            orderPrice = round(self.TICK_SIZE * rand_nb(bidCancelRate/bidCancelRate.sum()),self.PriceDecimals)
        elif index == 3:
        # ask cancel order
            orderDirection = "sell"
            orderType = "cancel"
            orderPrice = round(self.TICK_SIZE * rand_nb(askCancelRate/askCancelRate.sum()),self.PriceDecimals)
        elif index == 4:
        # bid market order
            orderDirection = "buy"
            orderType = "market"
            orderPrice = round(self.TICK_SIZE * self.priceA,self.PriceDecimals)     
        elif index == 5:
        # ask market order
            orderDirection = "sell"
            orderType = "market"
            orderPrice = round(self.TICK_SIZE * self.priceB,self.PriceDecimals)
        else:
            print("ERROR in ZIAgent Order Execute at {self.OrderCount}! ")
            print(index)
            print(f"Pchoice {Pchoice}")
            print(f"BidBookArray {BidBookArray}")
            print(f"AskBookArray {AskBookArray}")
            print(f"bidLimitRate  {bidLimitRate}")   
            print(f"askLimitRate  {askLimitRate}") 
            print(f"bidCancelRate  {bidCancelRate}")
            print(f"askCancelRate  {askCancelRate}")
        
        
        self.OrderIssued = ["ZIagent", orderType, orderDirection, self.qtysize, np.float(orderPrice)]
        self.OrderArrivalTime = random.expovariate(totalRate)
        
        self.ZIOrderBook.append(self.OrderIssued) 
        self.CurrentTime += self.OrderArrivalTime
        self.CurrentTimePath = np.append(self.CurrentTimePath,self.CurrentTime)
        self.ArrivalTimePath = np.append(self.ArrivalTimePath,self.OrderArrivalTime)
        self.OrderCount += 1       
        return  (self.OrderIssued,self.OrderArrivalTime)
           


    def Update(self,OMSinput):
        # update recording
        # self.ZIOrderBook.append(self.OrderIssued)     
        
        self.AskBookHistory.append(list(OMSinput.ask_book))
        self.BidBookHistory.append(list(OMSinput.bid_book))
        
        AskPriceAppend = OMSinput.ask
        BidPriceAppend = OMSinput.bid
        
        if (AskPriceAppend == OMSinput.MAX_PRICE):
            AskP2Append = self.AskPricePath[-1]
        else:
            AskP2Append =  AskPriceAppend   
        if (BidPriceAppend == OMSinput.MIN_PRICE):
            BidP2Append = self.BidPricePath[-1]
        else:
            BidP2Append = BidPriceAppend
        
        self.AskPricePath = np.append(self.AskPricePath,AskP2Append)
        self.BidPricePath = np.append(self.BidPricePath,BidP2Append)
        
        # self.CurrentTime += self.OrderArrivalTime
        # self.OrderCount += 1        
 


    def ConsoleOrderBookPrint(self,Book,Booktype):
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
                # print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1])
                print(f"{Booktype} {j+1}  {Book[j][0]}  {Book[j][1]}")
        elif (Booktype.lower() == "bid") :
           for j in range(n):
                # print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1])
                print(f"{Booktype} {j+1}  {Book[j][0]}  {Book[j][1]}")
        else:
            print("Booktype should be 'ask' or 'bid'! ")



    def FileOrderBookPrint(self,Book,Booktype,OUTPUTTXT):
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
                # print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1], file=OUTPUTTXT)
                print(f"{Booktype} {j+1}  {Book[j][0]}  {Book[j][1]}", file=OUTPUTTXT)
        elif (Booktype.lower() == "bid") :
            for j in range(n):
                # print(Booktype,j+1," ",Book[j][0],"  ",Book[j][1], file=OUTPUTTXT)
                print(f"{Booktype} {j+1}  {Book[j][0]}  {Book[j][1]}", file=OUTPUTTXT)
        else:
            print("Booktype should be 'ask' or 'bid'! ",file=OUTPUTTXT)
    


    def ConsolePrint(self,OMSinput):
        print("No. of the order:", self.OrderCount)   
        print("the new order is:", self.OrderIssued)
        print("arrival time interval:", self.OrderArrivalTime )
        print("the cumulated time: ", self.CurrentTime)
        # print("the cumulated time: ", self.CurrentTime + self.OrderArrivalTime)
            
        self.ConsoleOrderBookPrint(OMSinput.ask_book,"ask")
        self.ConsoleOrderBookPrint(OMSinput.bid_book,"bid")
        print("askPrice:",OMSinput.ask)   
        print("bidPrice:",OMSinput.bid)    
        print("\n")



    def FilePrint(self,OMSinput,OUTPUTTXT):
        print("No. of the order:", self.OrderCount,file=OUTPUTTXT)   
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
            SpreadN = int(round((AskPriceTemp - BidPriceTemp)/self.TICK_SIZE) - 1 )
        
        for j in range(1,SpreadN+1):
            SpreadPriceList.append(BidPriceTemp + self.TICK_SIZE * j )
        
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
        # plt.title('After %d th order'%k)
        plt.title(f"After {k}th order")
        ax.legend()
        plt.show()
    
    
    
    def unique_index(self,L,f):
    # find all the indexs of f appeared in L
        return [i for (i,v) in enumerate(L) if v==f]    



    def PirceOrderPlot(self):
        plt.plot(self.AskPricePath,color ='green',lw=1) 
        plt.plot(self.BidPricePath,color ='red',lw=1)         
        plt.ylabel('Price')
        plt.xlabel('Order Sequence')
        plt.show()



    def PirceTimePlot(self):
        plt.plot(self.CurrentTimePath,self.AskPricePath,color ='green',lw=1)
        plt.plot(self.CurrentTimePath,self.BidPricePath,color ='red',lw=1)
        plt.ylabel('Price')
        plt.xlabel('Time')
        plt.show() 


    def ArrivalTimeFrequencyPlot(self):
        print("Average arrival time: ",np.mean(self.ArrivalTimePath))
        plt.hist(self.ArrivalTimePath, bins = 20, range = (0,self.ArrivalTimePath.max()) )
        plt.title("The frequency distribution of ArricalTime:")
        plt.show()
    
    
    
    
    
    