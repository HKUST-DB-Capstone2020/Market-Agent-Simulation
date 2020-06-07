import os
# import pandas as pd
import sys
sys.path.append(os.path.pardir)
from LOB.LOB import LimitOrderBook

class action():
    def __init__(self, input_action):
        self.agent, self.type, self.direction, self.quantity, self.price = input_action

class strategy_record:
    def __init__(self, strategy_name = "strategy", min_volume_unit = 1, if_log = False):
        self.strategy_name = strategy_name if strategy_name else "strategy"
        self.active_order = {}
        self.filled_order = []
        self.position = 0
        self.min_volume_unit = min_volume_unit

    def create_order(self, action):
        if action.price not in self.active_order.keys():
            self.active_order[action.price] = [action.quantity, action.direction]
        else:
            if action.direction == self.active_order[action.price][1]:
                self.active_order[action.price][0] += action.quantity
            else:
                print("Create order record error! There is conflict about order direction.")

    def match_order(self, info, price, direction):
        for order_record in info:
            if order_record.ID == self.strategy_name:
                if price in self.active_order.keys():
                    if (direction == "buy") and (self.active_order[price][-1] == "sell"):
                        self.active_order[price][0] -= order_record.qty
                        self.position -= order_record.qty
                        self.filled_order.append([self.active_order[price][-1], price, order_record.qty])
                        if abs(self.active_order[price][0]) < 0.5 *self.min_volume_unit:
                            del self.active_order[price]
                    elif (direction == "sell") and (self.active_order[price][-1] == "buy"):
                        self.active_order[price][0] -= order_record.qty
                        self.position += order_record.qty
                        self.filled_order.append([self.active_order[price][-1], price, order_record.qty])
                        if abs(self.active_order[price][0]) < 0.5 *self.min_volume_unit:
                            del self.active_order[price]
                else:
                    "Record error. No such price record!"


    def match_market_order(self, action, volume, price):
        self.filled_order.append([action.direction, price, volume])
        if action.direction == "buy":
            self.position += volume
        else:
            self.position -= volume

    def cancel_order(self, action, volume):
        if action.price in self.active_order.keys():
            if action.direction == self.active_order[action.price][1]:
                diff_volume = self.active_order[action.price][0] - volume
                if diff_volume > 0.5*self.min_volume_unit:
                    self.active_order[action.price][0] -= action.quantity
                else:
                    self.active_order.pop(action.price)
            else:
                print("Create order record error! There is conflict about order direction.")

class OrderManagementSystem:
    def __init__(self, ask, bid, tick, orderLevel, lastPrice, init_qty = 1000):
        self.__LOB = LimitOrderBook(ask, bid, tick, orderLevel, init_qty)
        self.ask = self.__LOB.askBook.nearPrice
        self.bid = self.__LOB.bidBook.nearPrice
        self.ask_book = self.__LOB.askBook.Book_public
        self.bid_book = self.__LOB.bidBook.Book_public
        self.tick = tick
        self.trade_price_record = []
        self.trade_vol_record = []
        self.MAX_PRICE = 4560987
        self.MIN_PRICE = 0
        self.is_record = False
        self.cross_info = None

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
        self.cross_info = None
        trade_vol = min(self.action.quantity, self.__another_book.Book_public[0].qty)
        trade_price = self.__another_book.Book_public[0].price
        self.execPrice.append(trade_price)
        self.execQty.append(trade_vol)
        self.action.quantity -= trade_vol
        self.trade_price_record.append(trade_price)
        self.trade_vol_record.append(trade_vol)
        self.cross_info = self.__LOB.update("cross", self.action.direction, trade_vol)
        self.update_order_book()
        self.trade_vol = trade_vol
        self.trade_price = trade_price

    def match_order(self):
        while self.action.quantity > 0 and len(self.__another_book.Book_public) > 0:
            if (self.action.type == "limit") and \
                    (self.__para * self.action.price < self.__para * self.__another_book.nearPrice ):
                break
            self.exe_order()
            if self.is_record:
                if self.action.agent == self.strategy_record.strategy_name:
                    self.strategy_record.match_market_order(self.action, self.trade_vol, self.trade_price )
                self.strategy_record.match_order(self.cross_info, self.trade_price, self.action.direction)
        if self.action.type == "market":
            self.action.quantity = 0
        if self.action.quantity > 0:
            self.__LOB.update("insert", self.action.direction, self.action.quantity, self.action.agent, self.action.price)
            if self.is_record and self.action.agent == self.strategy_record.strategy_name:
                self.strategy_record.create_order(self.action)
        self.update_order_book()

    def cancel_order(self):
        sum_vol = 0
        if self.__para * self.action.price <= self.__para * self.__book.nearPrice:
            book_loc = self.__para*int(round((self.__book.nearPrice - self.action.price) / self.tick))
            if book_loc < len(self.__book.Book_public):
                for info in self.__book.Book_private[book_loc]:
                    if info[0] == self.action.agent:
                        sum_vol += info[1]
                self.__LOB.update("cancel", self.action.direction, min(self.action.quantity, sum_vol),
                                  self.action.agent,
                                  self.action.price)
                if self.is_record and self.action.agent == self.strategy_record.strategy_name:
                    self.strategy_record.cancel_order(self.action, min(self.action.quantity, sum_vol))
                self.update_order_book()

    def record(self, strategy_name = "strategy"):
        self.strategy_record = strategy_record(strategy_name, min_volume_unit = self.tick)
        self.is_record = True

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
