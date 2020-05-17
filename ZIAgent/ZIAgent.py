
import os
import sys
import random
import math
# import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.append(os.path.pardir)
from LOB.LOB import LimitOrderBook
from OMS.OMS import OrderManagementSystem 




class ZIAgent(object):
    def __init__(self,NAME,OMSinput,MAX_PRICE_LEVELS,TICK_SIZE,MU,LAMBDA,THETA,\
                 CurrentTime,OrderCount,ZIOrderBook,QTYSIZE=1000):
        self.NAME = NAME
        self.OMSinput = OMSinput
        self.MAX_PRICE_LEVELS = MAX_PRICE_LEVELS
        self.TICK_SIZE = TICK_SIZE
        self.MU = MU
        self.LAMBDA = LAMBDA
        self.THETA = THETA
        self.qtysize = QTYSIZE
        self.PriceDecimals = math.ceil(math.log10(1/TICK_SIZE))
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
        self.OrderArrivalTime = 0
        self.OrderIssued = []
        

    
    
    
    def GetLimitOrderRate(self,Parameter_Est,distance):
        n = len(Parameter_Est)
        distance = int(round(distance,0))
        if (distance <= n and distance > 0 ):
            return Parameter_Est[distance - 1]
        else:
            return 0
    
    
    
    def GetCancellationRate(self,Parameter_Est,distance):
        n = len(Parameter_Est)
        distance = int(round(distance,0)) 
        if (distance <= n and distance > 0 ):
            return Parameter_Est[distance - 1]
        elif (distance > n):
            return Parameter_Est[n - 1]
        else:
            return 0
    
       

    def random_index(self,rate):
        # allocate randomly according to the probabilities in the list
        start = 0
        index = 0
        randnum = random.random() * sum(rate)
        for index, scope in enumerate(rate):
            start += scope
            if randnum <= start:
                break
        return index



    def PDtoList(self,df):
        # convert dataframe to a list, by column
        list_df = []
        for j in range(df.shape[1]):
            list_df.extend(df[j].tolist())
        return list_df



    def ListSumUp(self,L):
        return [sum(L[0:(j+1)]) for j in range(len(L))]
    
    
    
    def BidBirthRate(self,p,BidBook):
        output=0
        if p>self.priceA:
            output = 0
        elif p == self.priceA:
            output = self.MU
        else:
            output = self.GetLimitOrderRate(self.LAMBDA, self.priceA-p)
        return output

    
    def BidDeathRate(self,p,BidBook):
        output=0
        if p>self.priceA:
            output = 0
        elif p == self.priceA:
            output = 0
        else:
            output = self.GetCancellationRate(self.THETA, self.priceA-p) * BidBook[p]
        return output
    
    
    
    def AskBirthRate(self,p,AskBook):
        output=0
        if p<self.priceB:
            output = 0
        elif p == self.priceB:
            output = self.MU
        else:
            output = self.GetLimitOrderRate(self.LAMBDA, p-self.priceB)
        return output


    
    def AskDeathRate(self,p,AskBook):
        output=0
        if p<self.priceB:
            output = 0
        elif p == self.priceB:
            output = 0
        else:
            output = self.GetCancellationRate(self.THETA, p-self.priceB) * AskBook[p]
        return output


    
    def Execute(self,OMSinput):
        # if (OMSinput.ask == 4560987):
        if (OMSinput.ask == OMSinput.MAX_PRICE):
            self.priceA = round( self.PricePathDF.AskP_2[len(self.PricePathDF)-1] / self.TICK_SIZE )
        else:
            self.priceA = round( OMSinput.ask / self.TICK_SIZE )
        
        # if (OMSinput.bid == 0):
        if (OMSinput.bid  == OMSinput.MIN_PRICE):
            self.priceB = round( self.PricePathDF.BidP_2[len(self.PricePathDF)-1] / self.TICK_SIZE )
        else:
            self.priceB = round( OMSinput.bid / self.TICK_SIZE )    
        
        
        
        BidBookList = [0 for _ in range(self.MAX_PRICE_LEVELS +1)]
        for j in OMSinput.bid_book:
            BidBookList[int(round(j.price/self.TICK_SIZE))] = j.qty // self.qtysize
        
        AskBookList = [0 for _ in range(self.MAX_PRICE_LEVELS +1)]
        for j in OMSinput.ask_book:
            AskBookList[int(round(j.price/self.TICK_SIZE))] = j.qty // self.qtysize

        BidBirthRateList = [self.BidBirthRate(j,BidBookList) for j in range(self.MAX_PRICE_LEVELS +1)]
        BidDeathRateList = [self.BidDeathRate(j,BidBookList) for j in range(self.MAX_PRICE_LEVELS +1)]
        AskBirthRateList = [self.AskBirthRate(j,AskBookList) for j in range(self.MAX_PRICE_LEVELS +1)]
        AskDeathRateList = [self.AskDeathRate(j,AskBookList) for j in range(self.MAX_PRICE_LEVELS +1)]
        
        
        RateDF = pd.DataFrame({0:BidBirthRateList,1:BidDeathRateList,2:AskBirthRateList,3:AskDeathRateList})
        RateList = self.PDtoList(RateDF)
        
        """
        Index = self.random_index(RateList)
        """
        
        SumRateList = sum(RateList)
        # RateList_2 = [j/SumRateList for j in RateList] 
        RateList_2 = list(map(lambda x: x/SumRateList , RateList))  
        Index = int(np.random.choice(range(4*(self.MAX_PRICE_LEVELS+1)), 1, p=RateList_2))
        
        
        Row = Index % (self.MAX_PRICE_LEVELS +1)
        Col = Index // (self.MAX_PRICE_LEVELS +1)

        orderprice = Row

        if Col == 0:
            orderdirection = "buy"
            if orderprice == self.priceA:
                ordertype = "market"
            else:
                ordertype = "limit"
        elif Col == 1:
            orderdirection = "buy"
            ordertype = "cancel"
        elif Col == 2:
            orderdirection = "sell"
            if orderprice == self.priceB:
                ordertype = "market"
            else:
                ordertype = "limit"
        else:
            orderdirection = "sell"
            ordertype = "cancel"
        
        self.OrderIssued = ["ZIagent", ordertype, orderdirection, self.qtysize, \
                       round(orderprice*self.TICK_SIZE,self.PriceDecimals)] 
    
        
        self.OrderArrivalTime = random.expovariate(sum(RateDF.sum()))
        
        self.ZIOrderBook.append(self.OrderIssued) 
        self.CurrentTime += self.OrderArrivalTime
        self.OrderCount += 1   
        
        return  (self.OrderIssued,self.OrderArrivalTime)
    
    
    
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
    


    def Update(self,OMSinput):
        # update recording
        # self.ZIOrderBook.append(self.OrderIssued)     
        self.AskBookHistory.append(list(OMSinput.ask_book))
        self.BidBookHistory.append(list(OMSinput.bid_book))
        self.PricePathDF = self.PricePathDF.append(self.PricePathUpdate(OMSinput),ignore_index=True)   
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
        plt.plot(self.PricePathDF.AskP_2,color ='green',lw=1) 
        plt.plot(self.PricePathDF.BidP_2,color ='red',lw=1) 
        # plt.plot(PricePathDF.MarketPrice,color ='yellow',lw=1) 
        plt.ylabel('Price')
        plt.xlabel('Order Sequence')
        plt.show()



    def PirceTimePlot(self):
        plt.plot(self.PricePathDF.CumulatedTime,self.PricePathDF.AskP_2,color ='green',lw=1)
        plt.plot(self.PricePathDF.CumulatedTime,self.PricePathDF.BidP_2,color ='red',lw=1)
        # plt.plot(PricePathDF.CumulatedTime,PricePathDF.MarketPrice,color ='yellow',lw=1)
        plt.ylabel('Price')
        plt.xlabel('Time')
        plt.show() 



    def ArrivalTimeFrequencyPlot(self):
        print("Average arrival time: ",np.mean(self.PricePathDF.ArrivalTime))
        plt.hist(self.PricePathDF.ArrivalTime, bins = 20, range = (0,self.PricePathDF.ArrivalTime.max()) )
        plt.title("The frequency distribution of ArricalTime:")
        plt.show()
