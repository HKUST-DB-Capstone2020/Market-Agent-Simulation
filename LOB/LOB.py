## 3 classes in this file
## (1) AskBook
## (2) BidBook
## (3) LimitOrderBook


import collections

class AskBook:
    
    def __init__(self, ask, tick, orderLevel, init_size = 1000):
        self.ask = ask
        self.tick = tick
        self.orderLevel = orderLevel
        self.init_size = init_size
        self.askBook_public = collections.deque( [round(self.ask + i*self.tick,4), self.init_size] for i in range(self.orderLevel) )
        self.askBook_private = collections.deque( [['ZIagent', self.init_size]] for i in range(self.orderLevel) )
        self.price_loc = 0
        self.qty_loc = 1
    
    def reset(self, ask):
        self.ask = ask
        self.askBook_public.clear()
        self.askBook_public.extend([round(self.ask + i*self.tick,4), self.init_size] for i in range(self.orderLevel))
        
        self.askBook_private.clear()
        self.askBook_private.extend([['ZIagent', self.init_size]] for i in range(self.orderLevel))

    def insert(self, ID, limitPrice, quantity):
        # judge if book is empty
        if self.ask == 4560987:
            self.ask = round(limitPrice,4)
            self.askBook_public.append([self.ask, quantity])
            self.askBook_private.append([ [ID, quantity] ])
            
            for i in range(self.orderLevel-1):
                self.askBook_public.append([round(self.ask + (i+1)*self.tick,4), 0])
                self.askBook_private.append([])
        else:
            book_loc = round( (limitPrice - self.ask)/self.tick )
            if book_loc<0:  # limit bid price is in the spread
                ## -1, -2, -3, ....
                for i in range(-book_loc-1):
                    self.askBook_public.appendleft([round(self.ask - (i+1)*self.tick,4), 0])
                    self.askBook_private.appendleft([])
                
                self.askBook_public.appendleft([round(limitPrice,4), quantity])
                self.ask = round(limitPrice,4)
                
                self.askBook_private.appendleft([ [ID, quantity] ])
                
            else:
                self.askBook_public[book_loc][self.qty_loc] += quantity
    
                if len(self.askBook_private[book_loc]) ==0: # private book is empty
                    self.askBook_private[book_loc].append( [ID, quantity] )
                elif self.askBook_private[book_loc][-1][0] == ID:  # same ID
                    self.askBook_private[book_loc][-1][1] += quantity
                else:
                    self.askBook_private[book_loc].append( [ID, quantity] )

    def cancel(self, ID, limitPrice, quantity):
        # Before passing in parameters, make sure (by OMS)
        # (1) price range is legal, i.e. not beyond the book
        # (2) the qty to cancel <= all qty this ID has inserted before
        
        book_loc = round((limitPrice - self.ask)/self.tick)
        self.askBook_public[book_loc][self.qty_loc] -= quantity
        
        if self.askBook_public[book_loc][self.qty_loc]==0: #this level is cancel out (meaning: previous orders are all from this ID)
            if book_loc!=0: # not best ask，need to keep this level
                self.askBook_private[book_loc][0][0] = 'None'
                self.askBook_private[book_loc][0][1] = 0
            else:
                # judge if the book becomes empty after this cancellation
                if [ self.askBook_public[i][self.qty_loc] for i in range(len(self.askBook_public)) ] == [0 for i in range(len(self.askBook_public))]:      
                    self.ask = 4560987
                    self.askBook_public.clear()
                    self.askBook_private.clear()
                else:    
                    while self.askBook_public[0][self.qty_loc]==0:
                        self.ask = self.askBook_public[1][self.price_loc]
    
                        self.askBook_public.popleft()
                        self.askBook_private.popleft()
                        
                        if len(self.askBook_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                            self.askBook_public.append( [round(self.ask+(self.orderLevel-1)*self.tick,4), 0] )
                            self.askBook_private.append([])
        
        else:  # find the ID to cancel
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.askBook_private[book_loc][-1][0] == ID: # tail orders are from this ID
                    if self.askBook_private[book_loc][-1][1] < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.askBook_private[book_loc][-1][1]
                        self.askBook_private[book_loc].pop(-1)
                    else:  # enough to cancel
                        self.askBook_private[book_loc][-1][1] -= qty_to_cancel
                        qty_to_cancel = 0
                else: # penultimate orders are from this ID
                    if self.askBook_private[book_loc][-2][1] < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.askBook_private[book_loc][-2][1]
                        self.askBook_private[book_loc].pop(-2)
                    else:
                        self.askBook_private[book_loc][-2][1] -= qty_to_cancel
                        qty_to_cancel = 0
            

    def cross(self, quantity):
        ## need to rely on OMS to make sure :
        ## size to cross <= existing size at bid1/ask1
        self.askBook_public[0][self.qty_loc] -= quantity
        
        if self.askBook_public[0][self.qty_loc]==0:   ##ask1 is eaten up
            # judge if the book becomes empty after this cancellation
            if [ self.askBook_public[i][self.qty_loc] for i in range(len(self.askBook_public)) ] == [0 for i in range(len(self.askBook_public))]:
                self.ask = 4560987
                self.askBook_public.clear()
                self.askBook_private.clear()
            else:  #find the next non-empty level
                while self.askBook_public[0][self.qty_loc]==0: 
                    self.ask = self.askBook_public[1][self.price_loc]
                    
                    self.askBook_public.popleft()
                    self.askBook_private.popleft()
                    
                    if len(self.askBook_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                        self.askBook_public.append( [round(self.ask+(self.orderLevel-1)*self.tick,4), 0] )
                        self.askBook_private.append([])
        else:
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.askBook_private[0][0][1] < qty_to_cancel: # not enough to cancel
                    qty_to_cancel -= self.askBook_private[0][0][1]
                    self.askBook_private[0].pop(0)
                else:
                    self.askBook_private[0][0][1] -= qty_to_cancel
                    qty_to_cancel = 0
            
            
            
#######################################################################################################
#######################################################################################################
#######################################################################################################


class BidBook:
    
    def __init__(self, bid, tick, orderLevel, init_size=1000):
        self.bid = bid
        self.tick = tick
        self.orderLevel = orderLevel
        self.init_size = init_size
        self.bidBook_public = collections.deque( [round(self.bid - i*self.tick,4), self.init_size] for i in range(self.orderLevel) )
        self.bidBook_private = collections.deque( [['ZIagent', self.init_size]] for i in range(self.orderLevel) )
        
        self.price_loc = 0
        self.qty_loc = 1
        
    def reset(self, bid):
        self.bid = bid
        self.bidBook_public.clear()
        self.bidBook_public.extend([round(self.bid - i*self.tick,4), self.init_size] for i in range(self.orderLevel))
        
        self.bidBook_private.clear()
        self.bidBook_private.extend([['ZIagent', self.init_size]] for i in range(self.orderLevel))
        
    def insert(self, ID, limitPrice, quantity):
        # # judge if book is empty
        if self.bid == 0:
            self.bid = round(limitPrice,4)
            self.bidBook_public.append([self.bid, quantity])
            self.bidBook_private.append([ [ID, quantity] ])
            
            for i in range(self.orderLevel-1):
                self.bidBook_public.append([round(self.bid - (i+1)*self.tick,4), 0])
                self.bidBook_private.append([])
        else:  #book is not empty
            book_loc = round( (self.bid - limitPrice)/self.tick )
            if book_loc<0:  # limit bid price is in the spread
                
                ## -1, -2, -3, ....
                for i in range(-book_loc-1):
                    self.bidBook_public.appendleft([round(self.bid + (i+1)*self.tick,4), 0])
                    self.bidBook_private.appendleft([])
                
                
                self.bidBook_public.appendleft([round(limitPrice,4), quantity])
                self.bid = round(limitPrice,4)
                
                self.bidBook_private.appendleft([ [ID, quantity] ])
                
            else:
                self.bidBook_public[book_loc][self.qty_loc] += quantity
    
                
                if len(self.bidBook_private[book_loc]) ==0:  # judge if private book is empty, otherwise index is out of bound
                    self.bidBook_private[book_loc].append( [ID, quantity] )
                elif self.bidBook_private[book_loc][-1][0] == ID:  # same ID
                    self.bidBook_private[book_loc][-1][1] += quantity
                else:  #  not same ID
                    self.bidBook_private[book_loc].append( [ID, quantity] )
    
    def cancel(self, ID, limitPrice, quantity):
        book_loc = round((self.bid - limitPrice)/self.tick)
        self.bidBook_public[book_loc][self.qty_loc] -= quantity
        
        if self.bidBook_public[book_loc][self.qty_loc]==0: ##this level is cancel out (meaning: previous orders are all from this ID)
            if book_loc!=0: # not best bid，need to keep this level
                self.bidBook_private[book_loc][0][0] = 'None'
                self.bidBook_private[book_loc][0][1] = 0
            else:  # best bid
                # # judge if the book becomes empty after this cancellation
                if [ self.bidBook_public[i][self.qty_loc] for i in range(len(self.bidBook_public)) ] == [0 for i in range(len(self.bidBook_public))]:
                    self.bid = 0
                    self.bidBook_public.clear()
                    self.bidBook_private.clear()
                else:    
                    while self.bidBook_public[0][self.qty_loc]==0:
                        self.bid = self.bidBook_public[1][self.price_loc]
    
                        self.bidBook_public.popleft()
                        self.bidBook_private.popleft()
                        
                        if len(self.bidBook_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                            self.bidBook_public.append( [round(self.bid-(self.orderLevel-1)*self.tick,4), 0] )
                            self.bidBook_private.append([])
                
        else:
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.bidBook_private[book_loc][-1][0] == ID: # # tail orders are from this ID
                    if self.bidBook_private[book_loc][-1][1] < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.bidBook_private[book_loc][-1][1]
                        self.bidBook_private[book_loc].pop(-1)
                    else:  # enough to cancel
                        self.bidBook_private[book_loc][-1][1] -= qty_to_cancel
                        qty_to_cancel = 0
                else: # penultimate orders are from this ID
                    if self.bidBook_private[book_loc][-2][1] < qty_to_cancel: # not enough to cancel
                        qty_to_cancel -= self.bidBook_private[book_loc][-2][1]
                        self.bidBook_private[book_loc].pop(-2)
                    else:
                        self.bidBook_private[book_loc][-2][1] -= qty_to_cancel
                        qty_to_cancel = 0
            
    def cross(self, quantity):
        self.bidBook_public[0][self.qty_loc] -= quantity
        
        if self.bidBook_public[0][self.qty_loc]==0:  # bid1 is eaten up
            # judge if the book becomes empty after this cancellation
            if [ self.bidBook_public[i][self.qty_loc] for i in range(len(self.bidBook_public)) ] == [0 for i in range(len(self.bidBook_public))]:
                self.bid = 0
                self.bidBook_public.clear()
                self.bidBook_private.clear()
            else: #find the next non-empty level
                while self.bidBook_public[0][self.qty_loc]==0:
                    self.bid = self.bidBook_public[1][self.price_loc]
                    
                    self.bidBook_public.popleft()
                    self.bidBook_private.popleft()
                    
                    if len(self.bidBook_public) < self.orderLevel:  # length of orderbook < orderLevel: need to keep at least minimal length
                        self.bidBook_public.append( [round(self.bid-(self.orderLevel-1)*self.tick,4), 0] )
                        self.bidBook_private.append([])
        
        else:
            qty_to_cancel = quantity
            while qty_to_cancel > 0:
                if self.bidBook_private[0][0][1] < qty_to_cancel: # not enough to cancel
                    qty_to_cancel -= self.bidBook_private[0][0][1]
                    self.bidBook_private[0].pop(0)
                else:
                    self.bidBook_private[0][0][1] -= qty_to_cancel
                    qty_to_cancel = 0
            



#######################################################################################################
#######################################################################################################
#######################################################################################################




class LimitOrderBook:
    
    def __init__(self, ask, bid, tick, orderLevel):
        '''Initialize the limit order book'''
        self.askBook = AskBook(ask, tick, orderLevel)
        self.bidBook = BidBook(bid, tick, orderLevel)
        
    def reset(self, ask, bid):
        '''Reset the limit order book'''
        self.askBook.reset(ask)
        self.bidBook.reset(bid)
    
    def update(self, orderType, orderSide, quantity, ID=None, limitPrice=0):
        '''Update the limit order book'''
        if orderType == 'insert':
            if orderSide == 'buy':
                self.bidBook.insert(ID, limitPrice, quantity)  
            elif orderSide == 'sell':
                self.askBook.insert(ID, limitPrice, quantity)
        
        elif orderType == 'cancel':
            if orderSide == 'buy':
                self.bidBook.cancel(ID, limitPrice, quantity)
                    
            elif orderSide == 'sell':
                self.askBook.cancel(ID, limitPrice, quantity)
            
        elif orderType == 'cross':
            if orderSide == 'buy':
                ## market buy order (need to cross it in the askBook)
                self.askBook.cross(quantity)

            elif orderSide == 'sell':
                ## market sell order
                self.bidBook.cross(quantity)
        
   
