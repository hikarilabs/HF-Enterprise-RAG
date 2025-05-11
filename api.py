import requests

from requests import RequestException
from typing import Dict, Any, Union, List


def api_call(query: List[str], url: str, headers: Dict) -> Union[Dict[str, Any], None]:
    """
    Generic python requests api call
    :param query: api query as a list of query strings e.g. ["Can you explain the weather?"]
    :param url: the URL of the api
    :param headers: required api headers such as auth and content type
    :return: it either returns:
                the API response as a JSON payload or
                None if either ValueError or RequestError exceptions are thrown
    """
    payload = {
        "query": query
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            try:
                json_data = response.json()
                return json_data
            except ValueError as vex:
                print(f"No JSON data in the response. Error: {vex} ")
                return None
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    except RequestException as rex:
        print(f"Error during request: {rex}")
        return None
