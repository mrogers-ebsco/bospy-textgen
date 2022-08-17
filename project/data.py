# Data Module: Contains methods for getting data from the NWS API,
# and classes for various data objects used in the pipeline.

from dataclasses import dataclass
import json
import os
from typing import Tuple, List
import pandas as pd
import requests


# Request API parameters for a particular latitude and longitude
def get_parameters_at(latitude: float, longitude: float) -> Tuple[str, int, int]:
    url = f'https://api.weather.gov/points/{latitude},{longitude}'
    response = requests.get(url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        response.raise_for_status()

    content = response.content.decode()
    content_json = json.loads(content)
    office = content_json['properties']['gridId']
    gridx = content_json['properties']['gridX']
    gridy = content_json['properties']['gridY']

    return office, gridx, gridy


# Request forecast data from the NWS API, and return the response content as a JSON-formatted string
def get_forecast(office: str, gridx: int, gridy: int) -> str:
    url = f'https://api.weather.gov/gridpoints/{office}/{gridx},{gridy}/forecast'
    response = requests.get(url)

    # Raise an exception if the request was unsuccessful
    if response.status_code != 200:
        response.raise_for_status()

    # Extract the forecast records from the JSON-formatted payload
    return response.content.decode()


# Extract daily forecast data from the serialized API response content, returning it as a pandas.DataFrame
def extract_forecast_data(forecast: str) -> pd.DataFrame:
    fc_json = json.loads(forecast)
    fc_records = fc_json['properties']['periods']

    # Create a pandas.DataFrame from the forecast records
    df = pd.DataFrame.from_records(fc_records)

    # Return the data frame
    return df


# Main Pipeline: Input latitude and longitude, output forecast in a pandas.DataFrame
def get_forecast_data_at(latitude: float, longitude: float) -> pd.DataFrame:
    office, gridx, gridy = get_parameters_at(latitude, longitude)
    forecast = get_forecast(office=office, gridx=gridx, gridy=gridy)
    df = extract_forecast_data(forecast)
    return df


# Useful coordinates for testing/debugging
test_coordinates = {
    'Somerville, MA': (42.396592, -71.122389),
    'Chicago, IL': (41.979138, -97.908431),
    'Denver, CO': (39.846457, -104.673739),
    'Newark, NJ': (40.691853, -74.180681),
    'Orlando, FL': (28.375286, -81.549377),
    'Phoenix, AZ': (33.449039, -112.067054),
    'Portland, ME': (43.656055, -70.252184),
    'Seattle, WA': (47.619950, -122.349235)
}


# Function to get the local forecast data - Use for live demo
def api_demo():
    lat, lon = test_coordinates['Somerville, MA']
    return get_forecast_data_at(lat, lon)


# Use in place of get_forecast_data_at() if the NWS API is down during live demo
def get_emergency_data():
    module_path = os.path.dirname(__file__)
    fp = os.path.join(module_path, 'sampledata.json')
    with open(fp, 'r') as file:
        return extract_forecast_data(file.read())


# Data Objects

# Messages
@dataclass
class Message:
    relation: str
    arguments: dict


# Text plans
@dataclass
class TextPlan:
    messages: List[Message]


# Sentence plans
@dataclass
class SentencePlan:
    subject: str
    verb: str
    objects: List[str]
