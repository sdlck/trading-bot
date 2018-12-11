import requests
import time
import hmac
from hashlib import sha256, sha512

BINANCE_KEY =  ''
BINANCE_SECRET = ''
BINANCE_URL = 'https://api.binance.com/api/v3/'
BINANCE_HEADERS = {'Accept': 'application/json', 'User-Agent': 'binance/python', 'X-MBX-APIKEY': BINANCE_KEY}

BITTREX_KEY = ''
BITTREX_SECRET = ''
BITTREX_URL = 'https://bittrex.com/api/v1.1/'


def signRequest(secret, data, hashFunction):
    return hmac.new(secret.encode(), data.encode(), hashFunction).hexdigest()


def binanceTrade(symbol, side, tradeType, quantity, price, timeInForce='GTC', recvWindow='5000'):
    timestamp = str(int(time.time() * 1000))
    request = 'symbol=' + symbol \
              + '&side=' + side \
              + '&type=' + tradeType \
              + '&timeInForce=' + timeInForce \
              + '&quantity=' + quantity \
              + '&price=' + price \
              + '&recvWindow=' + recvWindow \
              + '&timestamp=' + timestamp
    signed_request = BINANCE_URL + 'order?' + request + '&signature=' + signRequest(BINANCE_SECRET, request, sha256)
    return requests.post(signed_request, headers=BINANCE_HEADERS).content


def binancePrice(symbol):
    request = BINANCE_URL + 'ticker/price?symbol=' + symbol
    return requests.get(request).content


def bittrexTrade(side, symbol, quantity, rate):
    timestamp = str(int(time.time() * 1000))
    request = side + 'limit?' \
            + 'apikey=' + BITTREX_KEY \
            + '&nonce=' + timestamp \
            + '&market=' + symbol \
            + '&quantity=' + quantity \
            + '&rate=' + rate
    request = BITTREX_URL + 'market/' + request
    print(request)
    apisign = signRequest(BITTREX_SECRET, request, sha512)
    return requests.post(request, headers={'apisign': apisign}).content


def bittrexPrice(symbol):
    request = BITTREX_URL + 'public/getticker?market=' + symbol
    return requests.get(request).content

def main():
    binancePriceRequest = binancePrice('ADAUSDT')
    binanceTradeRequest = binanceTrade('ADAUSDT', 'SELL', 'LIMIT', '400', '0.05')
    bittrexPriceRequest = bittrexPrice('USD-ADA')
    bittrexTradeRequest = bittrexTrade('sell', 'USD-ADA', '400', '0.05')
    print(binancePriceRequest)
    print(binanceTradeRequest)
    print(bittrexPriceRequest)
    print(bittrexTradeRequest)


main()

