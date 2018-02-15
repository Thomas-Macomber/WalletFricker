import requests
import sys
import time
import os
#This has been imported in case you want to call anything from the other file. That way we don't have to rewrite it here.
#For example if you wanted to call the old get_market function you'd type "public_api.get_market()" and it would call it.
#Check out simpleHardCode.py to see how the class is set up.
import public_api

#For the sake of possibly calling functions in other files later I recommend you construct some classes and organize them.

running = 1
CryptoHopperName = "Wallet Fucker"
version = "Indev 0.0.1"
last96 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
last30 = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
lastPrice = 0

#Added color class. Each variable is a string representation that you need to enter to change the color of text.
#I made a change to printLogScreen to utilize colors for the first printed line. Feel free to check it to see implementation and run the program.
class color:
    RED = "\033[1;31;40m"
    YELLOW = "\033[1;33;40m"
    GREEN = "\033[1;32;40m"
    BLUE = "\033[1;34;40m"
    PURPLE = "\033[1;35;40m"
    CYAN = "\033[1;36;40m"
    BLACK = "\033[1;30;40m"
    WHITE = "\033[1;37;40m"

#basically GetMarkets except returns the value to the exterior function rather than printing it
#MIGHT BE FUCKED UP
#NAH BRO I FIXED IT NOW. KEEP READING FOR WHY IT DIDN'T WORK OR GO TO THE LAST LINE OF COMMENTS BEFORE RETRIEVE PRICE
#Now what it does is it takes a string starting at the coin par and goes out 200 characters
#From there it searches THAT string for the lastprice and gets the price based on that
#The reason the old method didn't work was because last price is after the volume of coin in their api
#Because the volume of the coin changes based on the coin it meant that the amount of characters to get to LastPrice from where the pair string was found changed based on the digits in volume
#This should bypass that and work with any coin combination now
#Tl;dr I suck at string searching
def retrievePrice( pairString ):
    url = "https://www.cryptopia.co.nz/api/GetMarkets"
    r = requests.get(url)
    rString = r.text
    pairIndex = rString.find(pairString)
    if(pairIndex != -1):
        formattedText = rString[pairIndex:pairIndex+200]
        lastPriceIndex = formattedText.find("LastPrice")
        slicePrice = formattedText[(lastPriceIndex+11):(lastPriceIndex+20)]
        return float(slicePrice)
    elif(pairIndex == -1 ):
        return 0

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

log( "ETN/BTC" )
