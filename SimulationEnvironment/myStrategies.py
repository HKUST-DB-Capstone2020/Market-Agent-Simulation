#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 14 17:20:38 2020

@author: boyuwang
"""

DAILY_VOLUME = 559500               # ADTV
TOTAL_SIZE   = DAILY_VOLUME * 0.05  # shares to execute
EXEC_PERIOD  = 10                   # liquidation period

DIRECTION    = "sell"
ORDER_ID     = "strategy"

class myStrategy_demo1:
    
    def __init__(self, para1, para2):
        
        '''strategy params'''
        self.para1 = para1
        self.para2 = para2
        self.done  = False
        
    def reset(self):
        self.__init__(self.para1, self.para2)
    
    def action(self, state):
        
        ## for demenstration purpose
        
        if not self.done:
            strategy_order = [ORDER_ID, "market", DIRECTION, TOTAL_SIZE/EXEC_PERIOD, 0]
        else:
            strategy_order = []
        
        return strategy_order, self.done

                        
                        
                      
                        
                        
                        
                        