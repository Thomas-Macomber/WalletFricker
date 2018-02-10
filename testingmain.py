# written by Thomas Macomber and Sean Glasgow

#all of the imports, as we figure out they do we need to add comments

import time
import hmac
import urllib
import requests
import hashlib
import base64
#is this one a typo? It tries to auto complete
import sys
import json

#Okay so I don't understand this funftion definition but it seems important (its the main query funct.)
def api_query (method, req = None ):
    #like WTF is this !
    if not req:
        req = {}

    #the array/set of all of the public API commands
    public_set = set([ "GetCurrencies", "GetTradePairs", "GetMarkets", "Get Market", "GetMarketHistory"])
    #the array/set of all of the private API Commands
    private_set = set([ "GetBalance", "GetDepositAddress", "GetOpenOrders", "GetTradeHistory", "GetTransactions", "SubmitTrade", "CancelTrade", "SubmitTip"])



#Anything we need to run once at the begining of the program
def setup():
    #Gather the API_KEY and API_SECRET
    API_KEY =  raw_input("Public Key: ")
    API_SECRET = raw_input("Secret Key: ")
    #for debugging, comment out when unneccessary
    print "Your API_KEY is: ", API_KEY
    print "Your API_SECRET is: ", API_SECRET

#Anything we want to run indefinitely
def loop ():
