import requests
import sys

class public_api:

    def get_currencies():
        url = "https://www.cryptopia.co.nz/api/" + "GetCurrencies/"
        r = requests.get(url)
        rString = r.text
        return rString

    def get_trade_pairs():
        url = "http://www.cryptopia.co.nz/api/" + "GetTradePairs/"
        r = requests.get(url)
        rString = r.text
        return rString

    def get_market_history():
        print()

    def get_market_orders():
        print()

    def get_market_order_groups():
        print()

    def get_market(tpiString):
        url = "https://www.cryptopia.co.nz/api/" + "GetMarket/" + tpiString
        r = requests.get(url)
        rString = r.text
        lastIndex = rString.find("LastPrice")
        buyIndex = rString.find("BuyVolume")
        if(lastIndex != -1):
            slicePrice = rString[lastIndex+11:buyIndex-2]
            return slicePrice
        elif(lastIndex == -1):
            return None

    def get_markets(pairString):
        slashIndex = pairString.find("/")
        coin1 = pairString[:slashIndex]
        coin2 = pairString[slashIndex+1:]
        url = "https://www.cryptopia.co.nz/api/GetMarkets"
        r = requests.get(url)
        rString = r.text
        pairIndex = rString.find(pairString)
        if(pairIndex != -1):
            formattedText = rString[pairIndex:pairIndex+200]
            lastPriceIndex = formattedText.find("LastPrice")
            slicePrice = formattedText[(lastPriceIndex+11):(lastPriceIndex+20)]
            return slicePrice
        elif(pairIndex == -1):
            return None
