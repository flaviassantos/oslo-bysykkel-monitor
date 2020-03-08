# Welcome to Oslo Bysykkel Monitor !

This project contains a simple Python application for working with an open API (in this case the [Oslo Bysykkel](https://oslobysykkel.no/apne-data/sanntid).

![HOME PAGE](app/static/assets/img/home.png)

## Introduction
The app shows a list of the various bike stations and how many available locks and available bikes are on them at the moment.
 
To update the data, just refresh the browser or click in the _'Explore all the stations'_ link.


### Monitor Features
- Modular design with **Blueprints**

### Product technology stack
- Used Language: [Python3](https://www.python.org/)
- Web Framework: [Flask](https://www.palletsprojects.com/p/flask/)

<br />
## How to use it

```bash
$ # Get the code
$ git clone https://github.com/flaviassantos/oslo-bysykkel-monitor.git
$ cd oslo-bysykkel-monitor
$
$ # Virtualenv modules installation (Unix based systems)
$ virtualenv --no-site-packages venv
$ source venv/bin/activate
$
$ # Virtualenv modules installation (Windows based systems)
$ # virtualenv --no-site-packages venv
$ # .\venv\Scripts\activate
$
$ # Install modules
$ pip install -r requirements.txt
$
$ # Set the FLASK_APP environment variable
$ (Unix/Mac) export FLASK_APP=monitor_run.py
$ (Windows) set FLASK_APP=monitor_run.py
$ (Powershell) $env:FLASK_APP = ".\monitor_run.py"
$
$ # Start the application
$ flask run
$
$ # Access the monitor in browser: http://127.0.0.1:5000/
```
<br />

```
@misc{Flavia: 2020,
  Author = {Flavia Santos},
  Title = {Oslo Bysykkel Monitor},
  Year = {2020},
  Publisher = {GitHub},
  Journal = {GitHub repository},
  Howpublished = {\url{https://github.com/flaviassantos/oslo-bysykkel-monitor.git}}
}
```