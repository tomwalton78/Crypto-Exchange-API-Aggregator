from datetime import datetime
import csv
import os

import api_common_functions as api_cf


class GdaxExchange():

    def __init__(self, market):
        self.market = market
        pass

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

    def latest_l1_quote_to_csv(self):
        file_name = 'datasets/gdax_{}.csv'.format(self.market)
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
    g = GdaxExchange('ETH-EUR')
    g.fetch_l1_quote()
    g.latest_l1_quote_to_csv()
    print(g.latest_l1_quote)
