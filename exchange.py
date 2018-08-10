import csv
import os


class Exchange():

    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        pass

    def latest_l1_quote_to_csv(self, path_to_folder='datasets/'):
        file_name = '{}{}_{}.csv'.format(
            path_to_folder, self.exchange_name, self.market
        )
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
    pass
    # g = GdaxExchange('ETH-EUR')
    # g.fetch_l1_quote()
    # g.latest_l1_quote_to_csv()
    # print(g.latest_l1_quote)
