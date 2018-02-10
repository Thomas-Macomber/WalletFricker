# written by Thomas Macomber and Sean Glasgow

#all of the imports, as we figure out they do we need to add comments

import time
import hmac
import urllib
#import requests
import hashlib
import base64
#is this one a typo? It tries to auto complete
import sys
import json

#string define for the URL
urlPub = "https://www.cryptopia.co.nz/api/"
urlPri = "https://www.cryptopia.co.nz/Api/"
running = 1

#Okay so I don't understand this funftion definition but it seems important (its the main query funct.)
def api_query (method, req = None ):
    #like WTF is this !
    if not req:
        req = {}

    #the array/set of all of the public API commands
    public_set = set([ "GetCurrencies", "GetTradePairs", "GetMarkets", "Get Market", "GetMarketHistory"])
    #the array/set of all of the private API Commands
    private_set = set([ "GetBalance", "GetDepositAddress", "GetOpenOrders", "GetTradeHistory", "GetTransactions", "SubmitTrade", "CancelTrade", "SubmitTip"])
    #Tells the function how to handle querys in the public array
    if method in public_set:
        #Sets the current used URL (only import if the Api vs api matters)
        url = urlPub + method
        #If there is a specific request (i.e. GetMarket singular)
        if req:
            #no fucking clue
            for param in req:
                #adds a slash and the neccessary params
                url += "/" +str( param )
        #Passes data through r cause we lazy
        r = requests.get( url )
    #Tells the funtion how to handle querys in the private array (with authentications)
    elif method in private_set:
        url = urlPri + method

        #leaving this blank for a while until I can successfully log the public queries

    #Finishes the pass through with r
    response = r.text
    #Gives you that sweet fucking mail
    print ("You Got Mail!!! " + response)
    return response.replace("false","False").replace("true,","True").replace('":null','":None')
#Anything we need to run once at the begining of the program
def setup():
    #Gather the API_KEY and API_SECRET
    API_KEY =  raw_input("Public Key: ")
    API_SECRET = raw_input("Secret Key: ")
    #for debugging, comment out when unneccessary
    print ("Your API_KEY is: ", API_KEY)
    print ("Your API_SECRET is: ", API_SECRET)

#Anything we want to run indefinitely
def loop ():
    print (api_query("GetMarket", [4405, 6]))

#starts the non terminating loop
while running == 1:
    #runs loop (Woah)
    loop()
