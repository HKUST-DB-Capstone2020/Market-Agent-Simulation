# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 22:20:49 2020

@author: jackz
"""

"""

Method 2, 
generate the next order at each price level, pick up the first-come one,
send it to OMS

"""


import os
import random
import math
import time
import numpy as np
import matplotlib.pyplot as plt

os.chdir("C:\\Users\\jackz\\Desktop\\0410 draft")


# parameters according to Cont paper
Mu_Est = 0.94
k_Est = 1.92
Alpha_Est = 0.52
Lambda_Est = [1.85,1.51,1.09,0.88,0.77]
Theta_Est = [0.71,0.81,0.68,0.56,0.47]

# Arrival rates according to power law 
Lambda_PowerLaw = [k_Est/(pow(j,Alpha_Est)) for j in range(1,6)]



# test for system
n = 200  # total number of price grids
PriceGridSize = 0.1  # usually 1 or 0.1 or 0.01
TimeHorizon = 600
deltaT = 0.5
qtysize = 1000

PriceDecimals = math.ceil(math.log10(1/PriceGridSize))
# Tn = int(TimeHorizon / deltaT)  # total number of time grids

def OneShotBirthDeath(x,b,d,deltaT):  
# b = birth rate, d = death rate, x = current state
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

"""
# test for OneShotBirthDeath(x,b,d,deltaT)

RoundsTest = 100000
BirthCountTest = 0
DeathCountTest = 0
NoOccurCount = 0
TimeIntervalRec = []
TimeIntervalTest = 1
InitialTest = 5
BirthRateTest = 1.85
DeathRateTest = 0.71

for j in range(RoundsTest):
    BDTemp = OneShotBirthDeath(InitialTest,BirthRateTest,DeathRateTest,TimeIntervalTest)
    if BDTemp[0] == 1 :
        BirthCountTest += 1
    elif BDTemp[0] == -1 :
        DeathCountTest += 1
    else:
        NoOccurCount += 1
    TimeIntervalRec.append(BDTemp[1])



print("Theoretical NoOccur%", math.exp(-(BirthRateTest+DeathRateTest)))
print("Test NoOccur%: ",NoOccurCount/RoundsTest)

print("Test Birth%: ",BirthCountTest/RoundsTest)
print("Test Death%: ",DeathCountTest/RoundsTest)

print("Theoretical Birth%: ", BirthRateTest/DeathRateTest)
print("Test Birth% / Death%: ",BirthCountTest/DeathCountTest)

