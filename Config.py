import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key'
    URL_STATUS = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"
    URL_INFO = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"