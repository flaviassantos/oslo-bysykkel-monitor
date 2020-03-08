from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)


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

    return app