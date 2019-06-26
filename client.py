from util import *
from blockchain import *


class Account(object):
	def __init__(self,name, password, port):
		self.name = name
		self.password = password
		self.port = port

	def unlock(self):
		post("unlock", [self.password], self.port)

	def buy(self, asset, money, price, amount, timeout):
		return post("sell_asset", 	
			[			
				self.name, 	
				str(my_round(price * amount, get_asset_precision(money, self.port))), 
				money,         
				str(my_round(amount, get_asset_precision(asset, self.port))), 
				asset, 
				timeout, "false", "true"
			], self.port)

	def sell(self, asset, money, price, amount, timeout):
		return post("sell_asset", 
			[
				self.name,
				str(my_round(amount, get_asset_precision(asset, self.port))),  
				asset, 
				str(my_round(price * amount, get_asset_precision(money, self.port))),
				money, 
				timeout, "false", "true"
			], self.port)


