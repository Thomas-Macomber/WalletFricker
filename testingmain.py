# written by Thomas Macomber and Sean Glasgow

#all of the imports, as we figure out they do we need to add comments

import time
import hmac
import urllib
#HTTP for humans
import requests
import hashlib
import base64
#is this one a typo? It tries to auto complete
import sys
import json

#string define for the URL
urlPub = "https://www.cryptopia.co.nz/api/"
urlPri = "https://www.cryptopia.co.nz/Api/"
#sets a variable for loop
running = 1

#Defines the function api_query and inputs a method and a req
def api_query (method, req = None ):
    #like WTF is this ! Creates an empty set req (I think?)
    if not req:
        req = {}

    #the array/set of all of the public API commands
    public_set = set([ "GetCurrencies", "GetTradePairs", "GetMarkets", "Get Market", "GetMarketHistory"])
    #the array/set of all of the private API Commands
    private_set = set([ "GetBalance", "GetDepositAddress", "GetOpenOrders", "GetTradeHistory", "GetTransactions", "SubmitTrade", "CancelTrade", "SubmitTip"])
    #Tells the function how to handle querys in the public array. If the method is in public_set it calls this if
    if method in public_set:
        #Sets the current used URL (only import if the Api vs api matters) Uses the method passed through and appends to urlPub to access the information for the method.
        #Here it does url = https://www.cryptopia.co.nz/api/ + GetMarkets. Try going to https://www.cryptopia.co.nz/api/GetMarkets
        url = urlPub + method
        #If there is a specific request (i.e. GetMarket singular)
        if req:
            #no fucking clue. Same here, it seems to find the parameter defined by 4405 at the moment and append it to https://www.cryptopia.co.nz/api/GetMarkets
            #Look through cryptopia to find out what the parameter 4405 corresponds to
            for param in req:
                #adds a slash and the neccessary params. ye boi
                url += "/" + str( param )
        #Passes data through r cause we lazy
        #This pings the url defined in the first half of api_query. Issue right now is url isn't accessed, r isn't accessed. Meaning responses down below is calling a variable that isn't assigned anything yet.
        r = requests.get( url )
    #Tells the funtion how to handle querys in the private array (with authentications)
    elif method in private_set:
        #Same as above but just with private sets
        url = urlPri + method

        #leaving this blank for a while until I can successfully log the public queries
    #Assigns response to a unicode text object of what r is. R is supposed to be the webpage info I'm assuming.
    reponse = r.text
    #Gives you that sweet fucking mail
    #Tbh I have no fucking clue what the purpose of this is.
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

#Anything we want to run indefinitely -- Calls api_query function defined above, inputs GetMarket method and 4405 key. Need to find what 4405 is
def loop ():
    HUSH = api_query ("GetMarket", 4405)
    return HUSH

#Calls loop() function while the script is running.
while running == 1:
    #runs loop (Woah)
    loop()
