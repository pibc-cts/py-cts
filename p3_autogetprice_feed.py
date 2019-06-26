import client
import pdb
import market
import blockchain

def publish_feedprice(account_name, feed_price, wallet_port):
        bts_amount = 100
        cny_amount = bts_amount * feed_price
        ret =market.publish_cny_feed_price(account_name, bts_amount * 100000, cny_amount * 10000, wallet_port)
        print(ret)



#################### parameter ##########################

wallet_port = '8093'
account_name = 'init3'
password = 'gg123123'

limit_order ='50'
#limit_order =input("请输入取市场单数量，过大会出错：\n")

fax_price =10
one_year = 3600 * 24 * 365
buy_order_cny_limit = 1000
sell_order_cts_limit = 1000


##################### start ############################

account = client.Account(account_name, password, wallet_port)
account.unlock()


cny_settlement_price = 0
buy_price_standard = 0
sell_price_standard = 0


order_book = market.get_order_book('CNY', 'CTS', limit_order, wallet_port)
#print(order_book)
cny_settlement_price = market.get_cny_settlement_price(wallet_port)
print("目前喂价:",cny_settlement_price)
#######maybe not used,but keep it#####
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
#######
buy_group =  [0, 0, 0, 0, 0]
sell_group = [0, 0, 0, 0, 0]
bpg=[]
spg=[]
bqg=[]
sqg=[]
bb=[]
sb=[]
bid_quote = 0.0
ask_quote =0.0
sum_bid_price=0.0
sum_ask_price=0.0
cny_math_order=0.0
temp_b=0.0
temp_s=0.0

for i in range(0, len(order_book['bids'])):
	price = float(order_book['bids'][i]['price'])
	bpg.append(price)
	#print("price =",price)
	base = float(order_book['bids'][i]['base'])
	temp_b+=base
	bb.append(temp_b)
	#print("base=",base)	
	bid_quote +=float(order_book['bids'][i]['quote'])
	bqg.append(bid_quote)
	#print(price)
	#fpp=bpg[0]*fax_price
	if price < bpg[0]*(100-fax_price)/100:
		print("买单价位已超出最高价的",(100-fax_price)," %")
		bpg.pop()
		bqg.pop()
		bb.pop()
		break
for i in range(0, len(order_book['asks'])):
	price = float(order_book['asks'][i]['price'])
	spg.append(price)
	#print("price =",price)
	base = float(order_book['asks'][i]['base'])
	temp_s+=base
	sb.append(temp_s)
	#print("base=",base)	
	ask_quote +=float(order_book['asks'][i]['quote'])
	sqg.append(ask_quote)
	if price>spg[0]*(100+fax_price)/100:
		print("卖单价位已超出最低价的",(100+fax_price)," %")
		spg.pop()
		sqg.pop()
		sb.pop()
		break

print("买单价队列:",bpg,"\n买单总数队列:",bqg,"\n买单总价位:",bb,"\n卖单价队列:",spg,"\n卖单总数队列:",sqg,"\n卖单总价位:",sb)

if bqg[-1] > sqg[-1] :
	print("买单数量多过卖单，重新取买单数量")
	#bid_quote_1=0.0
	#l_quote=0
	for i in range(0, int(limit_order)):
		#print(bqg[i],sqg[-1])
		#print(i)
		if bqg[i]>=sqg[-1]: 
			#print("sdfasdf",i)
			if i ==0:
					sum_bid_price=bpg[i]*sqg[-1]
			else: sum_bid_price=bb[i-1]+bpg[i]*(sqg[-1]-bqg[i-1])
			print("相同",sqg[-1],"数量下,","买单总价:",sum_bid_price,"卖单总价:",sb[-1])
			cny_math_order=(sum_bid_price+sb[-1])/(sqg[-1]*2)
			print("市场买卖取",fax_price,"%偏差后最小深度计算出来的CTS喂价:",cny_math_order)
			break
		
		
elif bqg[-1] < sqg[-1]:
	print("卖单数量多过买单，重新取卖单数量")
	ask_quote_1=0.0
	l_quote=0
	for i in range(0, len(sqg)):
		if sqg[i]>=bqg[-1]:
			if i ==0:
				sum_ask_price=spg[i]*bqg[-1]
			else: sum_ask_price=sb[i-1]+spg[i]*(bqg[-1]-sqg[i-1])
			print("相同",sqg[-1],"数量下,","买单总价:",bb[-1],"卖单总价:",sum_ask_price)
			cny_math_order=(sb[-1]+sum_ask_price)/(bqg[-1]*2)
			print("市场买卖取",fax_price,"%偏差后最小深度计算出来的CTS喂价:",cny_math_order)
			break
	
else :
	print("买卖单请求数量相等")
	cny_math_order=(sb[-1]+bb[-1])/(bqg[-1]*2)
	print(cny_math_order)
cny_math_order=round(cny_math_order,5)
print(cny_math_order)
#feed_choice=input("请判断是否使用上方数值进行喂价.y/n\n")
#if feed_choice == 'y':
publish_feedprice(account_name, cny_math_order, wallet_port)
#else:
exit(0)




