import market
import client

def publish_feedprice(account_name, feed_price, wallet_port):
        bts_amount = 100
        cny_amount = bts_amount * feed_price
        ret =market.publish_cny_feed_price(account_name, bts_amount * 100000, cny_amount * 10000, wallet_port)
        print(ret)

#################### start ##############################
# 
# wallet port which cli_wallet opened  
wallet_port = "8093"
# feed price you want to feed
f_f=input("1CTS=?CNY,cin\n")
print(f_f)
feed_price = float(f_f)
print(feed_price)
# account name which you publish your feed price
account_name = "init3"
password = "asadf"
passwdrd = getpass.getpass("enter your password of ",account_name,"： ")
#######################################################

account = client.Account(account_name, password, wallet_port)
account.unlock

publish_feedprice(account_name, feed_price, wallet_port)

