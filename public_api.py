import requests
import sys

running = 1

class public_api:

    def get_currencies():
        url = "https://www.cryptopia.co.nz/api/" + "GetCurrencies/"
        r = requests.get(url)
        rString = r.text
        print(rString)

    def get_market():
        tpiString = input("Please enter the TradePairId you would like to search for: ")
        type(tpiString)
        url = "https://www.cryptopia.co.nz/api/" + "GetMarket/" + tpiString
        r = requests.get(url)
        rString = r.text
        lastIndex = rString.find("LastPrice")
        buyIndex = rString.find("BuyVolume")
        if(lastIndex != -1):
            slicePrice = rString[lastIndex+11:buyIndex-2]
            print("Last sold price of trade pair " + tpiString + " is: "  + slicePrice)
        elif(lastIndex == -1):
            slicePrice = rString[lastIndex+60:buyIndex-10]
            print("TradePairId: " + slicePrice + "does not exist.")
        continueString = input("\nWould you like to input another TradePairId? (y/n): ")
        type(continueString)
        if(continueString == "y"):
            public_api.get_market()
        else:
            public_api.bot()

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
            formattedText = rString[pairIndex:pairIndex+200]
            lastPriceIndex = formattedText.find("LastPrice")
            slicePrice = formattedText[(lastPriceIndex+11):(lastPriceIndex+20)]
            print("The exchange rate for " + coin1 + " to " + coin2 + " is: " + slicePrice +"\nOr 1 " + coin1 + " to " + slicePrice + " " + coin2)
        elif(pairIndex == -1):
            print("The pair: " + pairString + " does not exist.")
        continueString = input("\nWould you like to input another pair? (y/n): ")
        type(continueString)
        if(continueString == "y"):
            public_api.get_markets()
        else:
            public_api.bot()

    def help():
        print("\nCurrent available commands are: \n")
        print("'help' -Will display this list\n")
        print("'exit' -Will terminate program\n")
        print("'GetMarketId' -Will retrieve current market price for a trade pair Id\n")
        print("'GetMarketPair' -Will retrieve current market asking price for a trade pair")

    def bot():
        methodString = input("\nPlease enter a command you would like to use: ")
        if(methodString == "GetMarketId"):
            public_api.get_market()
        elif(methodString == "GetMarketPair"):
            public_api.get_markets()
        elif(methodString == "GetCurrencies"):
            public_api.get_currencies()
        elif(methodString == "help"):
            public_api.help()
        elif(methodString == "exit"):
            sys.exit()
        else:
            print("\nPlease enter a valid command.")

while running == 1:
    public_api.bot()
