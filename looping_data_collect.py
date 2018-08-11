from twisted.internet import task, reactor

from gdax_exchange import GdaxExchange
from kraken_exchange import KrakenExchange

TIME_BETWEEN_CALLS = 5.0  # secs


g_etheur = GdaxExchange('ETH-EUR')
k_etheur = KrakenExchange('ETHEUR')

g_etheur_LoopingCall = task.LoopingCall(
    g_etheur.fetch_l1_quote_and_write_to_csv
).start(TIME_BETWEEN_CALLS)

k_etheur_LoopingCall = task.LoopingCall(
    k_etheur.fetch_l1_quote_and_write_to_csv
).start(TIME_BETWEEN_CALLS)

reactor.run()
