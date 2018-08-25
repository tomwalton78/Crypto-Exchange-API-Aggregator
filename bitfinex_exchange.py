from datetime import datetime

import api_common_functions as api_cf
from exchange import Exchange


class BitfinexExchange(Exchange):
    """Object representing Bitfinex cryptocurrency exchange
    """

    def __init__(self, market):
        """Initialise BitfinexExchange object for specified market

        Parameters
        ----------
        market : str
            Market (i.e. trading pair) that this instance will interact with

        """

        # Initialise parent class, Exchange
        super().__init__('bitfinex', market)

    def fetch_l1_quote(self):
        """Retrieve current level 1 quote from exchange's api

        Level 1 refers to obtaining price and quantity at best bid and best ask
        """

        # Make api call
        data = api_cf.fetch_data_from_url(
            'https://api.bitfinex.com/v1/book/{}?group=1&limit_bids=1&limit_asks=1'.format(
                self.market
            )
        )

        # Check API response
        try:
            # API call failed if no exception thrown
            data['message']
            self.raise_failed_api_call_error()
        except KeyError:
            # Successful API call
            pass

        # Store latest l1 quote data
        self.latest_l1_quote = {
            'timestamp': datetime.utcnow(),
            'best bid price': float(data['bids'][0]['price']),
            'best bid size': float(data['bids'][0]['amount']),
            'best ask price': float(data['asks'][0]['price']),
            'best ask size': float(data['asks'][0]['amount'])
        }


if __name__ == '__main__':
    bf = BitfinexExchange('LTC-GBP')
    bf.fetch_l1_quote_and_write_to_csv()
    print(bf.latest_l1_quote)
