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
        self.__LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        self.ask = self.__LOB.askBook.nearPrice
        self.bid = self.__LOB.bidBook.nearPrice
        self.ask_book = self.__LOB.askBook.Book_public
        self.bid_book = self.__LOB.bidBook.Book_public
        self.tick = tick
        self.lastPrice = lastPrice  # prevailing market price
        self.trade_price_record = []
        self.trade_vol_record = []
        self.execPrice = []
        self.execQty = []

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


    def market_order(self):
        self.execPrice = []
        self.execQty = []

        if self.action.direction == "buy":
            while self.action.quantity > 0:
                try:
                    if self.action.quantity > self.__LOB.askBook.Book_public[0].qty:
                        self.execPrice.append(self.__LOB.askBook.Book_public[0].price)
                        self.execQty.append(self.__LOB.askBook.Book_public[0].qty)
                        self.action.quantity -= self.__LOB.askBook.Book_public[0].qty
                        self.trade_price_record.append(self.__LOB.askBook.nearPrice)
                        self.trade_vol_record.append(self.__LOB.askBook.Book_public[0].qty)
                        self.__LOB.update("cross", "buy", self.__LOB.askBook.Book_public[0].qty)

                    else:
                        self.execPrice.append(self.__LOB.askBook.Book_public[0].price)
                        self.execQty.append(self.action.quantity)
                        self.trade_price_record.append(self.__LOB.askBook.nearPrice)
                        self.trade_vol_record.append(self.action.quantity)
                        self.__LOB.update("cross", "buy", self.action.quantity)
                        self.action.quantity = 0

                except:
                    self.action.quantity = 0
                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public

        elif self.action.direction == "sell":
            while self.action.quantity > 0:
                try:
                    if self.action.quantity > self.__LOB.bidBook.Book_public[0].qty:
                        self.execPrice.append(self.__LOB.bidBook.Book_public[0].price)
                        self.execQty.append(self.__LOB.bidBook.Book_public[0].qty)
                        self.action.quantity -= self.__LOB.bidBook.Book_public[0].qty
                        self.trade_price_record.append(self.__LOB.bidBook.Book_public[0].price)
                        self.trade_vol_record.append(self.__LOB.bidBook.Book_public[0].qty)
                        self.__LOB.update("cross", "sell", self.__LOB.bidBook.Book_public[0].qty)

                    else:
                        self.execPrice.append(self.__LOB.bidBook.Book_public[0].price)
                        self.execQty.append(self.action.quantity)
                        self.trade_price_record.append(self.__LOB.bidBook.Book_public[0].price)
                        self.trade_vol_record.append(self.action.quantity)
                        self.__LOB.update("cross", "sell", self.action.quantity)
                        self.action.quantity = 0
                except:
                    self.action.quantity = 0
                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public

        else:
            print("ERROR: An incorrect direction!")

    def limit_order(self):
        if self.action.direction == "buy":
            while self.action.quantity > 0 and self.action.price >= self.__LOB.askBook.nearPrice:
                if self.action.quantity > self.__LOB.askBook.Book_public[0].qty:
                    self.execPrice.append(self.__LOB.askBook.Book_public[0].price)
                    self.execQty.append(self.__LOB.askBook.Book_public[0].qty)
                    self.action.quantity -= self.__LOB.askBook.Book_public[0].qty
                    self.trade_price_record.append(self.__LOB.askBook.nearPrice)
                    self.trade_vol_record.append(self.__LOB.askBook.Book_public[0].qty)
                    self.__LOB.update("cross", "buy", self.__LOB.askBook.Book_public[0].qty)

                else:
                    self.execPrice.append(self.__LOB.askBook.Book_public[0].price)
                    self.execQty.append(self.__LOB.askBook.Book_public[0].qty)
                    self.trade_price_record.append(self.__LOB.askBook.nearPrice)
                    self.trade_vol_record.append(self.action.quantity)
                    self.__LOB.update("cross", "buy", self.action.quantity)
                    self.action.quantity = 0

                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public

            if self.action.quantity > 0:
                self.__LOB.update("insert", "buy", self.action.quantity, self.action.agent, self.action.price)
                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public

        elif self.action.direction == "sell":
            while self.action.quantity > 0 and self.action.price <= self.__LOB.bidBook.nearPrice:
                if self.action.quantity > self.__LOB.bidBook.Book_public[0].qty:
                    self.execPrice.append(self.__LOB.bidBook.Book_public[0].price)
                    self.execQty.append(self.__LOB.bidBook.Book_public[0].qty)
                    self.action.quantity -= self.__LOB.bidBook.Book_public[0].qty
                    self.trade_price_record.append(self.__LOB.bidBook.Book_public[0].price)
                    self.trade_vol_record.append(self.__LOB.bidBook.Book_public[0].qty)
                    self.__LOB.update("cross", "sell", self.__LOB.bidBook.Book_public[0].qty)
                else:
                    self.execPrice.append(self.__LOB.bidBook.Book_public[0].price)
                    self.execQty.append(self.__LOB.bidBook.Book_public[0].qty)
                    self.trade_price_record.append(self.__LOB.bidBook.Book_public[0].price)
                    self.trade_vol_record.append(self.action.quantity)
                    self.__LOB.update("cross", "sell", self.action.quantity)
                    self.action.quantity = 0
                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public
            if self.action.quantity > 0:
                self.__LOB.update("insert", "sell", self.action.quantity, self.action.agent, self.action.price)
                self.ask = self.__LOB.askBook.nearPrice
                self.bid = self.__LOB.bidBook.nearPrice
                self.ask_book = self.__LOB.askBook.Book_public
                self.bid_book = self.__LOB.bidBook.Book_public
        else:
            print("ERROR: An incorrect direction!")

    def cancel_order(self):
        if (self.action.direction == "buy") and (self.action.price <= self.__LOB.bidBook.nearPrice):
            book_loc = round((self.__LOB.bidBook.nearPrice - self.action.price) / self.tick)
            if book_loc < len(self.__LOB.bidBook.Book_public):
                sum_vol = 0
                for info in self.__LOB.bidBook.Book_private[book_loc]:
                    if info[0] == self.action.agent:
                        sum_vol += info[1]
                if sum_vol >= self.action.quantity:
                    self.__LOB.update("cancel", self.action.direction, self.action.quantity, self.action.agent,
                                    self.action.price)
                    self.ask = self.__LOB.askBook.nearPrice
                    self.bid = self.__LOB.bidBook.nearPrice
                    self.ask_book = self.__LOB.askBook.Book_public
                    self.bid_book = self.__LOB.bidBook.Book_public
        if (self.action.direction == "sell") and (self.action.price >= self.__LOB.askBook.nearPrice):
            book_loc = round((self.action.price - self.__LOB.askBook.nearPrice) / self.tick)
            if book_loc < len(self.__LOB.askBook.Book_public):
                sum_vol = 0
                for info in self.__LOB.askBook.Book_private[book_loc]:
                    if info[0] == self.action.agent:
                        sum_vol += info[1]
                if sum_vol >= self.action.quantity:
                    self.__LOB.update("cancel", self.action.direction, self.action.quantity, self.action.agent,
                                    self.action.price)
                    self.ask = self.__LOB.askBook.nearPrice
                    self.bid = self.__LOB.bidBook.nearPrice
                    self.ask_book = self.__LOB.askBook.Book_public
                    self.bid_book = self.__LOB.bidBook.Book_public

    def CDA(self):
        if self.action.type == "market":
            self.market_order()

        elif self.action.type == "limit":
            self.limit_order()

        elif self.action.type == "cancel":
            self.cancel_order()


        else:
            print("ERROR: An incorrect type!")

