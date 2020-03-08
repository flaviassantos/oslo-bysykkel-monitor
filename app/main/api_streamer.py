import sys
from flask import flash
from config import Config
import requests
import pandas as pd
from datetime import datetime

CLIENT_IDENTIFIER = {'Client-Identifier': 'flavia-oslobysykkelmonitor'}


def fetch_api_data(url=None, headers=None):
    """
    Streams data from Oslo Bysykkel open API into a json format.
    Selects the most appropriate attributes of the station data
    ('data', 'station' and 'last_updated').

    Parameters
    ----------
    url = string with the url to request from
    headers =  dictionary with the client identifier required

    Returns
    -------
    response['data']['stations']: json data
    last_updated: integer representing the elapsed time in number of seconds

    """
    try:
        response = requests.get(url=url, headers=headers).json()
        last_updated = response['last_updated']
        return response['data']['stations'], last_updated
    except AttributeError as e:
        raise e


def parse_datetime(date_time=None):
    """
    Formats the timestamp into a nice readable format such as 'March 08, 2020 10:16:48'.

    Parameters
    ----------
    date_time: integer representing the elapsed time in number of seconds

    Returns
    -------
    dt: string with the formatted timestamp
    """
    dt = datetime.fromtimestamp(date_time).strftime("%B %d, %Y %I:%M:%S")
    return dt


def get_station_data(config_class=Config):
    """
    Reads data into json format and parse it into a pandas.DataFrame.
    Keeps only the most relevant attributes of the station data.

    Parameters
    ----------
    config_class

    Returns
    -------
    station_data: list with the station data as a dictionary
    last_updated: string with formatted timestamp

    """
    try:
        columns = ['station_id', 'name', 'num_bikes_available',
                   'num_docks_available', 'last_reported']
        headers = CLIENT_IDENTIFIER
        dict_info, _ = fetch_api_data(url=config_class.URL_INFO, headers=headers)
        dict_status, last_updated = fetch_api_data(url=config_class.URL_STATUS, headers=headers)
        last_updated = parse_datetime(last_updated)

        # Parse into dataframe and merge by 'station_id'
        df_status = pd.DataFrame(dict_status)
        df_info = pd.DataFrame(dict_info)
        df = pd.concat([df_info, df_status], sort=False, axis=1, join='outer')
        df = df[df['is_installed'] == 1]
        df = df[columns]
        df = df.loc[:, ~df.columns.duplicated()]
        df.sort_values(by='name', inplace=True)
        station_data = list(df.T.to_dict().values())
        return station_data, last_updated

    except:
        flash(f"Oops! Exception: '{sys.exc_info()[0]}' occurred.")
