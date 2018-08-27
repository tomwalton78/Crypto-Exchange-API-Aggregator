import os
import markdown
from flask import Flask, request
import flask_restful

from api.exchanges.exchange import ExchangeAPICallFailedException
from api.exchanges import (
    gdax_exchange, kraken_exchange, bitstamp_exchange, bitfinex_exchange
)

# Initialise Flask app
app = Flask(__name__)

# Initialise Flask restful
flask_api = flask_restful.Api(app)


@app.route('/')
def index():
    """Show api documentation"""

    # Open api README file
    with open(
        os.path.dirname(app.root_path) + '/api_server/API_README.md', 'r'
    ) as markdown_file:

        # Read file content
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class l1_quote(flask_restful.Resource):
    """Class for the l1_quote endpoint"""

    def get(self):
        """Function to be run when user makes a GET request to the l1_quote
        endpoint. Retrieves l1 quote for specified exchange and market, if they
        are valid.
        """

        # Parse input arguments
        args = request.args
        exchange = args['exchange']
        market = args['market']

        # Map input exchange strings to corresponding exchange object
        exchange_class_dict = {
            'gdax': gdax_exchange.GdaxExchange,
            'coinbase': gdax_exchange.GdaxExchange,
            'coinbase pro': gdax_exchange.GdaxExchange,
            'kraken': kraken_exchange.KrakenExchange,
            'bitstamp': bitstamp_exchange.BitstampExchange,
            'bitfinex': bitfinex_exchange.BitfinexExchange
        }

        try:
            # Select correct exchange object
            Ex = exchange_class_dict[exchange.lower()]
        except KeyError:
            return {'message': 'Failure: exchange not recognised'}, 400

        try:
            # Initialise exchange object
            ex = Ex(market)
        except KeyError:
            return {'message': 'Failure: market not recognised'}, 400

        try:
            # Fetch l1 quote
            ex.fetch_l1_quote()
        except ExchangeAPICallFailedException:
            return {
                'message': 'Failure: market not available on specified \
                exchange'.replace('  ', '')
            }, 400

        # Convert datetime object to timestamp, so it is able to be shown in
        # json format
        response_data = ex.latest_l1_quote
        response_data['timestamp'] = str(response_data['timestamp'])

        response = {
            'message': 'Success',
            'data': response_data
        }

        return response, 200


def shutdown_server():
    """Shutdown API server when called
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


# Shutdown API server when GET request is made to /shutdown endpoint
@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'


# Route endpoints to specific classes
flask_api.add_resource(l1_quote, '/l1_quote')


if __name__ == '__main__':

    # Run API server
    app.run(host='0.0.0.0', port=80, debug=True)
