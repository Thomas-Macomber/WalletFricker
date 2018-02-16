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

#Added color class. Each variable is a string representation that you need to enter to change the color of text.
#I made a change to printLogScreen to utilize colors for the first printed line. Feel free to check it to see implementation and run the program.
#Note: Colors only seem to work after the program starts looping. It's a little weird and I'm not sure why that is.
class color:
    RED = "\033[1;31;40m"
    YELLOW = "\033[1;33;40m"
    GREEN = "\033[1;32;40m"
    BLUE = "\033[1;34;40m"
    PURPLE = "\033[1;35;40m"
    CYAN = "\033[1;36;40m"
    BLACK = "\033[1;30;40m"
    WHITE = "\033[1;37;40m"

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
    print ( color.GREEN + CryptoHopperName + color.WHITE + "___" + color.RED + version + color.WHITE)
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
        lastPrice = public_api.get_markets( pairString )
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

def startBot():
    print("\nEnter a coin pair to analyze. E.g. use 'BTC' instead of 'Bitcoin'")
    coin1 = input("Enter the first coin: ")
    coin2 = input("Enter the second coin: ")
    log( coin1 + "/" + coin2 )

startBot()
