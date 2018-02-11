import requests
import sys

running = 1
print("\nScript to find the current information about crypto.\nType 'help' to view valid commands.")

#I'm going to make some changes to the methods. Primary so that we have specific methods for each API command instead
#of having one large method that does everything. Maybe I'll clean it up later but this is mostly because
#the one large method last time was fucking everything up. So I'm going to rename this method "api_query" to "get_market"

def get_market():
    tpiString = input("Please enter the TradePairId you would like to search for: ")
    type(tpiString)
    url = "https://www.cryptopia.co.nz/api/" + "GetMarket/" + tpiString
    r = requests.get(url)
    rString = r.text
    tpiIndex = rString.find("AskPrice")
    bidIndex = rString.find("BidPrice")
    if(tpiIndex != -1):
        slicePrice = rString[tpiIndex+10:bidIndex-2]
        print("Current asking price for trade pair " + tpiString + " is: "  + slicePrice)
    elif(tpiIndex == -1):
        slicePrice = rString[tpiIndex+60:bidIndex-10]
        print("TradePairId: " + slicePrice + "does not exist.")
    continueString = input("\nWould you like to input another TradePairId? (y/n): ")
    type(continueString)
    if(continueString == "y"):
        get_market()
    else:
        bot()

def get_markets():
    pairString = input("\nPlease enter a pair in the format COIN/COIN to see their exchange rate: ")
    type(pairString)
    slashIndex = pairString.find("/")
    coin1 = pairString[:slashIndex]
    coin2 = pairString[slashIndex+1:]
    url = "https://www.cryptopia.co.nz/api/GetMarkets"
    r = requests.get(url)
    rString = r.text
    pairIndex = rString.find(pairString)
    if(pairIndex != -1):
        pairLength = (len(pairString))
        slicePrice = rString[(pairIndex+13+pairLength):(pairIndex+23+pairLength)]
        print("The exchange rate for " + coin1 + " to " + coin2 + " is: " + slicePrice +"\nOr 1 " + coin1 + " to " + slicePrice + " " + coin2)
    elif(pairIndex == -1):
        print("The pair: " + pairString + " does not exist.")
    continueString = input("\nWould you like to input another pair? (y/n): ")
    type(continueString)
    if(continueString == "y"):
        get_markets()
    else:
        bot()

#So you can test this out. When running the .bat for this file it should ask for a TradePairId.
#Inputting the ID should output the ask price for that pair of currencies.
#AskPrice just meaning the amount of the second coin for one of the first coin.
#So inputting 4405 for example gives a rate of 1 HUSH to BLANK BTC. I think as of right now 1 hush is 0.00027491 BTC.
#I'll work on more formatting later to output the actual pairing and more information.
#I more or less just wanted to see if I could format the output using python.


def bot():
    methodString = input("\nPlease enter a command you would like to use: ")
    if(methodString == "GetMarketId"):
        get_market()
    elif(methodString == "GetMarketPair"):
        get_markets()
    elif(methodString == "help"):
        print("\nCurrent available commands are: \n'help' -Will display this list\n'exit' -Will terminate program\n'GetMarketId' -Will retrieve current market asking price for a trade pair Id\n'GetMarketPair' -Will retrieve current market asking price for a trade pair ")
    elif(methodString == "exit"):
        sys.exit()
    else:
        print("\nPlease enter a valid command.")

while running == 1:
    bot()

#LEFTOVER CODE FROM TESTS THIS MORNING
#api_query("GetMarket/1262")  #just another request test
#api_query("GetMarkets")  #returns ALL markets regardless of trade pair id
#api_query("GetMarketHistory/LTC_BTC/48")  #Returns all history of LTC to BTC exchanges within the past 48 hours. Without the 48 the default hour is 24.
#This mother fucker works. We go frome here I guess (Create new files, I know its basic code but lets not fuck it up)
