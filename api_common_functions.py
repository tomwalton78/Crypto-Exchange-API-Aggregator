import requests
import json


def fetch_data_from_url(url):
    response = requests.request("GET", url)
    response_content = response.text
    parsed_to_list = json.loads(response_content)
    return parsed_to_list
