import requests


bitstamp_url = "https://www.bitstamp.net/api/v2/ticker/btcusd/"


def get_btc_price():
    result = requests.get(bitstamp_url).json()
    return int(result["low"])
