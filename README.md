# Crypto Exchange API Aggregator

This software allows the user to get data from the APIs of different cryptocurrency exchanges using the same interface, so that the user does not have to deal with understanding how to use all of the different APIs of individual exchanges.

## Getting Started

1. `pip3 install -r requirements.txt`
2. `python3 setup.py install`

There are 2 main ways of interacting with the api provided here: interacting directly with the python modules, or starting the api server and making requests to it through the browser.

### 1 Using the python modules

Create an instance of the object for the relevant exchange, specifying the market that that object will interact with; create a new instance for a different market. Then call methods to perform the corresponding actions. For example:
```python
from api.exchanges.kraken_exchange import KrakenExchange

k = KrakenExchange('BTC-EUR')
k.fetch_l1_quote()
print(k.latest_l1_quote)
```

### 2 Using the api server

Simply start the api server: `sudo python3 run_api_server.py`
Then you can make api requests in the browser, with `http://localhost/` as the base endpoint. For details of the api calls available, please see the corresponding documentation: [API Server Documentation](api/api_server/API_README.md)

## Note

Please note: the functionality of this project is not complete, as many more features could be implemented (i.e. support getting trades, level 2 order book, adding more exchanges etc.); however, this project is intended more as a proof of concept, rather than a feature complete piece of software.