import redis
import grequests
import json
import time
from twisted.python import log
from collections import OrderedDict
from twisted.internet import task, reactor, defer
import ccxt



db = redis.Redis('localhost', 6379)
def BitcoinAverage():
        reqs = [
            grequests.get("https://apiv2.bitcoinaverage.com/indices/global/ticker/BTCUSD"),
            grequests.get("https://apiv2.bitcoinaverage.com/indices/global/ticker/LTCUSD"),
            grequests.get("https://apiv2.bitcoinaverage.com/indices/global/ticker/ETHUSD"),
            grequests.get("https://apiv2.bitcoinaverage.com/indices/global/ticker/BCHUSD")]

        c = 0

        for req in grequests.map(reqs):
            db.hmset("bitcoinaverage:%s" % c , req.json())
            print(c, "done")
            c += 1


b = ccxt.bittrex()
g = ccxt.gdax()
h = ccxt.gemini()
i = ccxt.itbit()
k = ccxt.kraken()
a = ccxt.lakebtc()

def Exchanges():
    db.set("timestamp", int(time.time()))
    db.hmset("bittrex", b.fetch_tickers())
#    db.hmset("gdax", g.fetch_ticker())
#    db.hmset("gemini", h.fetch_tickers())
#    db.hmset("itbit", i.fetch_tickers())
    db.hmset("kraken", k.fetch_tickers())
#    db.hmset("lakebtc", a.fetch_tickers()


def periodic_task_crashed(reason):
        log.err(reason, "periodic_task_crashed")


l = task.LoopingCall(BitcoinAverage)
l2 = task.LoopingCall(Exchanges)

d = l.start(60)
d.addErrback(periodic_task_crashed)

d2 = l2.start(90)
d2.addErrback(periodic_task_crashed)


reactor.run()
