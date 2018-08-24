from twisted.internet import task, reactor

from gdax_exchange import GdaxExchange
from kraken_exchange import KrakenExchange
from bitstamp_exchange import BitstampExchange

TIME_BETWEEN_CALLS = 10.0  # secs

markets = ['ETH-EUR', 'LTC-EUR', 'BTC-EUR']

for market in markets:

    g_etheur = GdaxExchange(market)
    g_etheur_LoopingCall = task.LoopingCall(
        g_etheur.fetch_l1_quote_and_write_to_csv
    ).start(TIME_BETWEEN_CALLS)

    k_etheur = KrakenExchange(market)
    k_etheur_LoopingCall = task.LoopingCall(
        k_etheur.fetch_l1_quote_and_write_to_csv
    ).start(TIME_BETWEEN_CALLS)

    b_etheur = BitstampExchange(market)
    b_etheur_LoopingCall = task.LoopingCall(
        b_etheur.fetch_l1_quote_and_write_to_csv
    ).start(TIME_BETWEEN_CALLS)

reactor.run()
