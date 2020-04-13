from LOB import AskBook, BidBook, LimitOrderBook
import pytest


ask = 10.5
bid = 9.5
tick = 0.1
orderLevel = 5

LOB = LimitOrderBook(ask, bid, tick, orderLevel)

class TestClass:  
        
    '''Test: Insert orders'''
    # Insert limit buy orders
    def test_LOB_insert_at_bid1(self):  
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0][1] == 1500
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 1500]]
        
        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0][1] == 2000
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 1500], ['strategy', 500]]
        
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0][1] == 2500
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]]
  
    # LOB.bidBook.bidBook_public
    # deque([[9.5, 2500], [9.4, 1000], [9.3, 1000], [9.2, 1000], [9.1, 1000]])
        
        
    # LOB.bidBook.bidBook_private
    # deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
    #       [['ZIagent', 1000]],
    #       [['ZIagent', 1000]],
    #       [['ZIagent', 1000]],
    #       [['ZIagent', 1000]]])
    
    
    def test_LOB_insert_at_bid2(self):  
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid-1*tick )
        assert LOB.bidBook.bidBook_public[1][1] == 1500
        assert LOB.bidBook.bidBook_private[1] == [['ZIagent', 1500]]
        
        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.bid-1*tick )
        assert LOB.bidBook.bidBook_public[1][1] == 2000
        assert LOB.bidBook.bidBook_private[1] == [['ZIagent', 1500], ['strategy', 500]]
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid-1*tick )
        assert LOB.bidBook.bidBook_public[1][1] == 2500
        assert LOB.bidBook.bidBook_private[1] == [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]]
        
        # LOB.bidBook.bidBook_public
        # deque([[9.5, 2500], [9.4, 2500], [9.3, 1000], [9.2, 1000], [9.1, 1000]])
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #        [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #        [['ZIagent', 1000]],
       #        [['ZIagent', 1000]],
       #        [['ZIagent', 1000]]])
        
    
    def test_LOB_insert_new_bid1(self):  
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid+1*tick )
        assert LOB.bidBook.bidBook_public[0] == [bid+1*tick, 500]
        assert LOB.bidBook.bidBook_private[0] == [[ 'ZIagent', 500 ]]
        
        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0] == [bid+1*tick, 1000]
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 500], ['strategy', 500]]
        
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0] == [bid+1*tick, 1500]
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]]
    
    # LOB.bidBook.bidBook_public
    # deque([[9.6, 1500],
    #        [9.5, 2500],
    #        [9.4, 2500],
    #        [9.3, 1000],
    #        [9.2, 1000],
    #        [9.1, 1000]])
    
    
    # LOB.bidBook.bidBook_private
    # deque([[['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
    #        [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
    #        [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
    #        [['ZIagent', 1000]],
    #        [['ZIagent', 1000]],
    #        [['ZIagent', 1000]]])
        
        
    
    def test_LOB_insert_new_bid1_leq2tick(self):  
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid+2*tick )
        
        assert LOB.bidBook.bidBook_public[0] == [round(LOB.bidBook.bid,4), 500]
        assert LOB.bidBook.bidBook_public[1] == [round(LOB.bidBook.bid-1*tick,4), 0]
        assert LOB.bidBook.bidBook_private[0] == [[ 'ZIagent', 500 ]]
        assert LOB.bidBook.bidBook_private[1] == []
        
       # LOB.bidBook.bidBook_public
       #  deque([[9.8, 500],
       #         [9.7, 0],
       #         [9.6, 1500],
       #         [9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000]])
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 500]],
       #         [],
       #         [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
    
    def test_LOB_insert_new_empty_bid(self): 
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.bid-1*tick )
        
       #  LOB.bidBook.bidBook_public
       #  deque([[9.8, 500],
       #         [9.7, 500],
       #         [9.6, 1500],
       #         [9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000]])
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 500]],
       #         [['ZIagent', 500]],
       #         [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
    
    
    # Insert limit sell orders
    def test_LOB_insert_at_ask1(self):  
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0][1] == 1500
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 1500]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0][1] == 2000
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 1500], ['strategy', 500]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0][1] == 2500
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]]
        
        # LOB.askBook.askBook_public
        # deque([[10.5, 2500], [10.6, 1000], [10.7, 1000], [10.8, 1000], [10.9, 1000]])
        
        # LOB.askBook.askBook_private
        #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
        #         [['ZIagent', 1000]],
        #         [['ZIagent', 1000]],
        #         [['ZIagent', 1000]],
        #         [['ZIagent', 1000]]])
        
    
  
    def test_LOB_insert_at_ask2(self):  
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask+1*tick )
        assert LOB.askBook.askBook_public[1][1] == 1500
        assert LOB.askBook.askBook_private[1] == [['ZIagent', 1500]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.ask+1*tick )
        assert LOB.askBook.askBook_public[1][1] == 2000
        assert LOB.askBook.askBook_private[1] == [['ZIagent', 1500], ['strategy', 500]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask+1*tick )
        assert LOB.askBook.askBook_public[1][1] == 2500
        assert LOB.askBook.askBook_private[1] == [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]]
        
        
        # LOB.askBook.askBook_public
        # deque([[10.5, 2500], [10.6, 2500], [10.7, 1000], [10.8, 1000], [10.9, 1000]])
        
        # LOB.askBook.askBook_private
        #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
        #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
        #         [['ZIagent', 1000]],
        #         [['ZIagent', 1000]],
        #         [['ZIagent', 1000]]])
        
        
    
    def test_LOB_insert_new_ask1(self):  
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask-1*tick )
        assert LOB.askBook.askBook_public[0] == [LOB.askBook.ask, 500]
        assert LOB.askBook.askBook_private[0] == [[ 'ZIagent', 500 ]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0] == [LOB.askBook.ask, 1000]
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 500], ['strategy', 500]]
        
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0] == [LOB.askBook.ask, 1500]
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]]
        
        
       #  LOB.askBook.askBook_public
       #  deque([[10.4, 1500],
       #         [10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000]])
            
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
    
    
    def test_LOB_insert_new_ask1_leq2tick(self):  
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.ask-2*tick )
        
        assert LOB.askBook.askBook_public[0] == [LOB.askBook.ask, 500]
        assert LOB.askBook.askBook_public[1] == [round(LOB.askBook.ask+1*tick,4), 0]
        assert LOB.askBook.askBook_private[0] == [[ 'ZIagent', 500 ]]
        assert LOB.askBook.askBook_private[1] == []
        
       #  LOB.askBook.askBook_public
       #  deque([[10.2, 500],
       #         [10.3, 0],
       #         [10.4, 1500],
       #         [10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000]])
        
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 500]],
       #         [],
       #         [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
        
        
    
    
    '''Test: Cancel orders'''
    def test_LOB_cancel_bid_0(self):  
        ##
        LOB.update('cancel', 'buy', 500, 'ZIagent', LOB.bidBook.bid-tick )
        LOB.update('cancel', 'buy', 500, 'ZIagent', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_public[0] == [LOB.bidBook.bid, 1500]
        
       #  LOB.bidBook.bidBook_public
       #  deque([[9.6, 1500],
       #         [9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000],
       #         [9.3, 0],
       #         [9.2, 0]])
        
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [],
       #         []])
        
        
        
        
    def test_LOB_cancel_bid(self):  
        # [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]]
        LOB.update('cancel', 'buy', 100, 'strategy', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 500], ['strategy', 400], ['ZIagent', 500]]
        
        # [['ZIagent', 500], ['strategy', 400], ['ZIagent', 500]]
        LOB.update('cancel', 'buy', 700, 'ZIagent', LOB.bidBook.bid )
        assert LOB.bidBook.bidBook_private[0] == [['ZIagent', 300], ['strategy', 400]]
    
    
       # LOB.bidBook.bidBook_public
       # deque([[9.6, 700],
       #         [9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000]])
        

       # LOB.bidBook.bidBook_private
       # deque([[['ZIagent', 300], ['strategy', 400]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
    
    
    def test_LOB_cancel_ask_0(self):  
        ##
        LOB.update('cancel', 'sell', 500, 'ZIagent', LOB.askBook.ask )
        assert LOB.askBook.askBook_public[0] == [LOB.askBook.ask, 1500]
        
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],

        
       #  LOB.askBook.askBook_public
       #  deque([[10.4, 1500],
       #         [10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000],

        
        
        
    def test_LOB_cancel_ask(self):  
        
        # [['ZIagent', 500], ['strategy', 500], ['ZIagent', 500]]
        LOB.update('cancel', 'sell', 100, 'strategy', LOB.askBook.ask )
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 500], ['strategy', 400], ['ZIagent', 500]]
        
        
        # [['ZIagent', 500], ['strategy', 400], ['ZIagent', 500]]
        LOB.update('cancel', 'sell', 700, 'ZIagent', LOB.askBook.ask )
        assert LOB.askBook.askBook_private[0] == [['ZIagent', 300], ['strategy', 400]]
        
        
       #  LOB.askBook.askBook_public
       #  deque([[10.4, 700],
       #         [10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000],

        
        
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 300], ['strategy', 400]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
        
        
        
        
        
    
    '''Test: Cross market order'''
    def test_LOB_cross_market_buy(self):  
        ask_former = LOB.askBook.ask
        LOB.update('cross', 'buy', 700)
        assert LOB.askBook.ask == round(ask_former+1*tick,4)
        
       #  LOB.askBook.askBook_public
       #  deque([[10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000],
        
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
    
    def test_LOB_cross_market_buy_ask2eq0(self): 
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.ask-2*tick )
        
       #  LOB.askBook.askBook_public
       #  deque([[10.3, 500],
       #         [10.4, 0],
       #         [10.5, 2500],
       #         [10.6, 2500],
       #         [10.7, 1000],
       #         [10.8, 1000],
       #         [10.9, 1000]])
        
       #  LOB.askBook.askBook_private
       #  deque([[['strategy', 500]],
       #         [],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
        ask_former = LOB.askBook.ask
        LOB.update('cross', 'buy', 500)
        assert LOB.askBook.ask == round(ask_former+2*tick,4)
        
       # LOB.askBook.askBook_public
       # deque([[10.5, 2500], [10.6, 2500], [10.7, 1000], [10.8, 1000], [10.9, 1000]])
        
       #  LOB.askBook.askBook_private
       #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
        
        
        
    def test_LOB_cross_market_sell(self):  
        bid_former = LOB.bidBook.bid
        LOB.update('cross', 'sell', 700)
        assert LOB.bidBook.bid == round(bid_former-1*tick,4)
        
       #  LOB.bidBook.bidBook_public
       #  deque([[9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000],

        
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
        
    def test_LOB_cross_market_sell_bid2eq0(self): 
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.bid+2*tick )
       #  LOB.bidBook.bidBook_public
       #  deque([[9.7, 500],
       #         [9.6, 0],
       #         [9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000]])
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['strategy', 500]],
       #         [],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
        bid_former = LOB.bidBook.bid  #9.7
        LOB.update('cross', 'sell', 500)
        assert LOB.bidBook.bid == round(bid_former-2*tick,4)
        
       #  LOB.bidBook.bidBook_public
       #  deque([[9.5, 2500],
       #         [9.4, 2500],
       #         [9.3, 1000],
       #         [9.2, 1000],
       #         [9.1, 1000]])
        
       #  LOB.bidBook.bidBook_private
       #  deque([[['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1500], ['strategy', 500], ['ZIagent', 500]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]],
       #         [['ZIagent', 1000]]])
        
        
        
        
        
        
        
        
        
