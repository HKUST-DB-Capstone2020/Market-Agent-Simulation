import os
import pandas as pd
import sys
sys.path.append(os.path.pardir)
from LOB.LOB import LimitOrderBook

class action():
    def __init__(self, input_action):
        self.agent, self.type, self.direction, self.quantity, self.price = input_action
           
            
class OrderManagementSystem:
    
    def __init__(self, ask, bid, tick, orderLevel, lastPrice):
        '''Instantiate an LOB'''
        self.LOB = LimitOrderBook( ask, bid, tick, orderLevel)
        self.tick = tick
        self.lastPrice = lastPrice  # prevailing market price
        self.execPrice = []
        self.execQty = []
#         self.status = "Auction"

    def receive(self, agent_action):
        '''
        input:
            action:  [agent, type,  direction， quantity, price]
                              market buy
                              limit  sell
                              cancel
        '''
        self.action = action(agent_action)
        self.CDA()
        
#         if self.status != "Auction":
#             CDA()
#         else:
#             self.LOB.add_action(agent_action)  #
    
    
    
#     def at_auction(self):
#         self.cal_auction_price()
#         ask_quantity = self.maxVolume
#         bid_quantity = self.maxVolume
        
#         for i in self.cal_df.index:
#             if i>self.aucton_price:
#                 self.LOB.update("cross", "buy", self.cal_df.loc[i,"buy"])
#                 bid_quantity -= self.cal_df.loc[i,"buy"]
                
#         if bid_quantity>0:
#             self.LOB.update("cross", "buy", bid_quantity)
        
#         for i in self.cal_df.index[::-1]:
#             if i<self.aucton_price:
#                 self.LOB.update("cross", "sell", self.cal_df.loc[i,"sell"])
#                 ask_quantity -= self.cal_df.loc[i,"sell"]
                
#         if ask_quantity>0:
#             self.LOB.update("cross", "sell", ask_quantity)
        
        
        
#     def cal_auction_price(self):
#         price_list = sorted(list(np.arange(LOB.ask_price + len(LOB.ask_book.askBook_public)*self.tick, 
#                                            LOB.bid_price - (len(LOB.bid_price.bidBook_public)+1)*self.tick, 
#                                            -self.tick)))
#         cal_df = pd.DataFrame(index = price_list, columns = ["buy", "sell"])
        
        
#         for i in range(len(LOB.bid_book.bidBook_public)):
#             cal_df.loc[-i*self.tick + LOB.bid_price,"buy"] = LOB.bid_book.bidBook_public[i]
#         for i in range(len(LOB.ask_book.askBook_public)):
#             cal_df.loc[i*self.tick + LOB.ask_price,"sell"] = LOB.ask_book.askBook_public[i]
            
            
#         cal_df.loc[LOB.bid_price - len(LOB.bid_book.bidBook_public),"buy"] = LOB.auction_bid_market_order.public
#         cal_df.loc[LOB.ask_price - len(LOB.ask_book.askBook_public),"sell"] = LOB.auction_ask_market_order.public
        
#         cal_df["cumBuy"] = cal_df["buy"].cumsum()
#         cal_df["cumSell"] = cal_df["sell"][::-1].cumsum()[::-1]
        
#         cal_df["maxVolume"] = cal_df[["cumBuy", "cumSell"]].max(axis = 1)
#         maxVolume = cal_df["maxVolume"].max()
#         self.maxVolume = maxVolume
#         self.cal_df = cal_df
        
#         sub_df = cal_df[cal_df["maxVolume"]==maxVolume]
        
#         if sub_df.shape[0] == 1:
#             self.aucton_price = sub_df.index[0]
#         else:
#             sub_df["imbalance"] = sub_df["cumBuy"] - sub_df["cumSell"]
#             sub_df["absImb"] = sub_df["imbalance"].abs()
#             minImbalance = sub_df["absImb"].min()
#             sub_df = cal_df[cal_df["absImb"]==minImbalance]
            
