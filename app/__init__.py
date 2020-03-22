from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import os
from logging.handlers import RotatingFileHandler
import logging


bootstrap = Bootstrap()


def create_app(config_class=Config):
    """
    Constructs a Flask application instance.

    Parameters
    ----------
    config_class: class that stores the configuration variables.

    Returns
    -------
    app : Flask application
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    bootstrap.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/oslo-bysykkel-monitor.log',
                                           maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Oslo Bysykkel Monitor startup')
    return app