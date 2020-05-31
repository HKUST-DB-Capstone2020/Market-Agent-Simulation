import collections
import copy

isASK = 1
isBID = -1

class Book:
    
    def __init__(self, bidORask, nearPrice, tick, orderLevel, init_qty = 1000):
        self.bidORask     = isASK   if bidORask == 'ask' else isBID
        self.prc_qty      = collections.namedtuple('prc_qty',['price','qty'])
        self.ID_qty       = collections.namedtuple('ID_qty', ['ID','qty'])
        self.nearPrice    = nearPrice
        self.tick         = tick
        self.orderLevel   = orderLevel
        self.init_qty     = init_qty
        self.Book_public  = collections.deque( self.prc_qty(price = round(self.nearPrice + self.bidORask*i*self.tick,4), 
                                                            qty   = self.init_qty) 
                                               for i in range(self.orderLevel) )
        self.Book_private = collections.deque( [self.ID_qty(ID = 'ZIagent', qty = self.init_qty)] for i in range(self.orderLevel) )
        

    def reset(self, nearPrice):
        self.nearPrice = nearPrice
        self.Book_public.clear()
        self.Book_public.extend(self.prc_qty(price = round(self.nearPrice+ self.bidORask*i*self.tick,4), 
                                             qty   = self.init_qty) 
                                for i in range(self.orderLevel))
        
        self.Book_private.clear()
        self.Book_private.extend( [self.ID_qty(ID = 'ZIagent', qty = self.init_qty)] for i in range(self.orderLevel) )
        
        
    def isEmpty(self):
        '''Judge: whether the book is empty'''
        return [ self.Book_public[i].qty for i in range(len(self.Book_public)) ] == [0 for i in range(len(self.Book_public))]
    
    
    def set_nearPrice_isEmpty(self):
        ''''Override in child classes'''
        pass
    
    
    def insert(self, ID, limitPrice, quantity):
        
        if self.isEmpty(): # book is empty
            self.nearPrice = round(limitPrice,4)
            self.Book_public.append(self.prc_qty(price = self.nearPrice, qty = quantity))
            self.Book_private.append([ self.ID_qty(ID = ID, qty = quantity) ])
            
            for i in range(self.orderLevel-1):
                self.Book_public.append(self.prc_qty(price = round(self.nearPrice + self.bidORask*(i+1)*self.tick,4), qty = 0))
                self.Book_private.append([])
        else:  # book is not empty
            book_loc = round(self.bidORask * (limitPrice - self.nearPrice)/self.tick)
            if book_loc<0:  # limit price is in the spread
                ## -1, -2, -3, ....
                for i in range(-book_loc-1):
                    self.Book_public.appendleft(self.prc_qty(price = round(self.nearPrice - self.bidORask*(i+1)*self.tick,4), qty = 0))
                    self.Book_private.appendleft([])
                
                self.nearPrice = round(limitPrice,4)
                self.Book_public.appendleft(self.prc_qty(price = self.nearPrice, qty = quantity))
                self.Book_private.appendleft([ self.ID_qty(ID = ID, qty = quantity) ])
            
            elif book_loc >= len(self.Book_public): # beyond the book 
                farPrice = self.Book_public[-1].price
                for i in range( book_loc - len(self.Book_public) ):
                    self.Book_public.append(self.prc_qty(price = round(farPrice + self.bidORask*(i+1)*self.tick,4), qty = 0))
                    self.Book_private.append([])
                
                self.Book_public.append( self.prc_qty(price = round(limitPrice,4), qty = quantity) )
                self.Book_private.append([ self.ID_qty(ID = ID, qty = quantity) ])
                
            else:  # normally insert
                self.Book_public[book_loc] = self.Book_public[book_loc]._replace( qty=self.Book_public[book_loc].qty + quantity ) 
    
                if len(self.Book_private[book_loc]) ==0: # private book is empty
                    self.Book_private[book_loc].append(self.ID_qty(ID = ID, qty = quantity))
                else: # private book is not empty
                    if self.Book_private[book_loc][-1].ID == ID:  # last guy in the queue has same ID
                        self.Book_private[book_loc][-1] = self.Book_private[book_loc][-1]._replace( qty=self.Book_private[book_loc][-1].qty + quantity ) 
                    else:
                        self.Book_private[book_loc].append( self.ID_qty(ID = ID, qty = quantity) )

    
    def cancel(self, ID, limitPrice, quantity):
        # Before passing in parameters, make sure (by OMS)
        # (1) price range is legal, i.e. not beyond the book
        # (2) the qty to cancel <= all qty this ID has inserted before
        
        book_loc = round(self.bidORask * (limitPrice - self.nearPrice)/self.tick)
        self.Book_public[book_loc] = self.Book_public[book_loc]._replace( qty=self.Book_public[book_loc].qty - quantity ) 
        
        if self.Book_public[book_loc].qty==0: #this level is cancel out (meaning: previous orders are all from this ID)
            if book_loc!=0: # not near price，need to keep this level
                self.Book_private[book_loc] = []
            else:           # is near price，need to remove this level
                # judge if the whole book becomes empty after this cancellation
                if self.isEmpty():      
                    self.set_nearPrice_isEmpty()
                    self.Book_public.clear()
                    self.Book_private.clear()
                else:    
                    while self.Book_public[0].qty == 0:
                        self.nearPrice = self.Book_public[1].price
    
                        self.Book_public.popleft()
                        self.Book_private.popleft()
                        
                        if len(self.Book_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                            self.Book_public.append(self.prc_qty(price = round(self.nearPrice+ self.bidORask*(self.orderLevel-1)*self.tick,4), 
                                                                 qty   = 0))
                            self.Book_private.append([])
        
        else:  # find the ID to cancel
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.Book_private[book_loc][-1].ID == ID: # tail orders are from this ID
                    if self.Book_private[book_loc][-1].qty < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.Book_private[book_loc][-1].qty
                        self.Book_private[book_loc].pop(-1)
                    else:  # enough to cancel
                        self.Book_private[book_loc][-1] = self.Book_private[book_loc][-1]._replace( qty=self.Book_private[book_loc][-1].qty - qty_to_cancel ) 
                        qty_to_cancel = 0
                else: # penultimate orders are from this ID
                    if self.Book_private[book_loc][-2].qty < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.Book_private[book_loc][-2].qty
                        self.Book_private[book_loc].pop(-2)
                    else:  # enough to cancel
                        self.Book_private[book_loc][-2] = self.Book_private[book_loc][-2]._replace( qty=self.Book_private[book_loc][-2].qty - qty_to_cancel ) 
                        qty_to_cancel = 0


    def cross(self, quantity):
        ## need to rely on OMS to make sure :
        ## size to cross <= existing size at bid1/ask1
        self.Book_public[0] = self.Book_public[0]._replace( qty=self.Book_public[0].qty - quantity ) 
        
        if self.Book_public[0].qty == 0:   ## nearest level is eaten up
            
            result_record = copy.deepcopy(self.Book_private[0])
            
            # judge if the book becomes empty after this cross
            if self.isEmpty():
                self.set_nearPrice_isEmpty()
                self.Book_public.clear()
                self.Book_private.clear()
            else:  
                #find the next non-empty level
                while self.Book_public[0].qty == 0: 
                    self.nearPrice = self.Book_public[1].price
                    
                    self.Book_public.popleft()
                    self.Book_private.popleft()
                    
                    if len(self.Book_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                        self.Book_public.append(self.prc_qty(price = round(self.nearPrice+ self.bidORask*(self.orderLevel-1)*self.tick,4), 
                                                             qty   = 0))
                        self.Book_private.append([])
        else:  ## nearest level is not eaten up
            
            result_record = []
            
            #find the ID to cancel
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.Book_private[0][0].qty < qty_to_cancel: # first guy in the queue is not enough to cancel
                    result_record.append( copy.deepcopy(self.Book_private[0][0]) )
                    qty_to_cancel -= self.Book_private[0][0].qty
                    self.Book_private[0].pop(0)
                else:
                    result_record.append( self.Book_private[0][0]._replace( qty=qty_to_cancel )  )
                    self.Book_private[0][0] = self.Book_private[0][0]._replace( qty=self.Book_private[0][0].qty - qty_to_cancel ) 
                    qty_to_cancel = 0
                    
        return result_record




class AskBook(Book):
    
    def __init__(self, askPrice, tick, orderLevel, init_size = 1000):
        Book.__init__(self, 'ask', askPrice, tick, orderLevel, init_size)

    def set_nearPrice_isEmpty(self):
        ''''Override in child classes'''
        self.nearPrice = 4560987


class BidBook(Book):
    
    def __init__(self, bidPrice, tick, orderLevel, init_size = 1000):
        Book.__init__(self, 'bid', bidPrice, tick, orderLevel, init_size)
    
    def set_nearPrice_isEmpty(self):
        ''''Override in child classes'''
        self.nearPrice = 0



#######################################################################################################
#######################################################################################################
#######################################################################################################




class LimitOrderBook:
    
    def __init__(self, askPrice, bidPrice, tick, orderLevel, init_size=1000):
        '''Initialize the limit order book'''
        try:
            assert askPrice > bidPrice
            self.askBook = AskBook(askPrice, tick, orderLevel, init_size)
            self.bidBook = BidBook(bidPrice, tick, orderLevel, init_size)
        except:
            print("Creating LOB Failed: Ask price must be larger than bid price.")
        
    def reset(self, askPrice, bidPrice):
        '''Reset the limit order book'''
        self.askBook.reset(askPrice)
        self.bidBook.reset(bidPrice)
    
    def update(self, orderType, orderSide, quantity, ID=None, limitPrice=0):
        '''Update the limit order book'''
        if orderType == 'insert':
            if orderSide == 'buy':
                self.bidBook.insert(ID, limitPrice, quantity)  
            elif orderSide == 'sell':
                self.askBook.insert(ID, limitPrice, quantity)
            return []
        
        elif orderType == 'cancel':
            if orderSide == 'buy':
                self.bidBook.cancel(ID, limitPrice, quantity)
                    
            elif orderSide == 'sell':
                self.askBook.cancel(ID, limitPrice, quantity)
            return []
            
        elif orderType == 'cross':
            if orderSide == 'buy':
                ## market buy order (need to cross it in the askBook)
                return self.askBook.cross(quantity)

            elif orderSide == 'sell':
                ## market sell order(need to cross it in the bidBook)
                return self.bidBook.cross(quantity)
        
   