#             if sub_df.shape[0] == 1:
#                 self.aucton_price = sub_df.index[0]
#             else:
#                 imba_list =  sub_df["imbalance"].tolist()
#                 if imba_list[0]*imba_list[-1] >= 0:
#                     if imba_list[0]>0:
#                         self.aucton_price = sub_df.index[0]
#                     elif imba_list[0]<0:
#                         self.aucton_price = sub_df.index[-1]
#                     else:
#                         if (imba_list[0]-self.lastPrice)*(imba_list[-1]-self.lastPrice)<=0:
#                             self.aucton_price = self.lastPrice
#                         elif abs(imba_list[0]-self.lastPrice) > abs(imba_list[-1]-self.lastPrice) :
#                             self.aucton_price = sub_df.index[-1]
#                         else:
#                             self.aucton_price = sub_df.index[0]
                
#                 else:
#                     for i in range(len(imba_list)-1):
#                         if abs(imba_list[i]-self.lastPrice) > abs(imba_list[i+1]-self.lastPrice):
#                             self.aucton_price = sub_df.index[i]
                        
    
    
#     def send_message(agent, price, volume):
#         pass
                 
    
#     def market_order(self):
#         if self.action.direction == "buy":
#             while self.action.quantity > 0:
#                 try:
#                     if self.action.quantity > self.LOB.askBook.askBook_public[0][1]:
#                         self.action.quantity -= self.LOB.askBook.askBook_public[0][1]
#                         self.LOB.update("cross", "buy", self.LOB.askBook.askBook_public[0][1])
#                         self.lastPrice = self.askBook.ask
#                         print(self.lastPrice)

#                     else:
#                         self.LOB.update("cross", "buy", self.action.quantity)
#                         self.action.quantity = 0
#                         self.lastPrice = self.LOB.askBook.ask
#                          print(self.lastPrice)
#                 except:
#                     self.action.quantity = 0
                    
#         elif self.action.direction == "sell":
#             while self.action.quantity > 0:
#                 try:
#                     if self.action.quantity > self.LOB.bidBook.bidBook_public[0][1]:
#                         self.action.quantity -= self.LOB.bidBook.bidBook_public[0][1]
#                         self.LOB.update("cross", "sell", self.LOB.bidBook.bidBook_public[0][1])
#                         self.lastPrice = self.LOB.bidBook.bid

