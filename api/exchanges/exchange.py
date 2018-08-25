import csv
from datetime import datetime
import os
import json
import traceback
import requests
import pkg_resources

# __name__ in case you're within the package
# - otherwise it would be 'lidtk' in this example as it is the package name
path = 'classifiers/text_cat/REAMDE.md'  # always use slash
filepath = pkg_resources.resource_filename(__name__, path)


class Exchange():
    """General object representing a cryptocurrency exchange
    """

    def __init__(self, exchange_name, market):
        """Intiialise Exchange object for a particular exchange

        Parameters
        ----------
        exchange_name : str
            Name of cryptocurrency exchange

        market : str
            Market (i.e. trading pair) that this instance will interact with

        """

        self.exchange_name = exchange_name

        # Load exchange details from json file
        json_rel_path = '/exchange_info/{}_exchange.json'.format(exchange_name)
        json_path = pkg_resources.resource_filename(__name__, json_rel_path)
        with open(
            json_path, 'r'
        ) as f:
            self.exchange_info = json.load(f)

        # Store market in unparsed form
        self.raw_market = market

        # Define market, parsed to exchange specific form
        self.market = self._parse_market(market)

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

    def latest_l1_quote_to_csv(self, path_to_folder=''):
        """Write stored details of latest level 1 quote to csv file

        Parameters
        ----------
        path_to_folder : str, optional
            Relative path to folder containing csv file datasets

        """

        file_name = '{}{}_{}.csv'.format(
            path_to_folder, self.exchange_name, self.raw_market
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

    def fetch_l1_quote_and_write_to_csv(self, path_to_folder=''):
        """Fetch l1 quote using exchange api and write to csv in same function

        Parameters
        ----------
        path_to_folder : str, optional
            Relative path to folder containing csv file datasets

        """

        try:
            self.fetch_l1_quote()
            self.latest_l1_quote_to_csv(path_to_folder=path_to_folder)
            print(
                self.exchange_name.ljust(10),
                self.raw_market.ljust(10),
                str(datetime.utcnow()).ljust(30)
            )
        except Exception as e:
            print('\n\n\n', traceback.format_exc(), '\n\n\n')

    def raise_failed_api_call_error(self):
        """Raise ExchangeAPICallFailedException, with useful error message
        """

        raise ExchangeAPICallFailedException(
            'API call failed. \
            Check that {} market exists on the {} exchange.'.format(
                self.market, self.exchange_name
            ).replace('  ', '')
        )

    def _make_and_parse_GET_request(self, url):
        """Make GET request to specified url, parsing JSON response to a
        dictionary

        Parameters
        ----------
        url : str
            Url to make GET request to

        Returns
        -------
        dict
            Parsed JSON response as python dictionary

        """

        # Make GET request
        response = requests.request("GET", url)

        # parse json content to python dictionary
        response_content = response.text
        parsed_to_list = json.loads(response_content)

        return parsed_to_list


class ExchangeAPICallFailedException(Exception):
    """Error representing a failed call to an exchange's API"""
    pass
