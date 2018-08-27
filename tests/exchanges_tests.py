import unittest
from datetime import datetime
import os
import sys

from api.exchanges.exchange import ExchangeAPICallFailedException
from api.exchanges.gdax_exchange import GdaxExchange
from api.exchanges.kraken_exchange import KrakenExchange
from api.exchanges.bitstamp_exchange import BitstampExchange
from api.exchanges.bitfinex_exchange import BitfinexExchange


class HiddenPrints:
    """Class to disable printing for functions run under its scope.

    Example:
    with HiddenPrints()
        print('hello world')

    Nothing will print, since anything under the scope of HiddenPrints has its
    printing output suppressed.

    """

    def __enter__(self):
        """Disable printing on entering 'with HiddenPrints()' scope
        """
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Re-enable printing on exiting 'with HiddenPrints()' scope
        """
        sys.stdout.close()
        sys.stdout = self._original_stdout


class GdaxExchangeTests(unittest.TestCase):
    """
    Tests that functions within GdaxExchange class perform as intended.
    """

    def test_initialisation_with_valid_market(self):
        try:
            g = GdaxExchange('BTC-EUR')
            pass
        except KeyError:
            self.fail(
                'Initialising GdaxExchange with BTC-EUR raised KeyError.'
            )

    def test_initialisation_with_invalid_market(self):
        with self.assertRaises(KeyError):
            g = GdaxExchange('REDDDDDDDDDD-BLUEEEEEEEEEE')

    def test_fetch_l1_quote_on_supported_market(self):
        try:
            g = GdaxExchange('BTC-EUR')
            g.fetch_l1_quote()
            pass
        except Exception as e:
            self.fail(
                'Fetch l1 quote on supported market failed: {}'.format(
                    str(e)
                )
            )

    def test_fetch_l1_quote_on_unsupported_market(self):
        with self.assertRaises(ExchangeAPICallFailedException):
            g = GdaxExchange('LTC-GBP')
            g.fetch_l1_quote()

    def test_latest_l1_quote_to_csv(self):

        g = GdaxExchange('BTC-EUR')
        g.latest_l1_quote = {
            "best ask size": 0.65333759,
            "best bid price": 5780.1,
            "best ask price": 5781.24,
            "timestamp": datetime.utcnow(),
            "best bid size": 0.001006
        }
        g.latest_l1_quote_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/gdax_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_fetch_l1_quote_and_write_to_csv(self):

        g = GdaxExchange('BTC-EUR')
        with HiddenPrints():
            g.fetch_l1_quote_and_write_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/gdax_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)


class KrakenExchangeTests(unittest.TestCase):
    """
    Tests that functions within KrakenExchange class perform as intended.
    """

    def test_initialisation_with_valid_market(self):
        try:
            k = KrakenExchange('BTC-EUR')
            pass
        except KeyError:
            self.fail(
                'Initialising KrakenExchange with BTC-EUR raised KeyError.'
            )

    def test_initialisation_with_invalid_market(self):
        with self.assertRaises(KeyError):
            k = KrakenExchange('REDDDDDDDDDD-BLUEEEEEEEEEE')

    def test_fetch_l1_quote_on_supported_market(self):
        try:
            k = KrakenExchange('BTC-EUR')
            k.fetch_l1_quote()
            pass
        except Exception as e:
            self.fail(
                'Fetch l1 quote on supported market failed: {}'.format(
                    str(e)
                )
            )

    def test_fetch_l1_quote_on_unsupported_market(self):
        with self.assertRaises(ExchangeAPICallFailedException):
            k = KrakenExchange('LTC-GBP')
            k.fetch_l1_quote()

    def test_latest_l1_quote_to_csv(self):

        k = KrakenExchange('BTC-EUR')
        k.latest_l1_quote = {
            "best ask size": 0.65333759,
            "best bid price": 5780.1,
            "best ask price": 5781.24,
            "timestamp": datetime.utcnow(),
            "best bid size": 0.001006
        }
        k.latest_l1_quote_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/kraken_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_fetch_l1_quote_and_write_to_csv(self):

        k = KrakenExchange('BTC-EUR')
        with HiddenPrints():
            k.fetch_l1_quote_and_write_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/kraken_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)


class BitstampExchangeTests(unittest.TestCase):
    """
    Tests that functions within BitstampExchange class perform as intended.
    """

    def test_initialisation_with_valid_market(self):
        try:
            k = BitstampExchange('BTC-EUR')
            pass
        except KeyError:
            self.fail(
                'Initialising BitstampExchange with BTC-EUR raised KeyError.'
            )

    def test_initialisation_with_invalid_market(self):
        with self.assertRaises(KeyError):
            k = BitstampExchange('REDDDDDDDDDD-BLUEEEEEEEEEE')

    def test_fetch_l1_quote_on_supported_market(self):
        try:
            k = BitstampExchange('BTC-EUR')
            k.fetch_l1_quote()
            pass
        except Exception as e:
            self.fail(
                'Fetch l1 quote on supported market failed: {}'.format(
                    str(e)
                )
            )

    def test_fetch_l1_quote_on_unsupported_market(self):
        with self.assertRaises(ExchangeAPICallFailedException):
            k = BitstampExchange('LTC-GBP')
            k.fetch_l1_quote()

    def test_latest_l1_quote_to_csv(self):

        k = BitstampExchange('BTC-EUR')
        k.latest_l1_quote = {
            "best ask size": 0.65333759,
            "best bid price": 5780.1,
            "best ask price": 5781.24,
            "timestamp": datetime.utcnow(),
            "best bid size": 0.001006
        }
        k.latest_l1_quote_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/bitstamp_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_fetch_l1_quote_and_write_to_csv(self):

        k = BitstampExchange('BTC-EUR')
        with HiddenPrints():
            k.fetch_l1_quote_and_write_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/bitstamp_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)


class BitfinexExchangeTests(unittest.TestCase):
    """
    Tests that functions within BitfinexExchange class perform as intended.
    """

    def test_initialisation_with_valid_market(self):
        try:
            k = BitfinexExchange('BTC-EUR')
            pass
        except KeyError:
            self.fail(
                'Initialising BitfinexExchange with BTC-EUR raised KeyError.'
            )

    def test_initialisation_with_invalid_market(self):
        with self.assertRaises(KeyError):
            k = BitfinexExchange('REDDDDDDDDDD-BLUEEEEEEEEEE')

    def test_fetch_l1_quote_on_supported_market(self):
        try:
            k = BitfinexExchange('BTC-EUR')
            k.fetch_l1_quote()
            pass
        except Exception as e:
            self.fail(
                'Fetch l1 quote on supported market failed: {}'.format(
                    str(e)
                )
            )

    def test_fetch_l1_quote_on_unsupported_market(self):
        with self.assertRaises(ExchangeAPICallFailedException):
            k = BitfinexExchange('LTC-GBP')
            k.fetch_l1_quote()

    def test_latest_l1_quote_to_csv(self):

        k = BitfinexExchange('BTC-EUR')
        k.latest_l1_quote = {
            "best ask size": 0.65333759,
            "best bid price": 5780.1,
            "best ask price": 5781.24,
            "timestamp": datetime.utcnow(),
            "best bid size": 0.001006
        }
        k.latest_l1_quote_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/bitfinex_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)

    def test_fetch_l1_quote_and_write_to_csv(self):

        k = BitfinexExchange('BTC-EUR')
        with HiddenPrints():
            k.fetch_l1_quote_and_write_to_csv()

        # Test that csv file exists
        path = (
            os.path.dirname(os.path.realpath(__file__)) + '/bitfinex_BTC-EUR.csv'
        )
        self.assertTrue(os.path.exists(path))
        os.remove(path)


if __name__ == '__main__':
    unittest.main(exit=False)
