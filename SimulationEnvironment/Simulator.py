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
from Strategies import *

class State:
    
    def __init__(self, ask, bid, ask_book, bid_book, 
                 trade_price_record, trade_vol_record, 
                 strategy_record, execPrc, execQty,
                 current_time, lastTime, time_horizon):
        
        self.ask                = ask
        self.bid                = bid
        self.ask_book           = ask_book
        self.bid_book           = bid_book
        self.trade_price_record = trade_price_record
        self.trade_vol_record   = trade_vol_record
        self.strategy_record    = strategy_record
        self.execPrc            = execPrc
        self.execQty            = execQty
        self.current_time       = current_time
        self.lastTime           = lastTime
        self.time_horizon       = time_horizon


class Simulator:
    
    def __init__(self, strat_name=None, trans_record=False):
        
        self.MAX_PRICE_LEVELS = 200  # total number of price grids
        self.TICK_SIZE        = 0.1  # usually 1 or 0.1 or 0.01
        self.TimeHorizon      = 100  # 330min=1day (HKEX: 9:30am-12pm, 13pm-16pm)
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
        
        if trans_record: self.OMSTest.record(strat_name)
        
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
                             strategy_record    = self.OMSTest.strategy_record, 
                             execPrc            = self.OMSTest.execPrice,
                             execQty            = self.OMSTest.execQty,
                             current_time       = self.ZIAgent.CurrentTime,
                             lastTime           = self.lastTime,
                             time_horizon       = self.TimeHorizon)

    def reset(self, strat_name, trans_record):
        self.__init__(strat_name, trans_record)
        return self.state   
    
    def step(self, action):
        
        for act in action:  # multiple actions
            if act:  # this action is not empty list
                self.OMSTest.receive(act)
        
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
        self.state.strategy_record    = self.OMSTest.strategy_record
        self.state.execPrc            = self.OMSTest.execPrice
        self.state.execQty            = self.OMSTest.execQty
        self.state.current_time       = self.ZIAgent.CurrentTime
        self.time_horizon             = self.TimeHorizon

    def slippage(self):
        
        strat_revenue = 0
        ref_revenue   = 0
        for filled_order in self.OMSTest.strategy_record.filled_order:
            strat_revenue += filled_order[1]*filled_order[2]  #1:price, 2: qty
            ref_revenue += self.ref_price*filled_order[2]
        shortfall = ref_revenue - strat_revenue if DIRECTION == 'sell' else strat_revenue - ref_revenue
        return shortfall, ref_revenue, strat_revenue



if __name__ == '__main__':
    
    ## which strategy to use
    strat = "strategy"
    ## init simulator
    env  = Simulator(strat_name=strat, trans_record=True)
    
    if strat == "strategy":
        algo = myStrategy_demo1(para1 = 0.5,  # for demenstration purpose
                                para2 = 0.1)  # for demenstration purpose
    
    episodes      = 10_000
    # episodes      = 100
    shortfall     = episodes * [0.0]
    ref_revenue   = episodes * [0.0]
    strat_revenue = episodes * [0.0]
    
    # time for running program
    RunningStartTime = time.perf_counter()
    for episode in range(episodes):        
        print(episode)
        # reset state and algos
        state = env.reset(strat_name=strat, trans_record=True)
        algo.reset()
        done = False
    
        while (state.current_time < state.time_horizon) and not done:
            # run the algorithm for one episode
            algo_action, done = algo.action(state)                
            
            # state, reward, done, info = env.step(action)
            state = env.step(algo_action)
        
        # env.ZIAgent.ZIAgentPirceOrderPlot()
        # env.ZIAgent.PirceTimePlot()
        
        shortfall[episode], ref_revenue[episode], strat_revenue[episode] = env.slippage()
    
    RunningTime = round(time.perf_counter()-RunningStartTime,3)
    print(f"the running cost: {RunningTime} seconds")
    result = pd.DataFrame()
    result['shortfall'] = shortfall
    result['ref_revenue'] = ref_revenue
    result['strat_revenue'] = strat_revenue
    # print(result)

