from util import *
from blockchain import *

def get_order_book(money, asset, depth, port):
        return post("get_order_book", [money, asset, depth], port)['result']


def get_cny_settlement_price(port):
        result = get_object(["2.4.0"], port)["result"]
        cny = result[0]["current_feed"]['settlement_price']['base']['amount']
        bts = result[0]["current_feed"]['settlement_price']['quote']['amount']
        return float(cny) * 10 / float(bts)


def publish_cny_feed_price(account, cts_amount, cny_amount, port):
	return publish_feed_price(account, cts_amount, 'CNY', '1.3.1',cny_amount, port)