#                     else:
#                         self.LOB.update("cross", "sell", self.action.quantity)
#                         self.action.quantity = 0
#                         self.lastPrice = self.LOB.bidBook.bid
#                 except:
#                     self.action.quantity = 0
                    
                    
#         else:
#             print("ERROR: An incorrect direction!")
    
    def market_order(self):
        self.execPrice = []
        self.execQty = []
        
        if self.action.direction == "buy":
            while self.action.quantity > 0:
                try:
                    if self.action.quantity > self.LOB.askBook.askBook_public[0][1]:
                        self.execPrice.append( self.LOB.askBook.askBook_public[0][0] )
                        self.execQty.append( self.LOB.askBook.askBook_public[0][1] )                        
                        self.action.quantity -= self.LOB.askBook.askBook_public[0][1]
                        self.LOB.update("cross", "buy", self.LOB.askBook.askBook_public[0][1])
                        self.lastPrice = self.LOB.askBook.ask

                    else:
                        self.execPrice.append( self.LOB.askBook.askBook_public[0][0] )
                        self.execQty.append( self.action.quantity )                    
                        self.LOB.update("cross", "buy", self.action.quantity)
                        self.action.quantity = 0
                        self.lastPrice = self.LOB.askBook.ask

                except:
                    self.action.quantity = 0
                    
        elif self.action.direction == "sell":
            while self.action.quantity > 0:
                try:
                    if self.action.quantity > self.LOB.bidBook.bidBook_public[0][1]:
                        self.execPrice.append( self.LOB.bidBook.bidBook_public[0][0] )
                        self.execQty.append( self.LOB.bidBook.bidBook_public[0][1] )
                        self.action.quantity -= self.LOB.bidBook.bidBook_public[0][1]
                        self.LOB.update("cross", "sell", self.LOB.bidBook.bidBook_public[0][1])
                        self.lastPrice = self.LOB.bidBook.bid
                    else:
                        self.execPrice.append( self.LOB.bidBook.bidBook_public[0][0] )
                        self.execQty.append( self.action.quantity )
                        self.LOB.update("cross", "sell", self.action.quantity)
                        self.action.quantity = 0
                        self.lastPrice = self.LOB.bidBook.bid
                except:
                    self.action.quantity = 0
                    
                    
        else:
            print("ERROR: An incorrect direction!")
                                                                            
    
    def limit_order(self):
        if self.action.direction == "buy":
            while self.action.quantity > 0 and self.action.price >= self.LOB.askBook.ask:
                if self.action.quantity > self.LOB.askBook.askBook_public[0][1]:
                    self.execPrice.append( self.LOB.askBook.askBook_public[0][0] )
                    self.execQty.append( self.LOB.askBook.askBook_public[0][1] )
                    self.action.quantity -= self.LOB.askBook.askBook_public[0][1]
                    self.LOB.update("cross", "buy", self.LOB.askBook.askBook_public[0][1])
                    self.lastPrice = self.LOB.askBook.ask

                else:
                    self.execPrice.append( self.LOB.askBook.askBook_public[0][0] )
                    self.execQty.append( self.LOB.askBook.askBook_public[0][1] )
                    self.LOB.update("cross", "buy", self.action.quantity)
                    self.action.quantity = 0
                    self.lastPrice = self.LOB.askBook.ask

            if self.action.quantity > 0:
                self.LOB.update("insert", "buy", self.action.quantity, self.action.agent, self.action.price)
                
                
        elif self.action.direction == "sell":
            while self.action.quantity>0 and self.action.price <= self.LOB.bidBook.bid:
                if self.action.quantity > self.LOB.bidBook.bidBook_public[0][1]:
                    self.execPrice.append( self.LOB.bidBook.bidBook_public[0][0] )
                    self.execQty.append( self.LOB.bidBook.bidBook_public[0][1] )
                    self.action.quantity -= self.LOB.bidBook.bidBook_public[0][1]                   
                    self.LOB.update("cross", "sell", self.LOB.bidBook.bidBook_public[0][1]) 
                    self.lastPrice = self.LOB.bidBook.bid
                else:
                    self.execPrice.append( self.LOB.bidBook.bidBook_public[0][0] )
                    self.execQty.append( self.LOB.bidBook.bidBook_public[0][1] )
                    self.LOB.update("cross", "sell", self.action.quantity)
                    self.action.quantity = 0
                    self.lastPrice = self.LOB.bidBook.bid
            if self.action.quantity>0:
                self.LOB.update("insert", "sell", self.action.quantity, self.action.agent, self.action.price)
        else:
            print("ERROR: An incorrect direction!")

    def cancel_order(self):
        if (self.action.direction == "buy") and (self.action.price <= self.LOB.bidBook.bid):
            book_loc = round((self.LOB.bidBook.bid - self.action.price)/self.tick)
            sum_vol = 0
            for info in self.LOB.bidBook.bidBook_private[book_loc]:
                if info[0] == self.action.agent:
                    sum_vol += info[1]
            if sum_vol >= self.action.quantity:
                self.LOB.update("cancel", self.action.direction, self.action.quantity, self.action.agent, self.action.price)
        if (self.action.direction == "sell") and (self.action.price >= self.LOB.askBook.ask):
            book_loc = round((self.action.price - self.LOB.askBook.ask )/self.tick)
            sum_vol = 0
            for info in self.LOB.askBook.askBook_private[book_loc]:
                if info[0] == self.action.agent:
                    sum_vol += info[1]
            if sum_vol >= self.action.quantity:
                self.LOB.update("cancel", self.action.direction, self.action.quantity, self.action.agent, self.action.price)
                                                                                     
    def CDA(self):
        if self.action.type == "market":
            self.market_order()
                
        elif self.action.type == "limit":
            self.limit_order()
                
        elif self.action.type == "cancel":
            self.cancel_order()
            
                 
        else:
            print("ERROR: An incorrect type!")
        
        