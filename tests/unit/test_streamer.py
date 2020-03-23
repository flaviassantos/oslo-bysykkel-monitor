import pytest
import requests
from app.main.api_streamer import StationStreamer, parse_datetime


@pytest.fixture(scope='module')
def streamer():
    return StationStreamer()


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


def test_parse_datetime():
    last_updated = 1584862677
    expected = 'March 22, 2020 07:37:57'
    actual = parse_datetime(last_updated)
    assert actual == expected