import api_common_functions as api_cf


class KrakenExchange():

    def __init__(self):
        pass

    def fetch_quote(ticker_string):
        data = api_cf.fetch_data_from_url(
            'https://api.kraken.com/0/public/Ticker?pair={}'.format(
                ticker_string
            )
        )

        ticker = list(data['result'].keys())[0]
        best_bid_price = float(data['result'][ticker]['b'][0])
        best_ask_price = float(data['result'][ticker]['a'][0])

        return best_bid_price, best_ask_price


if __name__ == '__main__':
    k = KrakenExchange
    best_bid_price, best_ask_price = k.fetch_quote('ETHEUR')

    print('best bid price: ', best_bid_price)
    print('best ask price: ', best_ask_price)
