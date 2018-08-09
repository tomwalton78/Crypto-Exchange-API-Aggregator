from datetime import datetime
import csv
import os

import api_common_functions as api_cf


class KrakenExchange():

    def __init__(self, market):
        self.market = market
        pass

    def fetch_l1_quote(self):
        # Make api call
        data = api_cf.fetch_data_from_url(
            'https://api.kraken.com/0/public/Ticker?pair={}'.format(
                self.market
            )
        )

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

    def latest_l1_quote_to_csv(self):
        file_name = 'datasets/kraken_{}.csv'.format(self.market)
        file_exists = os.path.isfile(file_name)  # check if file already exists

        with open(file_name, 'a') as csvfile:
            column_headers = [
                'timestamp',
                'best bid price', 'best bid size',
                'best ask price', 'best ask size'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)

            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerow(self.latest_l1_quote)


if __name__ == '__main__':
    k = KrakenExchange('ETHEUR')
    k.fetch_l1_quote()
    k.latest_l1_quote_to_csv()
