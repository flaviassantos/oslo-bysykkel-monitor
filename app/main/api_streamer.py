import sys
from flask import flash
from config import Config
import requests
import pandas as pd
from datetime import datetime, timezone


class StationStreamer:

    def __init__(self):
        self.headers = {"Client-Identifier": Config.CLIENT_IDENTIFIER}
        self.columns = ['station_id', 'name', 'num_bikes_available',
                        'num_docks_available', 'last_reported']
        self.url_info = Config.URL_INFO
        self.url_status = Config.URL_STATUS

    def fetch_api_data(self, url=None):
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
        response_body['data']['stations']: json data
        last_updated: integer representing the elapsed time in number of seconds

        """
        try:
            response = requests.get(url, self.headers)
            response_body = response.json()
            return response_body
        except requests.exceptions.RequestException as e:
            raise e

    def get_station_data(self):
        """
        Reads data into json format and parse it into a pandas.DataFrame.
        Keeps only the most relevant attributes of the station data.

        Parameters
        ----------
        config_class

        Returns
        -------
        station_data: list which contains the station data in a dictionary format
        last_updated: string with formatted timestamp

        """
        try:
            # Station information
            data_info = self.fetch_api_data(self.url_info)  # json
            dict_info = data_info['data']['stations']

            # Station status
            data_status = self.fetch_api_data(self.url_status)  # json
            dict_status = data_status['data']['stations']
            last_updated = data_status['last_updated']
            last_updated = parse_datetime(last_updated)

            # Parse into dataframe and merge by 'station_id'
            df_status = pd.DataFrame(dict_status)
            df_info = pd.DataFrame(dict_info)
            df = pd.concat([df_info, df_status], sort=False, axis=1, join='outer')
            df = df[df['is_installed'] == 1]
            df = df[self.columns]
            df = df.loc[:, ~df.columns.duplicated()]
            df.sort_values(by='name', inplace=True)
            station_data = list(df.T.to_dict().values())
            return station_data, last_updated

        except:
            flash(f"Oops! Exception: '{sys.exc_info()[0]}' occurred.")


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
    dt = datetime.fromtimestamp(date_time, timezone.utc).strftime("%B %d, %Y %I:%M:%S")
    return dt