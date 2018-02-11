import requests

def api_query( method ):
    url = "https://www.cryptopia.co.nz/api/" + method
    r = requests.get(url)
    print(r.text)

api_query("GetMarket/4405")

#This mother fucker works. We go frome here I guess (Create new files, I know its basic code but lets not fuck it up)
