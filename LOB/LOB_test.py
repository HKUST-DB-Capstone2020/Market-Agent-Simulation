from LOB import LimitOrderBook
import pytest

ask = 10.5
bid = 9.5
tick = 0.1
orderLevel = 5

class TestLOB:  
        
    '''Test: Insert orders'''
    # Insert limit buy orders
    def test_LOB_insert_at_bid1(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 1500      
        assert len(LOB.bidBook.Book_private[0]) == 1
        assert LOB.bidBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[0][-1].qty == 1500
        
        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 2000
        assert len(LOB.bidBook.Book_private[0]) == 2
        assert LOB.bidBook.Book_private[0][-1].ID == 'strategy'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 2500
        assert len(LOB.bidBook.Book_private[0]) == 3
        assert LOB.bidBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
          
    # LOB.bidBook.Book_public
    # deque([prc_qty(price=9.5, qty=2500),
    #        prc_qty(price=9.4, qty=1000),
    #        prc_qty(price=9.3, qty=1000),
    #        prc_qty(price=9.2, qty=1000),
    #        prc_qty(price=9.1, qty=1000)])
        
        
    # LOB.bidBook.Book_private
    # deque([[ID_qty(ID='ZIagent', qty=1500), ID_qty(ID='strategy', qty=500), ID_qty(ID='ZIagent', qty=500)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    
    def test_LOB_insert_at_bid2(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice-1*tick )
        
        assert LOB.bidBook.Book_public[1].qty == 1500      
        assert len(LOB.bidBook.Book_private[1]) == 1
        assert LOB.bidBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[1][-1].qty == 1500

        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.nearPrice-1*tick )
        assert LOB.bidBook.Book_public[1].qty == 2000
        assert len(LOB.bidBook.Book_private[1]) == 2
        assert LOB.bidBook.Book_private[1][-1].ID == 'strategy'
        assert LOB.bidBook.Book_private[1][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice-1*tick )
        assert LOB.bidBook.Book_public[1].qty == 2500
        assert len(LOB.bidBook.Book_private[1]) == 3
        assert LOB.bidBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[1][-1].qty == 500
        
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=2500),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1500), ID_qty(ID='strategy', qty=500), ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
    
    def test_LOB_insert_new_bid1(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice+1*tick )
        assert LOB.bidBook.Book_public[0].qty == 500      
        assert len(LOB.bidBook.Book_private[0]) == 1
        assert LOB.bidBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 1000
        assert len(LOB.bidBook.Book_private[0]) == 2
        assert LOB.bidBook.Book_private[0][-1].ID == 'strategy'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 1500
        assert len(LOB.bidBook.Book_private[0]) == 3
        assert LOB.bidBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
        
    
    # LOB.bidBook.Book_public
    # deque([prc_qty(price=9.6, qty=1500),
    #        prc_qty(price=9.5, qty=1000),
    #        prc_qty(price=9.4, qty=1000),
    #        prc_qty(price=9.3, qty=1000),
    #        prc_qty(price=9.2, qty=1000),
    #        prc_qty(price=9.1, qty=1000)])
    
    
    # LOB.bidBook.Book_private
    # deque([[ID_qty(ID='ZIagent', qty=500),ID_qty(ID='strategy', qty=500),ID_qty(ID='ZIagent', qty=500)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)],
    #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
    
    def test_LOB_insert_new_bid1_leq2tick(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice+2*tick )
        
        assert LOB.bidBook.Book_public[0].price == LOB.bidBook.nearPrice
        assert LOB.bidBook.Book_public[0].qty == 500
        assert len(LOB.bidBook.Book_private[0]) == 1
        assert LOB.bidBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[0][-1].qty == 500
        
        assert LOB.bidBook.Book_public[1].price == round(LOB.bidBook.nearPrice-1*tick,4)
        assert LOB.bidBook.Book_public[1].qty == 0
        assert LOB.bidBook.Book_private[1] == []
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.7, qty=500),
        #        prc_qty(price=9.6, qty=0),
        #        prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=500)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    def test_LOB_insert_bid_at_empty(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice+2*tick )
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice-1*tick )
        
        assert LOB.bidBook.Book_public[1].price == round(LOB.bidBook.nearPrice-1*tick,4)
        assert LOB.bidBook.Book_public[1].qty == 500
        assert len(LOB.bidBook.Book_private[1]) == 1
        assert LOB.bidBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[1][-1].qty == 500

        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.7, qty=500),
        #        prc_qty(price=9.6, qty=500),
        #        prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    def test_LOB_insert_beyond_bid(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice-(orderLevel+1)*tick )
        
        assert LOB.bidBook.Book_public[-1].price == round(LOB.bidBook.nearPrice-(orderLevel+1)*tick,4)
        assert LOB.bidBook.Book_public[-1].qty == 500
        assert len(LOB.bidBook.Book_private[-1]) == 1
        assert LOB.bidBook.Book_private[-1][-1].ID == 'ZIagent'
        assert LOB.bidBook.Book_private[-1][-1].qty == 500
        assert len(LOB.bidBook.Book_private[-2]) == 0
        assert LOB.bidBook.Book_private[-2] == []
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000),
        #        prc_qty(price=9.0, qty=0),
        #        prc_qty(price=8.9, qty=500)])
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=500)]])
    
    
    
    # Insert limit sell orders
    def test_LOB_insert_at_ask1(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 1500      
        assert len(LOB.askBook.Book_private[0]) == 1
        assert LOB.askBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[0][-1].qty == 1500
        
    
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 2000
        assert len(LOB.askBook.Book_private[0]) == 2
        assert LOB.askBook.Book_private[0][-1].ID == 'strategy'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 2500
        assert len(LOB.askBook.Book_private[0]) == 3
        assert LOB.askBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=2500),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1500),ID_qty(ID='strategy', qty=500),ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
    
  
    def test_LOB_insert_at_ask2(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice+1*tick )
        assert LOB.askBook.Book_public[1].qty == 1500      
        assert len(LOB.askBook.Book_private[1]) == 1
        assert LOB.askBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[1][-1].qty == 1500
        
        
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.nearPrice+1*tick )
        assert LOB.askBook.Book_public[1].qty == 2000
        assert len(LOB.askBook.Book_private[1]) == 2
        assert LOB.askBook.Book_private[1][-1].ID == 'strategy'
        assert LOB.askBook.Book_private[1][-1].qty == 500

        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice+1*tick )
        assert LOB.askBook.Book_public[1].qty == 2500
        assert len(LOB.askBook.Book_private[1]) == 3
        assert LOB.askBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[1][-1].qty == 500

        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=2500),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1500),ID_qty(ID='strategy', qty=500),ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
    
    def test_LOB_insert_new_ask1(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice-1*tick )
        assert LOB.askBook.Book_public[0].qty == 500      
        assert len(LOB.askBook.Book_private[0]) == 1
        assert LOB.askBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 1000
        assert len(LOB.askBook.Book_private[0]) == 2
        assert LOB.askBook.Book_private[0][-1].ID == 'strategy'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 1500
        assert len(LOB.askBook.Book_private[0]) == 3
        assert LOB.askBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.4, qty=1500),
        #        prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
            
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=500),ID_qty(ID='strategy', qty=500),ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    
    def test_LOB_insert_new_ask1_leq2tick(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice-2*tick )
        assert LOB.askBook.Book_public[0].price == LOB.askBook.nearPrice
        assert LOB.askBook.Book_public[0].qty == 500
        assert len(LOB.askBook.Book_private[0]) == 1
        assert LOB.askBook.Book_private[0][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[0][-1].qty == 500
        
        assert LOB.askBook.Book_public[1].price == round(LOB.askBook.nearPrice+1*tick,4)
        assert LOB.askBook.Book_public[1].qty == 0
        assert LOB.askBook.Book_private[1] == []
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.3, qty=500),
        #        prc_qty(price=10.4, qty=0),
        #        prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=500)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
    
    def test_LOB_insert_ask_at_empty(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice-2*tick )
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice+1*tick )
        
        assert LOB.askBook.Book_public[1].price == round(LOB.askBook.nearPrice+1*tick,4)
        assert LOB.askBook.Book_public[1].qty == 500
        assert len(LOB.askBook.Book_private[1]) == 1
        assert LOB.askBook.Book_private[1][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[1][-1].qty == 500

        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.3, qty=500),
        #        prc_qty(price=10.4, qty=500),
        #        prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    def test_LOB_insert_beyond_ask(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice+(orderLevel+1)*tick )
        
        assert LOB.askBook.Book_public[-1].price == round(LOB.askBook.nearPrice+(orderLevel+1)*tick,4)
        assert LOB.askBook.Book_public[-1].qty == 500
        assert len(LOB.askBook.Book_private[-1]) == 1
        assert LOB.askBook.Book_private[-1][-1].ID == 'ZIagent'
        assert LOB.askBook.Book_private[-1][-1].qty == 500
        assert len(LOB.askBook.Book_private[-2]) == 0
        assert LOB.askBook.Book_private[-2] == []
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000),
        #        prc_qty(price=11.0, qty=0),
        #        prc_qty(price=11.1, qty=500)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=500)]])

    
    

    
    '''Test: Cancel orders'''
    def test_LOB_cancel_bid_0(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        former_bid = LOB.bidBook.nearPrice
        LOB.update('cancel', 'buy', 1000, 'ZIagent', LOB.bidBook.nearPrice-tick )
        LOB.update('cancel', 'buy', 1000, 'ZIagent', LOB.bidBook.nearPrice )
        
        assert LOB.bidBook.nearPrice == former_bid-2*tick
        assert LOB.bidBook.Book_public[-1].qty == 0
        assert LOB.bidBook.Book_public[-2].qty == 0
        assert LOB.bidBook.Book_private[-1] == []
        assert LOB.bidBook.Book_private[-2] == []

        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000),
        #        prc_qty(price=9.0, qty=0),
        #        prc_qty(price=8.9, qty=0)])
        
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [],
        #        []])
        
        
        
        
    def test_LOB_cancel_bid(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.nearPrice )
        LOB.update('insert', 'buy', 500, 'ZIagent', LOB.bidBook.nearPrice )
        
        # [['ZIagent', 1000], ['strategy', 500], ['ZIagent', 500]]
        LOB.update('cancel', 'buy', 100, 'strategy', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 1900
        assert LOB.bidBook.Book_private[0][1].qty == 400
        assert LOB.bidBook.Book_private[0][0].qty == 1000
        assert LOB.bidBook.Book_private[0][2].qty == 500
        
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.5, qty=1900),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000),ID_qty(ID='strategy', qty=400),ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        LOB.update('cancel', 'buy', 700, 'ZIagent', LOB.bidBook.nearPrice )
        assert LOB.bidBook.Book_public[0].qty == 1200
        assert LOB.bidBook.Book_private[0][1].qty == 400
        assert LOB.bidBook.Book_private[0][0].qty == 800
        assert len(LOB.bidBook.Book_private[0]) == 2


        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.5, qty=1200),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=800), ID_qty(ID='strategy', qty=400)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
    
    
    
    def test_LOB_cancel_ask_0(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ##
        former_ask = LOB.askBook.nearPrice
        LOB.update('cancel', 'sell', 1000, 'ZIagent', LOB.askBook.nearPrice+tick )
        LOB.update('cancel', 'sell', 1000, 'ZIagent', LOB.askBook.nearPrice )

        assert LOB.askBook.nearPrice == former_ask+2*tick
        assert LOB.askBook.Book_public[-1].qty == 0
        assert LOB.askBook.Book_public[-2].qty == 0
        assert LOB.askBook.Book_private[-1] == []
        assert LOB.askBook.Book_private[-2] == []

        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [],
        #        []])

        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000),
        #        prc_qty(price=11.0, qty=0),
        #        prc_qty(price=11.1, qty=0)])

        
        
        
    def test_LOB_cancel_ask(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.nearPrice )
        LOB.update('insert', 'sell', 500, 'ZIagent', LOB.askBook.nearPrice )
        
        
        # [['ZIagent', 1000], ['strategy', 500], ['ZIagent', 500]]
        LOB.update('cancel', 'sell', 100, 'strategy', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 1900
        assert LOB.askBook.Book_private[0][1].qty == 400
        assert LOB.askBook.Book_private[0][0].qty == 1000
        assert LOB.askBook.Book_private[0][2].qty == 500
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=1900),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000),ID_qty(ID='strategy', qty=400),ID_qty(ID='ZIagent', qty=500)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        LOB.update('cancel', 'sell', 700, 'ZIagent', LOB.askBook.nearPrice )
        assert LOB.askBook.Book_public[0].qty == 1200
        assert LOB.askBook.Book_private[0][1].qty == 400
        assert LOB.askBook.Book_private[0][0].qty == 800
        assert len(LOB.askBook.Book_private[0]) == 2
        
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=1200),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])


        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=800), ID_qty(ID='strategy', qty=400)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        
        
        
    
    '''Test: Cross market order'''
    def test_LOB_cross_market_buy(self):  
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        ask_former = LOB.askBook.nearPrice
        LOB.update('cross', 'buy', 1000)
        assert LOB.askBook.nearPrice == round(ask_former+1*tick,4)
        assert LOB.askBook.Book_public[-1].qty == 0
        assert LOB.askBook.Book_public[-1].price == LOB.askBook.nearPrice + (orderLevel-1)*tick
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000),
        #        prc_qty(price=11.0, qty=0)])
        
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        []])
    
    
    def test_LOB_cross_market_buy_ask2eq0(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        LOB.update('insert', 'sell', 500, 'strategy', LOB.askBook.nearPrice-2*tick )
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.3, qty=500),
        #        prc_qty(price=10.4, qty=0),
        #        prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='strategy', qty=500)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        ask_former = LOB.askBook.nearPrice
        LOB.update('cross', 'buy', 500)
        assert LOB.askBook.nearPrice == round(ask_former+2*tick,4)
        
        # LOB.askBook.Book_public
        # deque([prc_qty(price=10.5, qty=1000),
        #        prc_qty(price=10.6, qty=1000),
        #        prc_qty(price=10.7, qty=1000),
        #        prc_qty(price=10.8, qty=1000),
        #        prc_qty(price=10.9, qty=1000)])
        
        
        # LOB.askBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        
    def test_LOB_cross_market_sell(self):  
        
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        bid_former = LOB.bidBook.nearPrice
        LOB.update('cross', 'sell', 1000)
        assert LOB.bidBook.nearPrice == round(bid_former-1*tick,4)
        assert LOB.bidBook.Book_public[-1].qty == 0
        assert LOB.bidBook.Book_public[-1].price == LOB.bidBook.nearPrice - (orderLevel-1)*tick
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000),
        #        prc_qty(price=9.0, qty=0)])

        
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        []])
        
    def test_LOB_cross_market_sell_bid2eq0(self): 
        
        LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        
        LOB.update('insert', 'buy', 500, 'strategy', LOB.bidBook.nearPrice+2*tick )
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.7, qty=500),
        #        prc_qty(price=9.6, qty=0),
        #        prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='strategy', qty=500)],
        #        [],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        bid_former = LOB.bidBook.nearPrice 
        LOB.update('cross', 'sell', 500)
        assert LOB.bidBook.nearPrice == round(bid_former-2*tick,4)
        
        # LOB.bidBook.Book_public
        # deque([prc_qty(price=9.5, qty=1000),
        #        prc_qty(price=9.4, qty=1000),
        #        prc_qty(price=9.3, qty=1000),
        #        prc_qty(price=9.2, qty=1000),
        #        prc_qty(price=9.1, qty=1000)])
        
        
        # LOB.bidBook.Book_private
        # deque([[ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)],
        #        [ID_qty(ID='ZIagent', qty=1000)]])
        
        
        
if __name__ == "__main__":
    pytest.main()
        
        
        
        
        
        
