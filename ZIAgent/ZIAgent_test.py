# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 17:26:01 2020

@author: Lenovo
"""
import numpy as np

#Approach1: Estimate parameter from generated orders
CumArTime = []
for i in range(len(ArrivalTime)):
    CumArTime.append(sum(ArrivalTime[0:i+1]))
    
    
 # Test for limit bid order   
Bidlimit = [[]]   
for i in range(1,len(ZIOrderBook)):
    if (ZIOrderBook[i][1]== 'limit' and ZIOrderBook[i][2]== 'buy'):
        distance = round((AskPricePath[i-1]-ZIOrderBook[i][4])/PriceGridSize)
        Bidlimit.append([distance, CumArTime[i]])
    else:
        Bidlimit = Bidlimit
        
BidlimitRec = [[], [], [], [], []]      
for i in range(1,len(Bidlimit)):
    j = Bidlimit[i][0]
    BidlimitRec[j-1].append(Bidlimit[i][1])

BidLambda_test = []
for i in range(len(BidlimitRec)):
    BidLambda_test.append(len(BidlimitRec[i])/BidlimitRec[i][-1])

print(BidLambda_test)

# Test for market bid order       
Bidmarket = []   
for i in range(1,len(ZIOrderBook)):
    if (ZIOrderBook[i][1]== 'market' and ZIOrderBook[i][2]== 'buy'):
        Bidmarket.append(CumArTime[i])
    else:
        Bidmarket = Bidmarket

BidMu_test = len(Bidmarket)/Bidmarket[-1]
print(BidMu_test)       

Asklimit = [[]]   
for i in range(1,len(ZIOrderBook)):
    if (ZIOrderBook[i][1]== 'limit' and ZIOrderBook[i][2]== 'sell'):
        distance = round((ZIOrderBook[i][4]-BidPricePath[i-1])/PriceGridSize)
        Asklimit.append([distance, CumArTime[i]])
    else:
        Asklimit = Asklimit

# Test for limit ask order       
AsklimitRec = [[], [], [], [], []]      
for i in range(1,len(Asklimit)):
    j = Asklimit[i][0]
    AsklimitRec[j-1].append(Asklimit[i][1])

AskLambda_test = []
for i in range(len(AsklimitRec)):
    AskLambda_test.append(len(AsklimitRec[i])/AsklimitRec[i][-1])

print(AskLambda_test)

# Test for market ask order       
Askmarket = []   
for i in range(1,len(ZIOrderBook)):
    if (ZIOrderBook[i][1]== 'market' and ZIOrderBook[i][2]== 'sell'):
        Askmarket.append(CumArTime[i])
    else:
        Askmarket = Askmarket

AskMu_test = len(Askmarket)/Askmarket[-1]
print(AskMu_test)       

# Approach 2: test the function generated order
# death rate estimate
def DeathRateEst(Est,length,Deltat,n):
    artime = []
    for i in range(n):
        artime.append(OneShotBirthDeath(length,0,length*Est,Deltat)[1])
            
    Test = [1/(length*np.mean(artime)),1/(length*np.std(artime))]
    
    return Test

Theta_test = [[]]
for j in range(len(Theta_Est)):
    Theta_test.append(DeathRateEst(Theta_Est[j],10,10,100000))
    
    
# birth rate estimate
    
def BirthRateEst(Est,length,Deltat,n):
    artime = []
    for i in range(n):
        artime.append(OneShotBirthDeath(length,Est,0,Deltat)[1])
            
    Test = [1/np.mean(artime),1/np.std(artime)]
    
    return Test

Lambda_test = [[]]
for j in range(len(Lambda_Est)):
    Lambda_test.append(BirthRateEst(Lambda_Est[j],0,10,100000))
print(Lambda_test)
    
mu_test = BirthRateEst(Mu_Est,0,10,100000)
print("mu_test", mu_test)

