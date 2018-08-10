from datetime import datetime

import api_common_functions as api_cf
from exchange import Exchange


class GdaxExchange(Exchange):

    def __init__(self, market):
        self.market = market
        super().__init__('gdax')

    def fetch_l1_quote(self):
        # Make api call
        data = api_cf.fetch_data_from_url(
            'https://api.pro.coinbase.com/products/{}/book?level=1'.format(
                self.market
            )
        )

        # Store latest l1 quote data
        self.latest_l1_quote = {
            'timestamp': datetime.utcnow(),
            'best bid price': float(data['bids'][0][0]),
            'best bid size': float(data['bids'][0][1]),
            'best ask price': float(data['asks'][0][0]),
            'best ask size': float(data['asks'][0][1])
        }


if __name__ == '__main__':
    g = GdaxExchange('ETH-EUR')
    g.fetch_l1_quote()
    g.latest_l1_quote_to_csv()
    print(g.latest_l1_quote)
