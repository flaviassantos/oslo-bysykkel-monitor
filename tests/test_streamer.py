import requests
from app.main.api_streamer import fetch_api_data, parse_datetime, get_station_data

URL_STATUS = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"
URL_INFO = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"
CLIENT_IDENTIFIER = "flavia-oslobysykkelmonitor"
HEADERS = {"Client-Identifier": CLIENT_IDENTIFIER}


class TestFetchAPIData:
    def test_api_response_status(self):
        resp_status = requests.get(URL_STATUS, headers=HEADERS)
        resp_info = requests.get(URL_INFO, headers=HEADERS)
        assert resp_status.status_code == 200
        assert resp_info.status_code == 200

    def test_api_response_body(self):
        rep_status_body = fetch_api_data(URL_STATUS)
        resp_info_body = fetch_api_data(URL_INFO)

        assert "data" in rep_status_body
        assert "stations" in rep_status_body["data"]

        assert "data" in resp_info_body
        assert "stations" in resp_info_body["data"]


def test_parse_datetime():
    last_updated = 1584862677
    expected = 'March 22, 2020 08:37:57'
    actual = parse_datetime(last_updated)
    assert expected == actual


def test_get_station_data():
    expected_attributes = ['station_id', 'name', 'num_bikes_available', 'num_docks_available', 'last_reported']

    station_data, last_updated = get_station_data()
    actual_attributes = [k for k, v in station_data[0].items()]

    assert expected_attributes == actual_attributes
    assert len(station_data) > 0
    assert type(last_updated) == str