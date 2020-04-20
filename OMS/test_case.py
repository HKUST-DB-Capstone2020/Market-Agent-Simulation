import pytest
from OMS import OrderManagementSystem


class TestClass:  
	def test_buy_limit_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "buy", 100, 9.7])
		a = OMS.bid_book[1].qty == 1100
		assert a 

	def test_buy_limit_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "buy", 1500, 10])
		a = int(OMS.ask*10) == 101
		b = OMS.ask_book[0].qty == 1000
		c = int(OMS.bid*10) == 100
		d = OMS.bid_book[0].qty == 500
		assert a 
		assert b
		assert c
		assert d

	def test_sell_limit_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 1000, 9.7])
		a = OMS.bid_book[0].qty == 1000
		b = int(OMS.bid*10) == 97
		assert a 
		assert b

  
	def test_sell_limit_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 2500, 9.7])
		a = int(OMS.bid*10) == 96
		b = int(OMS.ask*10) == 97
		c = OMS.ask_book[0].qty == 500
		d = OMS.ask_book[1].qty == 0
		e = OMS.ask_book[2].qty == 0
		f = OMS.ask_book[3].qty == 1000
		assert a 
		assert b
		assert c
		assert d
		assert e
		assert f

	def test_sell_market_order(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "sell", 1560, 0])
		a = OMS.bid_book[0].qty == 440
		b = int(OMS.bid*10) == 97
		assert a 
		assert b

	def test_buy_market_order(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "buy", 1560, 0])
		a = OMS.ask_book[0].qty == 440
		b = int(OMS.ask*10) == 101
		assert a 
		assert b

	def test_buy_cancel_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 560, 9.7])
		a = OMS.bid_book[1].qty == 440
		assert a 

	def test_buy_cancel_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 1560, 9.8])
		a = OMS.bid_book[0].qty == 1000
		b = int(OMS.bid*10) == 98
		assert a 
		assert b

	def test_buy_cancel_order_inexist(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 1560, 9.0])
		a = OMS.bid_book[0].qty == 1000
		b = int(OMS.bid*10) == 98
		assert a
		assert b

	def test_sell_cancel_order_less(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "sell", 560, 10.2])
		a = OMS.ask_book[2].qty == 440
		assert a 

	def test_sell_cancel_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "sell", 1560, 10.2])
		a = OMS.ask_book[0].qty == 1000
		b = int(OMS.ask*10) == 100
		assert a 
		assert b


	def test_huge_buy_limit_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 6000, 9.7])
		a = OMS.ask_book[0].qty == 4000
		b = int(OMS.ask*10) == 97
		c = OMS.bid_book[0].qty == 1000
		d = int(OMS.bid*10) == 96
		e = OMS.ask_book[1].qty == 0
		f = int(OMS.ask_book[1].price*10) == 98
		g = OMS.ask_book[2].qty == 0
		h = int(OMS.ask_book[2].price*10) == 99
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
		a = OMS.bid_book[0].qty == 1000
		b = int(OMS.bid*10) == 104
		c = OMS.bid_book[1].qty == 0
		d = int(OMS.bid_book[1].price*10) == 103
		e = int(OMS.ask) == 4560987
		assert a 
		assert b
		assert c
		assert d
		assert e


	def test_huge_buy_market_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "buy", 7000, 10.4])
		a = int(OMS.ask) == 4560987
		b = OMS.bid_book[0].qty == 1000
		c = int(OMS.bid*10) == 98
		assert a 
		assert b
		assert c

	def test_huge_sell_market_order_more(self): 
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "sell", 7000, 10.4])
		a = int(OMS.bid) == 0
		b = OMS.ask_book[0].qty == 1000
		c = int(OMS.ask*10) == 100
		assert a 
		assert b
		assert c

if __name__ == "__main__":
	pytest.main()






