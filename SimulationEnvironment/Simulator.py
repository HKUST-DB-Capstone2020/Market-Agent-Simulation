'''
Authors: SHEN, Kanchao
         WANG, Boyu
'''

import os
import sys
import time
import numpy as np
import pandas as pd
sys.path.append(os.path.pardir)


from OMS.OMS import OrderManagementSystem
from ZIAgent.ZIAgent import ZIAgent
from myStrategies import *

class State:
    
    def __init__(self, ask, bid, ask_book, bid_book, 
                 trade_price_record, trade_vol_record, 
                 current_time, lastTime, time_horizon):
        
        self.ask                = ask
        self.bid                = bid
        self.ask_book           = ask_book
        self.bid_book           = bid_book
        self.trade_price_record = trade_price_record
        self.trade_vol_record   = trade_vol_record
        self.current_time       = current_time
        self.lastTime           = lastTime
        self.time_horizon       = time_horizon


class Simulator:
    
    def __init__(self):
        
        self.MAX_PRICE_LEVELS = 200  # total number of price grids
        self.TICK_SIZE        = 0.1  # usually 1 or 0.1 or 0.01
        self.TimeHorizon      = 330  # 330min=1day (HKEX: 9:30am-12pm, 13pm-16pm)
        self.qtysize          = 1000

        self.PRICE_START      = 9.7
        self.PRICE_A_START    = 10.0
        self.PRICE_B_START    = 9.8
        self.orderLevel       = 5
        self.ref_price        = (self.PRICE_A_START + self.PRICE_B_START)/2

        # parameters according to Cont paper
        self.Mu_Est           = 0.94
        self.Lambda_Est       = [1.85, 1.51, 1.09, 0.88, 0.77]
        self.Theta_Est        = [0.71, 0.81, 0.68, 0.56, 0.47]
        """
        self.k_Est            = 1.92
        self.Alpha_Est        = 0.52
        self.Lambda_PowerLaw  = [self.k_Est / (pow(j, self.Alpha_Est)) for j in range(1, 6)]  # Arrival rates according to power law
        """
        # set initial values for OMS and ZIAgent
        self.lastTime         = 0
        self.CurrentTime      = 0
        self.OrderCount       = 0
        self.ZIOrderBook      = [[]]

        self.OMSTest = OrderManagementSystem(ask        = self.PRICE_A_START, 
                                             bid        = self.PRICE_B_START, 
                                             tick       = self.TICK_SIZE, 
                                             orderLevel = self.orderLevel, 
                                             lastPrice  = self.PRICE_START,
                                             init_qty   = self.qtysize)
        
        self.ZIAgent = ZIAgent(NAME             = "ZIagent", 
                               OMSinput         = self.OMSTest, 
                               MAX_PRICE_LEVELS = self.MAX_PRICE_LEVELS, 
                               TICK_SIZE        = self.TICK_SIZE, 
                               MU               = self.Mu_Est, 
                               LAMBDA           = self.Lambda_Est, 
                               THETA            = self.Theta_Est, 
                               CurrentTime      = self.CurrentTime, 
                               OrderCount       = self.OrderCount, 
                               ZIOrderBook      = self.ZIOrderBook)
        
        self.state   = State(ask                = self.OMSTest.ask, 
                             bid                = self.OMSTest.bid, 
                             ask_book           = self.OMSTest.ask_book, 
                             bid_book           = self.OMSTest.bid_book,
                             trade_price_record = self.OMSTest.trade_price_record, 
                             trade_vol_record   = self.OMSTest.trade_vol_record, 
                             current_time       = self.ZIAgent.CurrentTime,
                             lastTime           = self.lastTime,
                             time_horizon       = self.TimeHorizon)
        
        self.exec_price  = []
        self.exec_qty    = []

    def reset(self):
        self.__init__()
        return self.state   
    
    def step(self, action):
        
        if action: # action is not empty list
            len_before = len(self.state.trade_price_record)
            self.OMSTest.receive(action)
            len_after = len(self.state.trade_price_record)
            
            self.exec_price += self.state.trade_price_record[len_before-len_after:] 
            self.exec_qty   += self.state.trade_vol_record[len_before-len_after:] 
        
        self.state.lastTime = self.state.current_time
        self.ZIAgent.Execute(self.OMSTest)              # execute ZIAgent generator
        self.OMSTest.receive(self.ZIAgent.OrderIssued)  # output to OMS
        self.ZIAgent.Update(self.OMSTest)               # update ZIAgent
        self.update_state()
    
        return self.state

    def update_state(self):
        
        self.state.ask                = self.OMSTest.ask
        self.state.bid                = self.OMSTest.bid
        self.state.ask_book           = self.OMSTest.ask_book
        self.state.bid_book           = self.OMSTest.bid_book
        self.state.trade_price_record = self.OMSTest.trade_price_record
        self.state.trade_vol_record   = self.OMSTest.trade_vol_record
        self.state.current_time       = self.ZIAgent.CurrentTime
        self.time_horizon             = self.TimeHorizon

    def slippage(self):
        
        strat_revenue = np.dot(np.array(self.exec_price), np.array(self.exec_qty))
        ref_revenue   = np.sum( self.ref_price * np.array(self.exec_qty) )
        return strat_revenue - ref_revenue, ref_revenue, strat_revenue



if __name__ == '__main__':
    
    ## init simulator
    env  = Simulator()
    
    # which strategy to use
    strat = "myStrategy_demo1"
    if strat == "myStrategy_demo1":
        algo = myStrategy_demo1(para1 = 0.5,  # for demenstration purpose
                                para2 = 0.1)  # for demenstration purpose
    
    episodes      = 1
    shortfall     = episodes * [0.0]
    ref_revenue   = episodes * [0.0]
    strat_revenue = episodes * [0.0]
    
    for episode in range(episodes):        
        # time for running program
        RunningStartTime=time.perf_counter()
        
        # reset state and algos
        state = env.reset()
        algo.reset()
        done = False
        qty_count = 0
    
        while (state.current_time < state.time_horizon) and not done:
            # run the algorithm for one episode
            algo_action, done = algo.action(state)                
            if algo_action:
                qty_count += algo_action[-2]
                print(round(state.current_time,3), algo_action)
            
            # state, reward, done, info = env.step(action)
            state = env.step(algo_action)
        
        # env.ZIAgent.ZIAgentPirceOrderPlot()
        env.ZIAgent.PirceTimePlot()
        
        RunningTime = round(time.perf_counter()-RunningStartTime,3)
        print(f"the running cost: {RunningTime} seconds")
        print("Total shares executed: ", qty_count)
        
        shortfall[episode], ref_revenue[episode], strat_revenue[episode] = env.slippage()
    
    result = pd.DataFrame()
    result['shortfall'] = shortfall
    result['ref_revenue'] = ref_revenue
    result['strat_revenue'] = strat_revenue

