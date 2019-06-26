'''
file: cny_feedprice.py
author: CTS
description:
	cny_feedprice.py is a demo for feeding CNY's feed price. It link to one cli_wallet
by rpc port, and send all of the comand by cli_wallet.

Usage:
	Modify the script by your own information:

wallet_port:    The rpc port which cli_wallet opened for script
account_name:   Account name of yours, which must be in the cli_wallet
password:       The password of cli_wallet, not the account priv key.
'''

import client
import pdb
import market


def publish_feedprice(feed_price, wallet_port):
	bts_amount = 100
	cny_amount = bts_amount * feed_price
	ret =market.publish_cny_feed_price(account_name, bts_amount * 100000, cny_amount * 10000, wallet_port)
	print(ret)

########## start to change#########
## change port to like  cli_wallet -r ******:8093
wallet_port = '8093'
## change to the name of your witness
account_name = 'rmb'
## change to the password of your wallet
password = 'T456827cts'
##change to the price which you want to feed  0.65 (cst/cny).
feed_price = 0.55324
#####finish and run it (python3 cny_feedprice.py) in its dir / or other way

account = client.Account(account_name, password, wallet_port)
account.unlock()


# get feed price by buy order price
order_book = market.get_order_book('CNY', 'CTS', 2, wallet_port)
buy = order_book['bids']

if buy == []:
	print("No buy order found, feed_price is ", feed_price)
else:
	feed_price = float(buy[0]['price']) * 1.1
	print("found buy order, 1.1 x buy_order is  ", feed_price)

try:

	old_feed_price = market.get_cny_settlement_price(wallet_port)
except :
	old_feed_price = feed_price

feed_price = old_feed_price * 0.9 + feed_price * 0.1

if buy != []:
	if feed_price < float(buy[0]['price']):
		feed_price = loat(buy[0]['price']) * 1.02
		print("fix feed price to buy price + 2%")

print("feed price version 2 : ", feed_price)

publish_feedprice(feed_price, wallet_port)
