import requests
import sys
import time

running = 1

#I'm going to make some changes to the methods. Primary so that we have specific methods for each API command instead
#of having one large method that does everything. Maybe I'll clean it up later but this is mostly because
#the one large method last time was fucking everything up. So I'm going to rename this method "api_query" to "get_market"

def get_markets():
    pairString = "HUSH/BTC"
    slashIndex = pairString.find("/")
    coin1 = pairString[:slashIndex]
    coin2 = pairString[slashIndex+1:]
    url = "https://www.cryptopia.co.nz/api/GetMarkets"
    r = requests.get(url)
    rString = r.text
    pairIndex = rString.find(pairString)
    if(pairIndex != -1):
        pairLength = (len(pairString))
        slicePrice = rString[(pairIndex+117+pairLength):(pairIndex+127+pairLength)]
        floatPrice = float(slicePrice)
        print(floatPrice)
    elif(pairIndex == -1):
        print("The pair: " + pairString + " does not exist.")

#So you can test this out. When running the .bat for this file it should ask for a TradePairId.
#Inputting the ID should output the ask price for that pair of currencies.
#AskPrice just meaning the amount of the second coin for one of the first coin.
#So inputting 4405 for example gives a rate of 1 HUSH to BLANK BTC. I think as of right now 1 hush is 0.00027491 BTC.
#I'll work on more formatting later to output the actual pairing and more information.
#I more or less just wanted to see if I could format the output using python.

while running == 1:
    time.sleep(5)
    get_markets()

#LEFTOVER CODE FROM TESTS THIS MORNING
#api_query("GetMarket/1262")  #just another request test
#api_query("GetMarkets")  #returns ALL markets regardless of trade pair id
#api_query("GetMarketHistory/LTC_BTC/48")  #Returns all history of LTC to BTC exchanges within the past 48 hours. Without the 48 the default hour is 24.
#This mother fucker works. We go frome here I guess (Create new files, I know its basic code but lets not fuck it up)
