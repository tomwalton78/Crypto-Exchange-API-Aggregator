from twisted.internet import task, reactor

from api.exchanges.exchange import ExchangeAPICallFailedException
from api.exchanges.gdax_exchange import GdaxExchange
from api.exchanges.kraken_exchange import KrakenExchange
from api.exchanges.bitstamp_exchange import BitstampExchange
from api.exchanges.bitfinex_exchange import BitfinexExchange

TIME_BETWEEN_CALLS = 10.0  # secs
DATATSET_STORAGE_FOLDER_REL_PATH = 'datasets/'

# Specify markets and exchanges to collect data for
markets = ['ETH-EUR', 'LTC-EUR', 'BTC-EUR']
exchanges = [GdaxExchange, KrakenExchange, BitstampExchange, BitfinexExchange]

# Check markets exist
valid_market_exchange_objects = []
for market in markets:
    for exchange_obj in exchanges:

        try:
            ex = exchange_obj(market)
            ex.fetch_l1_quote()
            valid_market_exchange_objects.append(ex)
        except ExchangeAPICallFailedException:
            print(
                'API call for {} market on the {} exchange failed. \
                Not collecting.\n'.format(
                    market, ex.exchange_name,
                ).replace('  ', ''))

# Set up LoopingCall for validated market-exchange objects
for obj in valid_market_exchange_objects:

    kwargs = {'path_to_folder': DATATSET_STORAGE_FOLDER_REL_PATH}
    task.LoopingCall(
        obj.fetch_l1_quote_and_write_to_csv, **kwargs
    ).start(TIME_BETWEEN_CALLS)


reactor.run()
