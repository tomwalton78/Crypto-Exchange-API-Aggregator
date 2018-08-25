from twisted.internet import task, reactor

from exchange import ExchangeAPICallFailedException
from gdax_exchange import GdaxExchange
from kraken_exchange import KrakenExchange
from bitstamp_exchange import BitstampExchange
from bitfinex_exchange import BitfinexExchange

TIME_BETWEEN_CALLS = 10.0  # secs

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
                    market, ex.exchange_name
                ).replace('  ', ''))

# Set up LoopingCall for validated market-exchange objects
for obj in valid_market_exchange_objects:

    task.LoopingCall(
        obj.fetch_l1_quote_and_write_to_csv
    ).start(TIME_BETWEEN_CALLS)


reactor.run()
