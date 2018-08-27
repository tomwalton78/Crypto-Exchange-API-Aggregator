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


### (3 Using the looping_data_collect.py file)

This script is simply useful for collecting and storing data repeatedly. The user specifies the exchanges and markets they want to cover, and also the time between api calls, and then the script will continually call these functions until stopped. It is currently set up to fetch an l1 quote and store in a csv (in the /datasets/ folder), with each exchange-market pair having its own csv file, although this can easily be modified.


## Testing

To run tests on both the exchanges module and the api_server module, first ensure that the API server us running by executing: `sudo python3 run_api_server.py` while at the root of this repo.

Then, in a new terminal window, still in the root directory of the repo, run: `python3 -m unittest tests/*.py`

You may now shut down the api server, by making a GET request to `http://localhost/shutdown`.


## Notes

### Cryptocurrency symbols

It should be noted that the 'standard' form of the symbol for a particular cryptocurrency is defined as the form used on [CoinMarketCap](https://coinmarketcap.com/), and this should be the form entered in this software. The software will automatically map this symbol to the symbol used on the exchange, so the user does not have to worry about the quirks of individual exchanges.

A `-` should always be used to separate the two symbols that make up a market.

The definitions for these maps are stored as JSON, in the `api/exchanges/exchange_info/` directory, with one JSON file for each exchange. If you want to use a symbol that is not in this JSON file you will need to add an entry for it, using the following format `"CoinMarketCap symbol" : "exchange specific symbol"`.

### Note on the functionality

Please note, the functionality of this project is not complete, as many more features could be implemented (i.e. support getting trades, level 2 order book, adding more exchanges etc.); however, this project is intended more as a proof of concept, rather than a feature complete piece of software.