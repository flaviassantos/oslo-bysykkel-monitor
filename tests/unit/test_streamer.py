import os
import pytest
import requests
from app.main.streamer import StationStreamer, parse_datetime
import pandas as pd
from config import Config


class TestConfig:
    DATABASE_URI = 'sqlite:///test.db'
    URL_STATUS = Config.URL_STATUS
    URL_INFO = Config.URL_INFO
    CLIENT_IDENTIFIER = Config.CLIENT_IDENTIFIER


def tear_down_db():
    os.remove('test.db')


@pytest.fixture(scope='module')
def df():
    data = {"station_id": ["111"],
            "name": ["Ensjø T-bane"],
            "num_bikes_available": [11],
            "num_docks_available": [8],
            "last_reported": [1540219230],
            "last_updated": ['March 22, 2020 07:37:57']
            }
    df = pd.DataFrame.from_dict(data)
    return df


@pytest.fixture(scope='module')
def streamer():
    return StationStreamer(TestConfig)


def test_api_response_status(streamer):
    resp_status = requests.get(streamer.url_status, headers=streamer.headers)
    resp_info = requests.get(streamer.url_info, headers=streamer.headers)
    assert resp_status.status_code == 200
    assert resp_info.status_code == 200


def test_api_response_body(streamer):
    rep_status_body = streamer.fetch_api_data(streamer.url_status)
    resp_info_body = streamer.fetch_api_data(streamer.url_info)

    assert "data" in rep_status_body
    assert "stations" in rep_status_body["data"]

    assert "data" in resp_info_body
    assert "stations" in resp_info_body["data"]


def test_parse_into_dataframes(streamer, df):
    expected_attributes = df.columns
    df_actual = streamer.parse_into_dataframe()
    assert all([a == b for a, b in zip(df_actual.columns, expected_attributes)])
    assert len(df_actual) > 0


def test_select_data(streamer, df):
    expected_attributes = df.columns.to_list()
    station_data, last_updated = streamer.select_data()
    actual_attributes = [k for k, v in station_data[0].items()]

    assert actual_attributes == expected_attributes
    assert len(station_data) > 0
    assert type(last_updated) == str


def test_save_data_to_database(streamer, df):
    streamer.to_database(df)
    db_table = pd.read_sql(f"SELECT * FROM {streamer.table_name}", con=streamer.connection_string)
    assert len(db_table) > 0
    tear_down_db()


def test_parse_datetime():
    last_updated = 1584862677
    expected = 'March 22, 2020 07:37:57'
    actual = parse_datetime(last_updated)
    assert actual == expected