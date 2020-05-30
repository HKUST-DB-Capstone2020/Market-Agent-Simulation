# -*- coding: utf-8 -*-
"""
Created on Tue May 19 21:14:25 2020

@author: jackz
"""

import os
import sys
# import random
# import math
# import time
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
sys.path.append(os.path.pardir)
# os.chdir("C:\\Users\\jackz\\Desktop\\0519 draft")
# from LOB.LOB import LimitOrderBook
from OMS.OMS import OrderManagementSystem 
from ZIAgent.ZIAgent import ZIAgent

import cProfile


if __name__ == "__main__":  
    # initial settings
    MAX_PRICE_LEVELS = 200  # total number of price grids
    TICK_SIZE = 0.1  # usually 1 or 0.1 or 0.01
    TimeHorizon = 600
    qtysize = 100
    
    PRICE_START =   9.7   
    PRICE_A_START =  10.0  
    PRICE_B_START =  9.8   
        
    # parameters according to Cont paper
    MU_Est = 0.94
    LAMBDA_Est = [1.85,1.51,1.09,0.88,0.77]
    THETA_Est = [0.71,0.81,0.68,0.56,0.47]
    """
    K_Est = 1.92
    ALPHA_Est = 0.52
    LAMBDA_PowerLaw = [K_Est/(pow(j,ALPHA_Est)) for j in range(1,6)] # Arrival rates according to power law 
    """
    
    # set initial values for OMS and ZIAgent
    CurrentTime = 0
    OrderCount = 0
    ZIOrderBook = [[]]    

    OMSTest = OrderManagementSystem(PRICE_A_START,PRICE_B_START,TICK_SIZE,5,PRICE_START)

    ZIAgentTest = ZIAgent(NAME                =   "ZIagent", 
                          OMSinput            =   OMSTest, 
                          MAX_PRICE_LEVELS    =   MAX_PRICE_LEVELS, 
                          TICK_SIZE           =   TICK_SIZE, 
                          QTYSIZE             =   qtysize, 
                          MU                  =   MU_Est, 
                          LAMBDA              =   LAMBDA_Est, 
                          THETA               =   THETA_Est, 
                          CurrentTime         =   CurrentTime, 
                          OrderCount          =   OrderCount, 
                          ZIOrderBook         =   ZIOrderBook)


    # ZIAgentTest.Execute(OMSTest)
    
    
    # cProfile
    def cProfileAnalysis(OMSinput,ZIAgentinput,TimeHorizoninput):
        while (ZIAgentinput.CurrentTime <= TimeHorizoninput):
            ZIAgentinput.Execute(OMSinput)                                       # execute ZIAgent generator
            OMSinput.receive(ZIAgentinput.OrderIssued)                           # output to OMS
            ZIAgentinput.Update(OMSinput)      
            if (ZIAgentinput.OrderCount % 1000 == 0 ):
                print(ZIAgentinput.OrderCount, end=" ")   

    # cProfile.run("cProfileAnalysis(OMSTest,ZIAgentTest,TimeHorizon)", sort="cumulative")
    cProfile.run("cProfileAnalysis(OMSTest,ZIAgentTest,TimeHorizon)", sort="tottime")



















