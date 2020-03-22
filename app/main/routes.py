from werkzeug.utils import redirect
from flask import render_template, flash
from app.main import bp
from app.main.api_streamer import get_station_data


@bp.route('/')
@bp.route('/index')
def index():
    """
    Renders the home page of the application.
    """
    try:
        stations, last_updated = get_station_data()
        return render_template('index.html', stations=stations, last_updated=last_updated)
    except:
        flash("Not possible to retrieve data from the API. "
              "Please contact the administrator")


@bp.route('/linkedin_profile')
def linkedin_profile():
    """
    Renders the profile page of the application's author.
    """
    return redirect("https://www.linkedin.com/in/flaviasouzasantos")


@bp.route('/oslo_byssykkel')
def oslo_bysykkel():
    """
    Renders the home page for Oslo Bysykkel.
    """
    return redirect("https://oslobysykkel.no/")
