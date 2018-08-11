from datetime import datetime

import api_common_functions as api_cf
from exchange import Exchange


class GdaxExchange(Exchange):
    """Object representing GDAX (now Coinbase Pro) cryptocurrency exchange
    """

    def __init__(self, market):
        """Initialise GdaxExchange object for specified market

        Parameters
        ----------
        market : str
            Market (i.e. trading pair) that this instance will interact with

        """

        self.market = market
        super().__init__('gdax')

    def fetch_l1_quote(self):
        """Retrieve current level 1 quote from exchange's api

        Level 1 refers to obtaining price and quantity at best bid and best ask
        """

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
    g.fetch_l1_quote_and_write_to_csv()
    print(g.latest_l1_quote)
