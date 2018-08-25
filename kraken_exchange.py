from datetime import datetime

import api_common_functions as api_cf
from exchange import Exchange


class KrakenExchange(Exchange):
    """Object representing Kraken cryptocurrency exchange
    """

    def __init__(self, market):
        """Initialise KrakenExchange object for specified market

        Parameters
        ----------
        market : str
            Market (i.e. trading pair) that this instance will interact with

        """

        # Initialise parent class, Exchange
        super().__init__('kraken', market)

    def fetch_l1_quote(self):
        """Retrieve current level 1 quote from exchange's api

        Level 1 refers to obtaining price and quantity at best bid and best ask
        """

        # Make api call
        data = api_cf.fetch_data_from_url(
            'https://api.kraken.com/0/public/Ticker?pair={}'.format(
                self.market
            )
        )

        # Raise useful error if API call fails
        if data['error'] == ['EQuery:Invalid asset pair']:
            self.raise_failed_api_call_error()

        # Extract ticker data from json dict
        ticker = list(data['result'].keys())[0]
        data = data['result'][ticker]

        # Store latest l1 quote data
        self.latest_l1_quote = {
            'timestamp': datetime.utcnow(),
            'best bid price': float(data['b'][0]),
            'best bid size': float(data['b'][2]),
            'best ask price': float(data['a'][0]),
            'best ask size': float(data['a'][2])
        }


if __name__ == '__main__':
    k = KrakenExchange('LTC-GBP')
    k.fetch_l1_quote_and_write_to_csv()
    print(k.latest_l1_quote)
