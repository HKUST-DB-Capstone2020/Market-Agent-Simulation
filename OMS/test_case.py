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

	def test_buy_cancel_order_less2(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 560, 9.6])
		a = OMS.bid_book[2].qty == 440
		assert a

	def test_buy_cancel_order_more(self):  
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "buy", 1560, 9.8])
		a = OMS.bid_book[0].qty == 1000
		b = int(OMS.bid*10) == 97
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
		a = OMS.ask_book[2].qty == 0
		b = int(OMS.ask*10) == 100
		assert a 
		assert b

	def test_sell_cancel_order_more2(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "cancel",  "sell", 1000, 10.0])
		print(OMS.ask_book)
		OMS.receive(["ZIagent", "cancel", "sell", 1000, 10.2])
		print(OMS.ask_book)
		a = OMS.ask_book[1].qty == 0
		b = int(OMS.ask*10) == 101
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
		b = OMS.ask_book[4].qty == 1000
		c = int(OMS.ask_book[4].price * 10) == 104
		assert a 
		assert b
		assert c

	def test_exe_less(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "market",  "sell", 300, 9.7])
		a = OMS.execPrice == [9.8]
		b = OMS.execQty == [300]
		assert a
		assert b

	def test_exe_more(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 2300, 9.7])
		a = OMS.execPrice == [9.8, 9.7]
		b = OMS.execQty == [1000, 1000]
		assert a
		assert b

	def test_trade_record(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		OMS.receive(["ZIagent", "limit",  "sell", 2300, 9.7])
		OMS.receive(["ZIagent", "market", "sell", 1300, 9.7])
		OMS.receive(["ZIagent", "market", "buy", 1400, 9.7])
		a = OMS.trade_price_record == [9.8, 9.7, 9.6, 9.5, 9.7, 10.0, 10.1]
		b = OMS.trade_vol_record == [1000, 1000, 1000, 300, 300, 1000, 100]
		assert a
		assert b

	def test_parameters(self):
		OMS = OrderManagementSystem(10.0, 9.8, 0.1, 5, 9.7)
		a = OMS.MAX_PRICE == 4560987
		b = OMS.MIN_PRICE == 0
		assert a
		assert b

	def test_limit_record(self):
		OMS = OrderManagementSystem(10.0, 9.98, 0.01, 5, 9.7)
		OMS.record("strategy")
		OMS.receive(["strategy", "limit", "sell", 2300, 9.7])
		a = OMS.strategy_record.filled_order == [['sell', 9.98, 1000], ['sell', 9.97, 1000], ['sell', 9.96, 300]]
		d = OMS.strategy_record.position == -2300
		OMS.receive(["strategy", "limit", "sell", 2300, 10.7])
		b = OMS.strategy_record.active_order[10.7] == [2300, 'sell']
		OMS.receive(["strategy", "cancel", "sell", 2300, 10.7])
		c = OMS.strategy_record.active_order == {}
		e = OMS.strategy_record.position == -2300
		assert a
		assert b
		assert c
		assert d
		assert e

	def test_market_record(self):
		OMS = OrderManagementSystem(10.0, 9.98, 0.01, 5, 9.7)
		OMS.record("strategy")
		OMS.receive(["strategy", "market", "buy", 2300, 9.7])
		OMS.receive(["ZIagent", "market", "buy", 2300, 9.7])
		a = OMS.strategy_record.filled_order == [['buy', 10.00, 1000], ['buy', 10.01, 1000], ['buy', 10.02, 300]]
		d = OMS.strategy_record.position == 2300
		OMS.receive(["strategy", "market", "sell", 1300, 10.7])
		OMS.receive(["ZIagent", "limit", "buy", 2300, 9.7])
		OMS.receive(["ZIagent", "cancel", "buy", 2300, 9.97])
		b = OMS.strategy_record.active_order == {}
		c = OMS.strategy_record.filled_order == [['buy', 10.00, 1000], ['buy', 10.01, 1000], ['buy', 10.02, 300], ['sell', 9.98, 1000], ['sell', 9.97, 300]]
		e = OMS.strategy_record.position == 1000
		assert a
		assert b
		assert c
		assert d
		assert e

	def test_market_record2(self):
		OMS = OrderManagementSystem(10.0, 9.99, 0.01, 5, 9.7)
		OMS.record("strategy")
		OMS.receive(["strategy", "limit", "buy", 1200, 10.0])
		a = OMS.strategy_record.active_order == {10.0: [200, 'buy']}
		b = OMS.strategy_record.position == 1000
		c = OMS.strategy_record.filled_order == [['buy', 10.0, 1000]]
		OMS.receive(["strategy", "market", "sell", 200, 9.7])
		d = OMS.strategy_record.active_order == {}
		e = OMS.strategy_record.position == 1000
		f = OMS.strategy_record.filled_order == [['buy', 10.0, 1000], ['sell', 10.0, 200], ['buy', 10.0, 200]]
		assert a
		assert b
		assert c
		assert d
		assert e
		assert f

	def test_market_record3(self):
		OMS = OrderManagementSystem(10.0, 9.99, 0.01, 5, 9.7)
		OMS.record("strategy")
		OMS.receive(["strategy", "limit", "buy", 1200, 10.0])
		a = OMS.strategy_record.active_order == {10.0: [200, 'buy']}
		b = OMS.strategy_record.position == 1000
		c = OMS.strategy_record.filled_order == [['buy', 10.0, 1000]]
		OMS.receive(["ZIagent", "market", "sell", 200, 9.7])
		d = OMS.strategy_record.active_order == {}
		e = OMS.strategy_record.position == 1200
		f = OMS.strategy_record.filled_order == [['buy', 10.0, 1000], ['buy', 10.0, 200]]
		assert a
		assert b
		assert c
		assert d
		assert e
		assert f

if __name__ == "__main__":
	pytest.main()






