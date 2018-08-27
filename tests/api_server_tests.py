import unittest
import requests
import json

import api.api_server.api_server as api_server

# MAKE SURE API SERVER IS RUNNING BEFORE RUNNING THIS SCRIPT


class APIServerTests(unittest.TestCase):

    def test_api_server_root(self):

        # Make GET request
        response = requests.request('GET', 'http://localhost/')

        expected_content = '<h1>API Server Documentation</h1>'

        # parse response
        response_content = response.text

        # Check first line of response is as expected
        if response_content[:33] == expected_content:
            pass
        else:
            self.fail(
                """First line of root endpoint response does
                not match expected string."""
            )

    def test_GET_fetch_l1_quote_valid_input(self):

        # Make GET request
        response = requests.request(
            'GET',
            'http://localhost/l1_quote?exchange=kraken&market=BTC-EUR'
        )

        # parse response to json
        response_content = response.text
        json_content = json.loads(response_content)

        # Check returned message is as expected
        if json_content['message'] == 'Success':
            pass
        else:
            self.fail('GET l1_quote on kraken for BTC-EUR market failed.')

    def test_GET_fetch_l1_quote_invalid_exchange_input(self):

        # Make GET request
        response = requests.request(
            'GET',
            'http://localhost/l1_quote?exchange=hubawuba&market=BTC-EUR'
        )

        # parse response to json
        response_content = response.text
        json_content = json.loads(response_content)

        # Check returned message is as expected
        if json_content['message'] == 'Failure: exchange not recognised':
            pass
        else:
            self.fail(
                'GET l1_quote on invalid exchange returned incorrect message.'
            )

    def test_GET_fetch_l1_quote_invalid_market_input(self):

        # Make GET request
        response = requests.request(
            'GET',
            'http://localhost/l1_quote?exchange=kraken&market=BTCCCCCX-UUY'
        )

        # parse response to json
        response_content = response.text
        json_content = json.loads(response_content)

        # Check returned message is as expected
        if json_content['message'] == 'Failure: market not recognised':
            pass
        else:
            self.fail(
                'GET l1_quote on invalid market returned incorrect message.'
            )


# MAKE SURE TO SHUT DOWN API SERVER AFTER RUNNING THIS SCRIPT

if __name__ == '__main__':
    unittest.main(exit=False)
