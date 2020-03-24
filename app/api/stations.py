from app.api import bp
from app.main.streamer import StationStreamer


@bp.route('/stations', methods=['GET'])
def get_stations():
    """
    Endpoint which returns the collection of all stations in a JSON format.

    Representing station as JSON objects:
        [
            {|
                "last_reported": 1585031881,
                "last_updated": "March 24, 2020 06:38:01",
                "name": "Vår Frelsers gravlund sør",
                "num_bikes_available": 2,
                "num_docks_available": 16,
                "station_id": "384"
            },
            {
                "last_reported": 1585031881,
                "last_updated": "March 24, 2020 06:38:01",
                "name": "Økernveien",
                "num_bikes_available": 0,
                "num_docks_available": 24,
                "station_id": "605"
            }
        ]
    """
    streamer = StationStreamer()
    data = streamer.from_database()
    return data.to_json(orient='records')



# @bp.route('/stations/<str:name>', methods=['GET'])
# def get_station(name):
#     """
#     Return a station.
#
#     Parameters
#     ----------
#     name
#
#     Returns
#     -------
#
#     """
#     pass
