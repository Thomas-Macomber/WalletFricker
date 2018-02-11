import requests
import sys
import time
import os

running = 1
CryptoHopperName = "Wallet Fucker"
version = "Indev 0.0.1"
last96 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last30 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lastPrice = 0

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

#basically GetMarkets except returns the value to the exterior function rather than printing it
#MIGHT BE FUCKED UP
def retrievePrice( pairString ):
    url = "https://www.cryptopia.co.nz/api/GetMarkets"
    r = requests.get(url)
    rString = r.text
    pairIndex = rString.find(pairString)
    if(pairIndex != -1):
        pairLength = (len(pairString))
        slicePrice = rString[(pairIndex+117+pairLength):(pairIndex+127+pairLength)]
        return float(slicePrice)
    elif(pairIndex == -1 ):
        return 0


#So you can test this out. When running the .bat for this file it should ask for a TradePairId.
#Inputting the ID should output the ask price for that pair of currencies.
#AskPrice just meaning the amount of the second coin for one of the first coin.
#So inputting 4405 for example gives a rate of 1 HUSH to BLANK BTC. I think as of right now 1 hush is 0.00027491 BTC.
#I'll work on more formatting later to output the actual pairing and more information.
#I more or less just wanted to see if I could format the output using python.


def bot():
    methodString = input("\nPlease enter a command you would like to use: ")
    if(methodString == "GetMarket"):
        get_market()
    elif(methodString == "GetMarkets"):
        get_markets()
    elif(methodString == "help"):
        print("\nCurrent available commands are: \n'help' -Will display this list\n'exit' -Will terminate program\n'GetMarket' -Will retrieve current market asking price for a trade pair")
    elif(methodString == "exit"):
        sys.exit()
    else:
        print("\nPlease enter a valid command.")

#The main screen print with some basic formatting logic
def printLogScreen( ticker, lastPrice, SMA, lastBuyPrice, lastBuyQuant, waitBuy, lastSellPrice, lastSellQuant, waitSell, momentum):
    #defines the coins
    slashIndex = ticker.find("/")
    coin1 = ticker[:slashIndex]
    coin2 = ticker[slashIndex+1:]

    #determines the order status and which values should be N/A
    #if we have a pending buy order we want to know how much it's trying to buy
    if waitBuy == 1:
        buyIn = lastBuyPrice
        buyQ = lastBuyQuant
        sellOut = "N/A "
        sellQ = "N/A "
        status = "Pending Buy Order"
    #if we have a pending sell order we want to know how much its selling for and also what the previous purchase was for reference
    elif waitSell == 1:
        buyIn = lastBuyPrice
        buyQ = lastBuyQuant
        sellOut = lastSellPrice
        sellQ = lastSellQuant
        status = "Pending Sell Order"
    #if we have no pending orders its just scanning and we dont give a fuck
    else:
        buyIn = "N/A "
        buyQ = "N/A "
        sellOut = "N/A "
        sellQ = "N/A "
        status = "Scanning Market... "

    #clear the screen for clean look
    os.system('cls')

    #prints the screen
    print ( CryptoHopperName + "___" + version )
    print ( "Logging: " + ticker )
    print ( "Last Price: " + str(lastPrice) )
    print ( "SMA: " + str(SMA) )
    print ( "Current Market Momentum: " + str(momentum) )
    print ( "ORDER STATUS: " + str(status) )
    print ( "Buy: " + str(buyQ) + coin1 )
    print ( "   @ " + str(buyIn) + coin2 )
    print ( "Sell: " + str(sellQ) + coin1 )
    print ( "   @ " + str(sellOut) + coin2 )

#This function floods the last96 with a set value that the user determines to be near the currentSMA for a baseline
def set96( pairString ):
    currentSMA = input( "Please input current market SMA for: " + pairString + ": ")
    type(currentSMA)
    for i in range( 0, 96 ):
        last96[i] = float(currentSMA)

#This functions bumps all of the last96 values foward one and adds the lastPrice to the 0th index
def foward96( lastPrice ):
    for i in range( 95, 0, -1 ):
        #print(i)
        last96[ i ] = last96 [ i - 1]
    last96[0] = lastPrice

#This funtion mirrors foward96 but for last30
def foward30( lastPrice ):
    for i in range( 29, 0, -1 ):
        #print(i)
        last30[ i ] = last30[ i - 1]
    last30[0] = lastPrice

#The main log
def log( pairString ):
    #The last 96 should only update every 15 minutes, this keeps track of progress
    counter96 = 0
    #If we're waiting to confirm a buy ORDER
    #NOT YET IMPLIMENTED
    waitBuy = 0
    #If we're waiting to confirm a sell ORDER
    #NOT YET IMPLIMENTED
    waitSell = 0
    #sets the SMA to give a baseline
    set96( pairString )
    #Starts the loop of unending refresh
    while 1 < 2:
        #grabs the lastprice
        lastPrice = retrievePrice( pairString )
        #moves the 30 values stored in last30 foward by 1 adding in the current price
        foward30( lastPrice )

        #refreshes the SMA
        sum96 = 0
        for i in range(0,len(last96)):
            sum96 += last96[i]
        SMA = float(sum96) / float(len(last96))

        #if the counter has hit 29 then we have gone through 30 chunks of 30 seconds (15 min)
        #this starts an update of last 96, the less precise list over a longer period
        if counter96 == 29:
            #resets counter
            counter96 = 0

            #averages the last 15 minutes
            sum30 = 0
            for i in range(0,len(last30)):
                sum30 += last30[i]
            avg30 = float(sum30) / float(len(last30))

            #slaps that bitch into the last96 list
            foward96( avg30 )

        #prints the main screen
        printLogScreen( pairString, lastPrice, SMA, 0, 0, waitBuy, 0, 0, waitSell, 0)
        #increments the counter
        counter96 += 1
        #waits 30 seconds (our current refresh rate)
        time.sleep(30)

log( "HUSH/BTC" )


#LEFTOVER CODE FROM TESTS THIS MORNING
#api_query("GetMarket/1262")  #just another request test
#api_query("GetMarkets")  #returns ALL markets regardless of trade pair id
#api_query("GetMarketHistory/LTC_BTC/48")  #Returns all history of LTC to BTC exchanges within the past 48 hours. Without the 48 the default hour is 24.
#This mother fucker works. We go frome here I guess (Create new files, I know its basic code but lets not fuck it up)
