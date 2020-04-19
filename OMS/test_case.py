import pytest
from OMS import OrderManagementSystem



class TestClass:  
	def test_buy_limit_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "buy", 100, 9.7])
		a = OMS.LOB.bidBook.bidBook_public[1][1] == 1100
		assert a 

	def test_buy_limit_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "buy", 1500, 10])
		a = int(OMS.LOB.askBook.ask*10) == 101
		b = OMS.LOB.askBook.askBook_public[0][1] == 1000
		c = int(OMS.LOB.bidBook.bid*10) == 100
		d = OMS.LOB.bidBook.bidBook_public[0][1] == 500
		assert a 
		assert b
		assert c
		assert d

	def test_sell_limit_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 1000, 9.7])
		a = OMS.LOB.bidBook.bidBook_public[0][1] == 1000
		b = int(OMS.LOB.bidBook.bid*10) == 97
		assert a 
		assert b

  
	def test_sell_limit_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 2500, 9.7])
		a = int(OMS.LOB.bidBook.bid*10) == 96
		b = int(OMS.LOB.askBook.ask*10) == 97
		c = OMS.LOB.askBook.askBook_public[0][1] == 500
		d = OMS.LOB.askBook.askBook_public[1][1] == 0
		e = OMS.LOB.askBook.askBook_public[2][1] == 0
		f = OMS.LOB.askBook.askBook_public[3][1] == 1000
		assert a 
		assert b
		assert c
		assert d
		assert e
		assert f

	def test_sell_market_order(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "sell", 1560, 0])
		a = OMS.LOB.bidBook.bidBook_public[0][1] == 440
		b = int(OMS.LOB.bidBook.bid*10) == 97
		assert a 
		assert b

	def test_buy_market_order(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "buy", 1560, 0])
		a = OMS.LOB.askBook.askBook_public[0][1] == 440
		b = int(OMS.LOB.askBook.ask*10) == 101
		assert a 
		assert b

	def test_buy_cancel_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 560, 9.7])
		a = OMS.LOB.bidBook.bidBook_public[1][1] == 440
		assert a 

	def test_buy_cancel_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 1560, 9.8])
		a = OMS.LOB.bidBook.bidBook_public[0][1] == 1000
		b = int(OMS.LOB.bidBook.bid*10) == 98
		assert a 
		assert b

	def test_sell_cancel_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "sell", 560, 10.2])
		a = OMS.LOB.askBook.askBook_public[2][1] == 440
		assert a 

	def test_sell_cancel_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "sell", 1560, 10.2])
		a = OMS.LOB.askBook.askBook_public[0][1] == 1000
		b = int(OMS.LOB.askBook.ask*10) == 100
		assert a 
		assert b


	def test_huge_buy_limit_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 6000, 9.7])
		a = OMS.LOB.askBook.askBook_public[0][1] == 4000
		b = int(OMS.LOB.askBook.ask*10) == 97
		c = OMS.LOB.bidBook.bidBook_public[0][1] == 1000
		d = int(OMS.LOB.bidBook.bid*10) == 96
		e = OMS.LOB.askBook.askBook_public[1][1] == 0
		f = int(OMS.LOB.askBook.askBook_public[1][0]*10) == 98
		g = OMS.LOB.askBook.askBook_public[2][1] == 0
		h = int(OMS.LOB.askBook.askBook_public[2][0]*10) == 99
		assert a 
		assert b
		assert c
		assert d
		assert e
		assert f
		assert g
		assert h

	def test_huge_sell_limit_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "buy", 6000, 10.4])
		a = OMS.LOB.bidBook.bidBook_public[0][1] == 1000
		b = int(OMS.LOB.bidBook.bid*10) == 104
		c = OMS.LOB.bidBook.bidBook_public[1][1] == 0
		d = int(OMS.LOB.bidBook.bidBook_public[1][0]*10) == 103
		e = int(OMS.LOB.askBook.ask) == 4560987
		assert a 
		assert b
		assert c
		assert d
		assert e


	def test_huge_buy_market_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "buy", 7000, 10.4])
		a = int(OMS.LOB.askBook.ask) == 4560987
		b = OMS.LOB.bidBook.bidBook_public[0][1] == 1000
		c = int(OMS.LOB.bidBook.bid*10) == 98
		assert a 
		assert b
		assert c

	def test_huge_sell_market_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "sell", 7000, 10.4])
		a = int(OMS.LOB.bidBook.bid) == 0
		b = OMS.LOB.askBook.askBook_public[0][1] == 1000
		c = int(OMS.LOB.askBook.ask*10) == 100
		assert a 
		assert b
		assert c







