import csv
import os


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
        pass

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
            column_headers = [
                'timestamp',
                'best bid price', 'best bid size',
                'best ask price', 'best ask size'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=column_headers)

            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header

            writer.writerow(self.latest_l1_quote)