print("Average arrival time: ",np.mean(TimeIntervalRec))
"""


def OneShotBuyOrderUpdate(y,p,pA,deltaT,Mu,Lambda,Theta):
    if p>pA:
        return [0,deltaT]
    elif p==pA:
        return OneShotBirthDeath(y,Mu,0,deltaT)
    else:
        return OneShotBirthDeath(y,Lambda,Theta*y,deltaT)


def OneShotSellOrderUpdate(z,p,pB,deltaT,Mu,Lambda,Theta):
    if p<pB:
        return [0,deltaT]
    elif p==pB:
        return OneShotBirthDeath(z,Mu,0,deltaT)
    else:
        return OneShotBirthDeath(z,Lambda,Theta*z,deltaT)



def OneShotZIOrderIssue(Order,pA,pB,direction,qty):
# Order = [price, order change +1 or -1 or 0, arrival time]
# direction = "buy" or "sell"

    p = Order[0]
    ordertype = ""
    
    if (Order[1] == -1):
        ordertype = "cancel"
    else:
        if (( direction == "buy" and p<pA ) or ( direction == "sell" and p>pB )) :
            ordertype = "limit"
        if (( direction == "buy" and p==pA ) or ( direction == "sell" and p==pB )) :
            ordertype = "market"

    output = ["ZIagent", ordertype, direction, qty, round(p*PriceGridSize,PriceDecimals)]
    
    return output



# get birth rate and death rate of different price levels from Lambda_Est Theta_Est
# 0 if out of the distance, in Cont paper, the valid distance is 5
def GetParameter(Parameter_Est,distance,Parameter):
    n = len(Parameter_Est)
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
    

# find the first arrive order 
def FirstOrderSearch(BookRec):
    BookRecTime = [j[1] for j in BookRec]
    FirstOrderPrice = BookRecTime.index(min(BookRecTime))
    FirstOrderTime = BookRecTime[FirstOrderPrice]
    FirstOrderCount =  BookRec[FirstOrderPrice][0]
    outcome = [FirstOrderPrice,FirstOrderCount,FirstOrderTime]
    return outcome



def OrderBookPrint(Book,Booktype):
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

def unique_index(L,f):
    return [i for (i,v) in enumerate(L) if v==f]





def FileOrderBookPrint(Book,Booktype,txt):
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


# open the txt ready for output

OutputTxt = open("Output.txt","w")

# setting initial values of variables

price =   9.9   # initial for example
priceA =  10.0   # initial for example
priceB =  9.8   # initial for example

CurrentTime = 0
OrderCount = 1
ZIOrderBook = [[]]
ArrivalTime = [0]


starttime=time.perf_counter()



## set OMS from OMS&LOB part
OMStest = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
AskPricePath = [OMStest.LOB.askBook.ask]
BidPricePath = [OMStest.LOB.bidBook.bid]
AskPricePath_2 = [OMStest.LOB.askBook.ask]
BidPricePath_2 = [OMStest.LOB.bidBook.bid]
AskBookHistory = [list(OMStest.LOB.askBook.askBook_public)]
BidBookHistory = [list(OMStest.LOB.bidBook.bidBook_public)]

# during the trading period

while (CurrentTime <= TimeHorizon):
    # input from OMS
        
    # price = OMSupdate(price) / PriceGridSize , eg. 99 instead of 9.9
    """
    priceA = round( OMStest.LOB.askBook.ask / PriceGridSize )
    priceB = round( OMStest.LOB.bidBook.bid / PriceGridSize )
    """
    if (OMStest.LOB.askBook.ask == 4560987):
        priceA = round( AskPricePath_2[-1] / PriceGridSize )
    else:
        priceA = round( OMStest.LOB.askBook.ask / PriceGridSize )
    if (OMStest.LOB.bidBook.bid == 0):
        priceB = round( BidPricePath_2[-1] / PriceGridSize )
    else:
        priceB = round( OMStest.LOB.bidBook.bid / PriceGridSize )   
    
    YBookTemp = [0 for _ in range(n+1)]
    for j in OMStest.LOB.bidBook.bidBook_public:
        YBookTemp[round(j[0]/PriceGridSize)] = j[1] // qtysize

    
    ZBookTemp = [0 for _ in range(n+1)]
    for j in OMStest.LOB.askBook.askBook_public:
        ZBookTemp[round(j[0]/PriceGridSize)] = j[1] // qtysize

    """
   
    # for draft, no OMS     
    price =   int( 9.9 / PriceGridSize )   
    priceA =  int( 10.0 / PriceGridSize ) 
    priceB =  int( 9.8 / PriceGridSize ) 
    
    """
    
    # ZIagent generate
    """
    # for draft, no OMS  
    XBook[k-1] = [ZBook[k-1][j] - YBook[k-1][j] for j in range(n+1)]  
    YBookTemp = YBook[k-1]
    ZBookTemp = ZBook[k-1]    
    """
    
    YBookRec = [ [0,0] for _ in range(n+1)]
    ZBookRec = [ [0,0] for _ in range(n+1)]
    
    YBookRec = [OneShotBuyOrderUpdate(YBookTemp[j],j,priceA,deltaT,\
          Mu_Est,GetParameter(Lambda_Est,priceA-j,"lambda"),GetParameter(Theta_Est,priceA-j,"theta")) \
    for j in range(n+1) ]   
        
    ZBookRec = [OneShotSellOrderUpdate(ZBookTemp[j],j,priceB,deltaT,\
          Mu_Est,GetParameter(Lambda_Est,j-priceB,"lambda"),GetParameter(Theta_Est,j-priceB,"theta")) \
    for j in range(n+1) ]
            
    # find the first arrive order 
    YOrderFirst = FirstOrderSearch(YBookRec)
    ZOrderFirst = FirstOrderSearch(ZBookRec)
        
    if (YOrderFirst[2] < ZOrderFirst[2]):  
        OrderIssued = OneShotZIOrderIssue(YOrderFirst,priceA,priceB,"buy",qtysize)
        OrderArrivalTime = YOrderFirst[2]
    elif (YOrderFirst[2] > ZOrderFirst[2]):
        OrderIssued = OneShotZIOrderIssue(ZOrderFirst,priceA,priceB,"sell",qtysize)
        OrderArrivalTime = ZOrderFirst[2]
    else:
        tempU = random.random()
        if tempU < 0.5:
            OrderIssued = OneShotZIOrderIssue(YOrderFirst,priceA,priceB,"buy",qtysize)
            OrderArrivalTime = YOrderFirst[2]
        else:
            OrderIssued = OneShotZIOrderIssue(ZOrderFirst,priceA,priceB,"sell",qtysize)
            OrderArrivalTime = ZOrderFirst[2]
         
    # output to OMS
    OMStest.receive(OrderIssued)
        
    ZIOrderBook.append(OrderIssued)
    ArrivalTime.append(OrderArrivalTime)

    """
    # full output of order book
    print("at kth order:",OrderCount)   
    print("the new order is:",OrderIssued)
    print("arrival time interval:",OrderArrivalTime )
    print("the cumulated time: ",CurrentTime+OrderArrivalTime)
        
    OrderBookPrint(OMStest.LOB.askBook.askBook_public,"ask")
    OrderBookPrint(OMStest.LOB.bidBook.bidBook_public,"bid")
    print("askPrice:",OMStest.LOB.askBook.ask)   
    print("bidPrice:",OMStest.LOB.bidBook.bid)    
    print("\n")
    """
    # full output of order book to txt file

    print("at kth order:",OrderCount,file=OutputTxt)   
    print("the new order is:",OrderIssued,file=OutputTxt)
    print("arrival time interval:",OrderArrivalTime,file=OutputTxt )
    print("the cumulated time: ",CurrentTime+OrderArrivalTime,file=OutputTxt)
    
    FileOrderBookPrint(OMStest.LOB.askBook.askBook_public,"ask",OutputTxt)
    FileOrderBookPrint(OMStest.LOB.bidBook.bidBook_public,"bid",OutputTxt)
    print("askPrice:",OMStest.LOB.askBook.ask,file=OutputTxt)   
    print("bidPrice:",OMStest.LOB.bidBook.bid,file=OutputTxt)    
    print("\n",file=OutputTxt)
    
    AskPricePath.append(OMStest.LOB.askBook.ask)
    BidPricePath.append(OMStest.LOB.bidBook.bid)
    if (OMStest.LOB.askBook.ask == 4560987):
        AskPricePath_2.append(AskPricePath_2[-1])
    else:
        AskPricePath_2.append(OMStest.LOB.askBook.ask)    
    if (OMStest.LOB.bidBook.bid == 0):
        BidPricePath_2.append(BidPricePath_2[-1])
    else:
        BidPricePath_2.append(OMStest.LOB.bidBook.bid)
    
    AskBookHistory.append(list(OMStest.LOB.askBook.askBook_public))
    BidBookHistory.append(list(OMStest.LOB.bidBook.bidBook_public))
    

    if (OrderCount % 500 == 0 ):
        print(OrderCount, end=" ")

    
    
    CurrentTime += OrderArrivalTime
    OrderCount += 1





endtime=time.perf_counter()
PlotXaxis = list(range(len(AskPricePath))) 
plt.plot(PlotXaxis,AskPricePath_2,color ='green',lw=1) 
plt.plot(PlotXaxis,BidPricePath_2,color ='red',lw=1) 
plt.show()

print('4560987 in ask prices',unique_index(AskPricePath,4560987))
print('0 in bid prices',unique_index(BidPricePath,0))

OutputTxt.close()

# show ArrivalTime
print("Average arrival time: ",np.mean(ArrivalTime))

print("the running cost:",endtime-starttime, " seconds")


"""
### print history

# BidPricePath.index(9.7)
HistoryCheck = 1593

print("before the %d th order"%HistoryCheck)
OrderBookPrint(AskBookHistory[HistoryCheck-1],"ask")
OrderBookPrint(BidBookHistory[HistoryCheck-1],"bid")
print("askPrice:",AskPricePath[HistoryCheck-1])   
print("bidPrice:",BidPricePath[HistoryCheck-1]) 

print("at %d th order:"%HistoryCheck)   
print("the new order is: ",OrderIssued)
print("arrival time interval:",OrderArrivalTime )
print("the cumulated time: ",ArrivalTime[HistoryCheck])
        
OrderBookPrint(AskBookHistory[HistoryCheck],"ask")
OrderBookPrint(BidBookHistory[HistoryCheck],"bid")
print("askPrice:",AskPricePath[HistoryCheck])   
print("bidPrice:",BidPricePath[HistoryCheck]) 
print("\n")
"""



