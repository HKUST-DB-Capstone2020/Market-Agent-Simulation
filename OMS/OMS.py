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
        self.__LOB = LimitOrderBook(ask, bid, tick, orderLevel)
        self.ask = self.__LOB.askBook.nearPrice
        self.bid = self.__LOB.bidBook.nearPrice
        self.ask_book = self.__LOB.askBook.Book_public
        self.bid_book = self.__LOB.bidBook.Book_public
        self.tick = tick
        self.trade_price_record = []
        self.trade_vol_record = []
        self.max_price = 4560987
        self.min_price = 0

    def init_book(self):
        if self.action.direction == "buy":
            self.__para = 1
            self.__book = self.__LOB.bidBook
            self.__another_book = self.__LOB.askBook
        else:
            self.__para = -1
            self.__book = self.__LOB.askBook
            self.__another_book = self.__LOB.bidBook

    def receive(self, agent_action):
        self.execPrice = []
        self.execQty = []
        self.action = action(agent_action)
        self.CDA()

    def update_order_book(self):
        self.ask = self.__LOB.askBook.nearPrice
        self.bid = self.__LOB.bidBook.nearPrice
        self.ask_book = self.__LOB.askBook.Book_public
        self.bid_book = self.__LOB.bidBook.Book_public

    def exe_order(self):
        trade_vol = min(self.action.quantity, self.__another_book.Book_public[0].qty)
        trade_price = self.__another_book.Book_public[0].price
        self.execPrice.append(trade_price)
        self.execQty.append(trade_vol)
        self.action.quantity -= trade_vol
        self.trade_price_record.append(trade_price)
        self.trade_vol_record.append(trade_vol)
        self.__LOB.update("cross", self.action.direction, trade_vol)
        self.update_order_book()

    def match_order(self):
        while self.action.quantity > 0 and len(self.__another_book.Book_public) > 0:
            if (self.action.type == "limit") and \
                    (self.__para * self.action.price < self.__para * self.__another_book.nearPrice ):
                break
            self.exe_order()
        if self.action.type == "market":
            self.action.quantity = 0
        if self.action.quantity > 0:
            self.__LOB.update("insert", self.action.direction, self.action.quantity, self.action.agent, self.action.price)
        self.update_order_book()

    def cancel_order(self):
        sum_vol = 0
        if self.__para * self.action.price <= self.__para * self.__book.nearPrice:
            book_loc = int(round((self.__book.nearPrice - self.action.price) / self.tick))
            if book_loc < len(self.__book.Book_public):
                for info in self.__book.Book_private[book_loc]:
                    if info[0] == self.action.agent:
                        sum_vol += info[1]
                self.__LOB.update("cancel", self.action.direction, min(self.action.quantity, sum_vol),
                                  self.action.agent,
                                  self.action.price)
                self.update_order_book()

    def CDA(self):
        if self.action.direction in ["buy", "sell"]:
            self.init_book()
            if self.action.type in ["market", "limit"]:
                self.match_order()
            elif self.action.type == "cancel":
                self.cancel_order()
            else:
                print("ERROR: An incorrect type!")
        else:
            print("ERROR: An incorrect direction!")
