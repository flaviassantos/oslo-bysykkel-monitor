import sys
from flask import flash
from config import Config
import requests
import pandas as pd
from datetime import datetime, timezone


class StationStreamer:

    def __init__(self, config_class=Config):
        self.headers = {"Client-Identifier": config_class.CLIENT_IDENTIFIER}
        self.columns = ['station_id', 'name', 'num_bikes_available',
                        'num_docks_available', 'last_reported']
        self.url_info = config_class.URL_INFO
        self.url_status = config_class.URL_STATUS
        self.connection_string = config_class.DATABASE_URI
        self.table_name = "station"

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

    def parse_into_dataframe(self):
        """
        Reads data from a json format and parse it into a pandas.DataFrame.

        Returns
        ----------
        dataframe: pandas.DataFrame flat table which contains station data
        """
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
        df = df[(df['is_installed'] == 1) & (df['is_renting'] == 1)]
        df = df[self.columns]
        df['last_updated'] = last_updated
        df = df.loc[:, ~df.columns.duplicated()]
        df.sort_values(by='name', inplace=True)
        return df

    def select_data(self):
        """
        Keeps only the most relevant attributes of the station data.
        It saves the data selected to the database.

        Returns
        -------
        station_data: list which contains the station data in a dictionary format
        last_updated: string with formatted timestamp
        """""

        try:
            df = self.parse_into_dataframe()
            self.to_database(df)
            last_updated = df.loc[0, 'last_updated']
            station_data = list(df.T.to_dict().values())
            return station_data, last_updated
        except:
            flash(f"Oops! Exception: '{sys.exc_info()[0]}' occurred.")

    def to_database(self, dataframe):
        """
        Writes the most updated station data stored in a DataFrame to a SQL database.
        Table overwritten.

        Parameters
        ----------
        dataframe: pandas.DataFrame flat table which contains station data
        """
        con = self.connection_string
        dataframe.to_sql(self.table_name, con, if_exists="replace", index=False)
        return

    def from_database(self):
        """
        Reads the most updated station data stored into a SQL database to a DataFrame.

        Returns
        ----------
        dataframe: pandas.DataFrame flat table which contains station data
        """
        try:
            con = self.connection_string
            dataframe = pd.read_sql(f"SELECT * FROM {self.table_name}", con)
            return dataframe
        except:
            dataframe = self.parse_into_dataframe()
            self.to_database(dataframe)
            return dataframe
        finally:
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