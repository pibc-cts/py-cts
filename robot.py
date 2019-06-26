import client
import pdb
import market
import blockchain

######################## function ##########################
def is_a_bigger_b(a, b):
	if (a > b) and abs(a - b) > 0.0001:
		return True
	else:
		return False
def is_a_bigger_equ_b(a, b):
	if (a > b) or abs(a - b) < 0.0001:
		return True
	else:
		return False


def is_a_smaller_b(a, b):
	if (b > a) and abs(b - a) > 0.0001:
		return True
	else:
		return False

def is_a_smaller_equ_b(a, b):
	if (b > a) or abs(b - a) < 0.0001:
		return True
	else:
		return False


def analyse_buy_price_step(price , buy_standard, step_precision):
	if is_a_bigger_equ_b(price, buy_standard * step_precision[0]) :
		return 0
	elif is_a_bigger_b(buy_standard * step_precision[0], price) and is_a_bigger_equ_b(price, buy_standard * step_precision[1]):
		return 1
	elif is_a_bigger_b(buy_standard * step_precision[1], price) and is_a_bigger_equ_b(price, buy_standard * step_precision[2]):
		return 2
	elif is_a_bigger_b(buy_standard * step_precision[2], price) and is_a_bigger_equ_b(price, buy_standard * step_precision[3]):
		return 3
	elif is_a_bigger_b(buy_standard * step_precision[3], price) and is_a_bigger_equ_b(price, buy_standard * step_precision[4]):
		return 4
	else:
		return -1

def analyse_sell_price_step(price, sell_standard, step_precision):
	if is_a_smaller_equ_b(price, sell_standard * step_precision[0]):
		return 0
	elif is_a_smaller_b(sell_standard * step_precision[0], price) and is_a_smaller_equ_b(price, sell_standard * step_precision[1]):
		return 1
	elif is_a_smaller_b(sell_standard * step_precision[1], price) and is_a_smaller_equ_b(price, sell_standard * step_precision[2]):
		return 2
	elif is_a_smaller_b(sell_standard * step_precision[2], price) and is_a_smaller_equ_b(price, sell_standard * step_precision[3]):
		return 3
	elif is_a_smaller_b(sell_standard * step_precision[3], price) and is_a_smaller_equ_b(price, sell_standard * step_precision[4]):
		return 4
	else:
		return -1
	

#################### parameter ##########################

wallet_port = '8090'
account_name = 'account_name'
password = 'password'

one_year = 3600 * 24 * 365
buy_order_cny_limit = 1000
sell_order_cts_limit = 1000
sell_order_step_precision =  [1.01, 1.03, 1.05, 1.07, 1.09]
buy_order_step_precision =   [0.99, 0.97, 0.95, 0.93, 0.91]

##################### start ############################

account = client.Account(account_name, password, wallet_port)
account.unlock()


cny_settlement_price = 0
buy_price_standard = 0
sell_price_standard = 0


order_book = market.get_order_book('CNY', 'CTS', 50, wallet_port)
if order_book['bids'] == [] and order_book['asks'] == []:
	cny_settlement_price = market.get_cny_settlement_price(wallet_port)
	buy_price_standard = cny_settlement_price * 0.99
	sell_price_standard = cny_settlement_price * 1.01

elif order_book['bids'] and order_book['asks'] == []:
	buy_price_standard = float(order_book['bids'][0]['price'])
	sell_price_standard = buy_price_standard * 1.01

elif order_book['bids'] == [] and order_book['asks']:
	sell_price_standard = float(order_book['asks'][0]['price'])
	buy_price_standard = sell_price_standard * 0.99

elif order_book['bids'] and order_book['asks']:
	buy_price_standard = float(order_book['bids'][0]['price'])
	sell_price_standard = float(order_book['asks'][0]['price'])

if buy_price_standard == 0 or sell_price_standard == 0:
	print("Error: Can Not Get Price Standard")
	exit

buy_group =  [0, 0, 0, 0, 0]
sell_group = [0, 0, 0, 0, 0]

for i in range(0, len(order_book['bids'])):
	price = float(order_book['bids'][i]['price'])
	base = float(order_book['bids'][i]['base'])
	step = analyse_buy_price_step(price, buy_price_standard, buy_order_step_precision)
	if step != -1:
		buy_group[step] = buy_group[step] + base

for i in range(0, len(order_book['asks'])):
	price = float(order_book['asks'][i]['price'])
	quote = float(order_book['asks'][i]['quote'])
	step = analyse_sell_price_step(price, sell_price_standard, sell_order_step_precision)
	if step != -1:
		sell_group[step] = sell_group[step] + quote



	
print("buy_group ",buy_group)
print("sell_group ",sell_group)


buy_order_total = 0
for i in range(0, len(buy_group)):
	# buy order compare with cny
	buy_order_total = buy_order_total + buy_group[i]
	if buy_order_total > 5 * buy_order_cny_limit:
		print("We got enought buy_order_total, no need to buy")
		break
	if is_a_smaller_b(buy_group[i], buy_order_cny_limit):
		new_order_cny_amount = buy_order_cny_limit - buy_group[i]
		price = buy_price_standard * buy_order_step_precision[i]
		new_order_cts_amount = new_order_cny_amount / price
		print("buy {} CTS at price {}".format(new_order_cts_amount, price))
		account.buy('CTS', 'CNY', price, new_order_cts_amount, one_year)

sell_order_total = 0
for i in range(0, len(sell_group)):
	# sell order compare with cts
	sell_order_total = sell_order_total + sell_group[i]
	if sell_order_total > 5 * sell_order_cts_limit:
		print("We got enought sell_order_total, no need to sell")
		break
	if is_a_smaller_b(sell_group[i], sell_order_cts_limit):
		new_order_cts_amount = sell_order_cts_limit - sell_group[i]
		price = sell_price_standard * sell_order_step_precision[i]
		print("sell {} CTS at price {}".format(new_order_cts_amount, price))
		account.sell('CTS', 'CNY', price, new_order_cts_amount, one_year) 


print("buy")
for i in range(0, len(buy_order_step_precision)):
	print(buy_price_standard * buy_order_step_precision[i])

print("sell")
for i in range(0, len(sell_order_step_precision)):
	print(sell_price_standard * sell_order_step_precision[i])
