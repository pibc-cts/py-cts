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

wallet_port = '8093'
account_name = 'init3'
password = 'gg123123'

one_year = 3600 * 24 * 365
buy_order_cny_limit = 1000
sell_order_cts_limit = 1000
limit_order ='10'
sell_order_step_precision =  [1.01, 1.03, 1.05, 1.07, 1.09]
buy_order_step_precision =   [0.99, 0.97, 0.95, 0.93, 0.91]

##################### start ############################

account = client.Account(account_name, password, wallet_port)
account.unlock()


cny_settlement_price = 0
buy_price_standard = 0
sell_price_standard = 0


order_book = market.get_order_book('CNY', 'CTS', 10, wallet_port)
#print(order_book)
cny_settlement_price = market.get_cny_settlement_price(wallet_port)
print(cny_settlement_price)

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
bqg=[0,0,0,0,0,0,0,0,0,0]
sqg=[0,0,0,0,0,0,0,0,0,0]
bpg=[0,0,0,0,0,0,0,0,0,0]
spg=[0,0,0,0,0,0,0,0,0,0]
bb=[0,0,0,0,0,0,0,0,0,0]
sb=[0,0,0,0,0,0,0,0,0,0]
bid_quote = 0.0
ask_quote =0.0
sum_bid_price=0.0
sum_ask_price=0.0
cny_math_order=0.0

for i in range(0, 10):
	bpg[i]=price = float(order_book['bids'][i]['price'])
	#print("price =",price)
	base = float(order_book['bids'][i]['base'])
	bb[i]=bb[i-1]+base
	#print("base=",base)	
	bid_quote +=float(order_book['bids'][i]['quote'])
	bqg[i]=bid_quote
	#print("sum_bid_quote=",bid_quote)
	#step = analyse_buy_price_step(price, buy_price_standard, buy_order_step_precision)
	#if step != -1:
		#buy_group[step] = buy_group[step] + base
		#print(buy_group[step])

for i in range(0, 10):
	spg[i]=price = float(order_book['asks'][i]['price'])
	quote= float(order_book['asks'][i]['quote'])
	base = float(order_book['asks'][i]['base'])
	sb[i]=sb[i-1]+base
	#print(quote)
	ask_quote+=quote
	sqg[i]=ask_quote
	#print("sum_ask_quote",ask_quote)

print("sum_bid_quote=",bid_quote)
print("sum_ask_quote=",ask_quote)
print("",bqg,"\n",sqg,"\n",bpg,"\n",spg,"\n",bb,"\n",sb)


if bid_quote > ask_quote :
	print("买单数量多过卖单，重新取买单数量")
	bid_quote_1=0.0
	l_quote=0
	for i in range(0, 10):
		price = float(order_book['bids'][i]['price'])
		quote= float(order_book['bids'][i]['quote'])
		#print(quote)
		print(i)
		bid_quote_1+=quote
		print(bid_quote_1)
		if bid_quote_1>=ask_quote:
			l_quote=i
			print(l_quote)
			if l_quote ==0:
					sum_bid_price=price*ask_quote
			else: sum_bid_base=bpg[l_quote-1]=(bqg[l_quote-1]-sid_quote)+bb[l_quote-1]
			print(sum_bid_base)
			print(sb[9])
			cny_math_order=sb[9]/sum_bid_base
		break
	
elif bid_quote < ask_quote:
	print("卖单数量多过买单，重新取卖单数量")
	ask_quote_1=0.0
	l_quote=0
	for i in range(0, 10):
		price = float(order_book['asks'][i]['price'])
		quote= float(order_book['asks'][i]['quote'])
		#print(quote)
		print(i)
		ask_quote_1+=quote
		print(ask_quote_1)
		if ask_quote_1>=bid_quote:
			l_quote=i
			print(l_quote)
			if l_quote ==0:
				sum_ask_base=price*(bid_quote)
			else: sum_ask_base=spg[l_quote-1]=(sqg[l_quote-1]-bid_quote)+sb[l_quote-1]
			print(sum_ask_base)
			print(bb[9])
			cny_math_order=bb[9]/sum_ask_base
			print("市场买卖各10单取最低深度计算出来的CTS喂价:",cny_math_order)
		break
	
else :
	print("买卖单请求数量相等")
#print(l_quote)

	#step = analyse_sell_price_step(price, sell_price_standard, sell_order_step_precision)
	#if step != -1:
		#sell_group[step] = sell_group[step] + quote


	
#print("buy_group ",buy_group)
#print("sell_group ",sell_group)

'''
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

'''
