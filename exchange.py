import csv
from datetime import datetime
import os
import json
import traceback


class Exchange():
    """General object representing a cryptocurrency exchange
    """

    def __init__(self, exchange_name):
        """Intiialise Exchange object for a particular exchange

        Parameters
        ----------
        exchange_name : str
            Name of cryptocurrency exchange

        """

        self.exchange_name = exchange_name

        # Load exchange details from json file
        with open('{}_exchange.json'.format(exchange_name), 'r') as f:
            self.exchange_info = json.load(f)

    def _parse_market(self, market):
        """Parse input market string to exchange specific form

        Returns
        -------
        str
            Parsed market string, in exchange's format
        """

        # Extract input (universal) currency tickers
        currency_1 = market.split('-')[0]
        currency_2 = market.split('-')[1]

        # Convert tickers to exchange specific form
        currency_1_parsed = self.exchange_info['currency_mapping'][currency_1]
        currency_2_parsed = self.exchange_info['currency_mapping'][currency_2]

        market_ticker_delimiter = self.exchange_info['market_ticker_delimiter']

        return currency_1_parsed + market_ticker_delimiter + currency_2_parsed

    def latest_l1_quote_to_csv(self, path_to_folder='datasets/'):
        """Write stored details of latest level 1 quote to csv file

        Parameters
        ----------
        path_to_folder : str, optional
            Relative path to folder containing csv file datasets

        """

        file_name = '{}{}_{}.csv'.format(
            path_to_folder, self.exchange_name, self.market
        )
        file_exists = os.path.isfile(file_name)  # check if file already exists

        with open(file_name, 'a') as csvfile:
            # Define table headings in csv file
            column_headers = [
                'timestamp',
                'best bid price', 'best bid size',
                'best ask price', 'best ask size'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)

            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerow(self.latest_l1_quote)  # write quote to csv file

    def fetch_l1_quote_and_write_to_csv(self, path_to_folder='datasets/'):
        """Fetch l1 quote using exchange api and write to csv in same function

        Parameters
        ----------
        path_to_folder : str, optional
            Relative path to folder containing csv file datasets

        """
        try:
            self.fetch_l1_quote()
            self.latest_l1_quote_to_csv(path_to_folder=path_to_folder)
            print(self.exchange_name, self.market, datetime.utcnow())
        except Exception as e:
            print('\n\n\n', traceback.format_exc(), '\n\n\n')
