import requests

def api_query( method ):
    url = "https://www.cryptopia.co.nz/api/" + method
    r = requests.get(url)
    #return not print
    return(r.text)

def get_last( method ):
    market = api_query( method )
    found = 0
    for i in range(185, 200):
        char = market[i]
        print( i, char )
        if char == ":":
            found = i + 1
            print("Found at: ", found)
    print("LAST PRICE FOUND AT: ", market[found:found+10])


get_last("GetMarket/4405")

#I'm doing a shit job commenting but I'm basically just running this a
#   a shit load of times trying to nail down small pieces of the puzzle
#   try running this with a batch. I had it print out a few flags that
#   kind of explain what its doing. Essentially I found roughly where
#   the "LastPrice" is however since some cryptos have 3 vs. 4 character
#   ticker symbols it moves..... so this gets close enough then finds the
#   ":" that always follows "LastPrice" and prints the next 10 didgits
#   obviously this is a string but I don't know enough about string to int
#   to move foward. Someother time. I'm going to bed.
