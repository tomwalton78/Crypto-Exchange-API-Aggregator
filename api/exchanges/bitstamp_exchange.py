from datetime import datetime
from json.decoder import JSONDecodeError

from api.exchanges.exchange import Exchange


class BitstampExchange(Exchange):
    """Object representing Bitstamp cryptocurrency exchange
    """

    def __init__(self, market):
        """Initialise BitstampExchange object for specified market

        Parameters
        ----------
        market : str
            Market (i.e. trading pair) that this instance will interact with

        """

        # Initialise parent class, Exchange
        super().__init__('bitstamp', market)

    def fetch_l1_quote(self):
        """Retrieve current level 1 quote from exchange's api

        Level 1 refers to obtaining price and quantity at best bid and best ask
        """

        # Make api call
        try:
            data = self._make_and_parse_GET_request(
                'https://www.bitstamp.net/api/v2/order_book/{}/'.format(
                    self.market
                )
            )
        # Raise useful error if API call fails
        except JSONDecodeError:
            self.raise_failed_api_call_error()

        # Store latest l1 quote data
        self.latest_l1_quote = {
            'timestamp': datetime.utcnow(),
            'best bid price': float(data['bids'][0][0]),
            'best bid size': float(data['bids'][0][1]),
            'best ask price': float(data['asks'][0][0]),
            'best ask size': float(data['asks'][0][1])
        }


if __name__ == '__main__':
    b = BitstampExchange('ETH-EUR')
    b.fetch_l1_quote_and_write_to_csv()
    print(b.latest_l1_quote)
