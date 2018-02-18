import requests
import sys
import time
import os
#imports everything from apiQuery
from apiQuery import *
from GlobalVariables import *

running = 1
last96 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last30 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lastPrice = 0



#The main screen print with some basic formatting logic
def printLogScreen( ticker, lastPrice, SMA, lastBuyPrice, lastBuyQuant, waitBuy, lastSellPrice, lastSellQuant, waitSell, momentum):
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

    os.system('cls')

    header() #defined in global variables, prints the program name and version
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

def formatMarket(rString):
    lastIndex = rString.find("LastPrice")
    buyIndex = rString.find("BuyVolume")
    if(lastIndex != -1):
        slicePrice = rString[lastIndex+11:buyIndex-2]
        return float(slicePrice)
    elif(lastIndex == -1):
        return None

def formatMarkets(rString, pairString):
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

#The main log
def log( pairString ):
    counter96 = 0
    waitBuy = 0
    waitSell = 0
    set96( pairString )
    while 1 < 2:
        rString = public_api.get_markets()
        lastPrice = formatMarkets(rString, pairString )
        foward30( lastPrice )
        sum96 = 0
        for i in range(0,len(last96)):
            sum96 += last96[i]
        SMA = float(sum96) / float(len(last96))
        if counter96 == 29:
            counter96 = 0
            sum30 = 0
            for i in range(0,len(last30)):
                sum30 += last30[i]
            avg30 = float(sum30) / float(len(last30))
            foward96( avg30 )
        printLogScreen( pairString, lastPrice, SMA, 0, 0, waitBuy, 0, 0, waitSell, 0)
        counter96 += 1
        time.sleep(30)

def startBot():
    print("\nEnter a coin pair to analyze. E.g. use 'BTC' instead of 'Bitcoin'")
    coin1 = input("Enter the first coin: ")
    coin2 = input("Enter the second coin: ")
    log( coin1 + "/" + coin2 )

startBot()
