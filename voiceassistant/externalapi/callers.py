# -*- coding: utf-8 -*-

import datetime
import time
import inflect
import requests
from tqdm import tqdm
import math
from unidecode import unidecode
import requests
from typing import Optional, List
import re
from ..core import state

_geos, _cryptos = set(), dict()


def load_geos() -> None:
    """
    Loads geo parameters for commands.
    """

    global _geos

    if len(_geos) > 0:
        return

    url = "https://geography2.p.rapidapi.com/cities"

    # api takes long to respond, fetch as many as possible
    total = 90_000
    page_size = 20_000
    iters = total / page_size

    for i in tqdm(range(1, math.ceil(iters))):
        querystring = {"page": str(i), "pageSize": str(page_size)}
        headers = {
            "X-RapidAPI-Key": state.args.apikey,
            "X-RapidAPI-Host": "geography2.p.rapidapi.com"
        }

        response = requests.request(
            "GET", url, headers=headers, params=querystring)
        if not response.ok:
            continue
        resp = response.json()
        for city in resp["cities"]:
            _geos.add(unidecode(city["name"]).lower())


def load_cryptos() -> None:
    """
    Loads crypto parameters for commands.
    """

    global _cryptos

    if len(_cryptos.values()) > 0:
        return

    url = "https://cryptocurrency-markets.p.rapidapi.com/coins"

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "cryptocurrency-markets.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    if not response.ok:
        raise Exception("Failed to fetch cryptos data")

    resp = response.json()
    for ind, tok in resp["result"].items():
        _cryptos[tok["name"].lower()] = tok["key"]


def get_params(command: str, dataset: List[str]) -> Optional[str]:
    """
    Fetches params from command. Complexity: O(n^2) (?)
    """

    if not dataset:
        raise Exception("Empty dataset!")

    # try 1...n token-groups
    tokens = re.split("\s+", command)
    for i in range(1, len(tokens) + 1):
        for j in range(0, math.ceil(len(tokens) / i)):
            gr = " ".join(tokens[j: j + i])
            if gr in dataset:
                return gr
    return None


def weather_api(loc: str):
    """
    Fetches weather data for the given loc.
    """

    # https://rapidapi.com/weatherapi/api/weatherapi-com/

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": loc}

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    json = response.json()
    current = json["current"]
    temperature = current["temp_c"]

    if temperature <= 0:
        return 'In ' + loc + ' it is very cold'

    if temperature > 0 and temperature <= 10:
        return 'In ' + loc + ' it is cold'

    if temperature > 10 and temperature <= 20:
        return 'In ' + loc + ' it is pleasant'

    if temperature > 20 and temperature <= 30:
        return 'In ' + loc + ' it is warm'

    if temperature > 30:
        return 'In ' + loc + ' it is hot'


def crypto_api(coin: str) -> str:
    """
    Fetches the price of the given crypto
    coin.
    """
    global _cryptos

    url = "https://cryptocurrency-markets.p.rapidapi.com/coin/quote"

    if not _cryptos:
        raise Exception("cryptos not loaded!")

    querystring = {"key": _cryptos[coin]}

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "cryptocurrency-markets.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    if not response.ok:
        raise Exception("Failed to fetch cryptos data!")

    price = int(response.json()["result"]["price"])

    price_worded = inflect.engine().number_to_words(price)

    return f"one {coin} is worth {price_worded} dollars"


def time_api() -> str:
    """
    Fetches the current time.
    """
    res = time.localtime(time.time())
    eng = inflect.engine()
    return f"The time is {eng.number_to_words(res.tm_hour)} and {eng.number_to_words(res.tm_min)}"


def joke_api() -> str:
    """
    Fetches a joke from an API.
    """

    # https://rapidapi.com/KegenGuyll/api/dad-jokes

    url = "https://dad-jokes.p.rapidapi.com/random/joke"

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "dad-jokes.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    if not response.ok:
        raise Exception("Failed to call jokes api!")

    response = response.json()["body"][0]

    return response["setup"] + " " + response["punchline"]


def flights_api(loc: str) -> str:
    """
    Finds flight data for 7 days from now.
    """

    # https://rapidapi.com/DataCrawler/api/tripadvisor16/

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchAirport"

    querystring = {"query": loc}

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    print(response)
    if not response.ok:
        raise Exception("Failed to get flight data!")

    response = response.json()
    if not response["data"]:
        return f"I could not find any flights to {loc}"

    # hardcoded belgrade origin
    orig = "BEG"

    dest = response["data"][0]["airportCode"]

    date = datetime.date.today() + datetime.timedelta(days=7)
    date = date.strftime("%Y-%m-%d")

    url = "https://tripadvisor16.p.rapidapi.com/api/v1/flights/searchFlights"

    querystring = {
        "sourceAirportCode": orig,
        "destinationAirportCode": dest,
        "date": date,
        "itineraryType": "ONE_WAY",
        "sortOrder": "ML_BEST_VALUE",
        "numAdults": "1",
        "numSeniors": "0",
        "classOfService": "ECONOMY",
        "currencyCode": "USD"
    }

    headers = {
        "X-RapidAPI-Key": state.args.apikey,
        "X-RapidAPI-Host": "tripadvisor16.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    response = response.json()
    if (not response["data"]) or (not response["data"]["flights"]):
        return f"I could not find any flights to {loc}"

    num_flights = len(response["data"]["flights"])
    price = int(response["data"]["flights"][0]
                ["purchaseLinks"][0]["totalPrice"])
    price_worded = inflect.engine().number_to_words(price)
    return f"Found {num_flights} to {loc} at {price_worded} dollars"
