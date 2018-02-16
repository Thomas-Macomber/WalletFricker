import requests
import time
import os
import sys

class public_api:

    url = "https://www.cryptopia.co.nz/api/"
    coinCounter = 0
#returns unformatted text of every currency on the exchange as of pinging
    def get_currencies():
        methodUrl = public_api.url + "GetCurrencies/"
        r = requests.get(methodUrl)
        rString = r.text
        return rString

#returns unformatted text of every trade pair on the exchange as of pinging
    def get_trade_pairs():
        methodUrl = public_api.url + "GetTradePairs/"
        r = requests.get(methodUrl)
        rString = r.text
        return rString

#returns unformatted market history of a specific trade pair within the past
#number of x hours. Accepts trade pair ID for format or symbol pairs in format SYM_SYM
    def get_market_history(market, time):
        methodUrl = public_api.url + "GetMarketHistory/" + market + "/" + time
        r = requests.get(methodUrl)
        rString = r.text
        if (rString.find("Market " + market + " not found") != -1):
            return None
        else:
            return rString

#returns the open buy and sell orders for a trade pair id or symbol pair in the format SYM_SYM
#Count specifies how many orders you wish to return
#Currently unformatted
    def get_market_orders(market, count):
        methodUrl = public_api.url + "GetMarketOrders/" + market + "/" + count
        r = requests.get(methodUrl)
        rString = r.text
        return rString

#takes a list of markets and returns buy and sell orders for specified trade pairs or symbol pairs in the format SYM_SYM
#Count specifies how many orders of EACH you wish to return
#For instance, specifying a count of 5 for 2 groups will return 5 buy AND 5 sell for BOTH groups, totaling 20 entries.
#at least.. that's what I think it does. I'm not 100% sure I got it working properly
#You need to create a list, THEN fill it with pairs/symbols, THEN pass it to the function and it should work.
#Again, the return is currently unformatted.
    def get_market_order_groups(groupList, count):
        urlString = ""
        for group in groupList:
            urlString += group + "-"
        urlStringFormatted = urlString[:-1]
        methodUrl = public_api.url + "GetMarketOrderGroups/" + urlStringFormatted + "/" + count
        r = requests.get(methodUrl)
        rString = r.text
        return rString

#returns last price of a trade pair
    def get_market(tpiString):
        methodUrl = public_api.url + "GetMarket/" + tpiString
        r = requests.get(methodUrl)
        rString = r.text
        lastIndex = rString.find("LastPrice")
        buyIndex = rString.find("BuyVolume")
        if(lastIndex != -1):
            slicePrice = rString[lastIndex+11:buyIndex-2]
            return float(slicePrice)
        elif(lastIndex == -1):
            return None

#Returns last price of a coin pair
#Added a  bunch of error checking. Basically just checking the coin index to see if they exist, and flipping pairs to retest if the pair exists given the coins exist
    def get_markets(pairString):
        methodUrl = public_api.url + "GetMarkets/"
        r = requests.get(methodUrl)
        rString = r.text
        pairIndex = rString.find(pairString)
        slashIndex = pairString.find("/")
        coin1 = pairString[:slashIndex]
        coin2 = pairString[slashIndex+1:]
        if(rString.find(coin1) == -1):
            print(coin1 + " is not currently on this exchange.")
            startBot()
        elif(rString.find(coin2) == -1):
            print(coin2 + " is not currently on this exchange.")
            startBot()
        else:
            if(pairIndex != -1):
                formattedText = rString[pairIndex:pairIndex+200]
                lastPriceIndex = formattedText.find("LastPrice")
                slicePrice = formattedText[(lastPriceIndex+11):(lastPriceIndex+20)]
                return float(slicePrice)
            elif(pairIndex == -1):
                public_api.coinCounter += 1
                if public_api.coinCounter%2 == 0:
                    print("Pair does not exist in current market\nPlease enter a different coin pair.")
                    startBot()
                else:
                    print("Pair doesn't exist in current format . . . Flipping for computation\nPlease enter SMA value again.")
                    newPairString = coin2 + "/" + coin1
                    log(newPairString)

class private_api:

    def get_balance():
        return None

    def get_deposit_address():
        return None

    def get_open_orders():
        return None

    def get_trade_history():
        return None

    def get_transactions():
        return None

    def submit_trade():
        return None

    def cancel_trade():
        return None

    def submit_tip():
        return None

    def submit_withdraw():
        return None

    def submit_transfer():
        return None
