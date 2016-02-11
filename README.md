# AIC_mezzanine_site

This repo contains website source code of [Sharif AI Challnges](http://aichallenge.sharif.edu/).
We made it based on [Mezzanine CMS](https://github.com/stephenmcd/mezzanine/).

## Requirements
* `AIC_mezzanine_site` files!
* An environment with installed python requirements! (see `requirements.txt`)

## Installation

To run this project on your own computer, you must:

* Have **a running redis server**:
If redis server is running, the response of command `redis-cli ping` must be `PONG`.

* Have **a DataStore**:
We highly recommend PostgreSQL for deployment and SQLite for development environment. DBMS settings must be set on `local_settings.py`.
A file named `dev.db.sample` is a sample and also simple development SQLite DB to work on.
   
* Have **a running SMTP server** (maybe a dummy one!):
Running a Debugging SMTP server is as easy as running (root privilege is required):
```sh
python3 -m smtpd -n -c DebuggingServer localhost:25
```

* Configure **`local_settings.py`**:
some important settings are extracted to a python file named `local_settings.py` in `AIC_site` directory.
Two samples named `local_settings.deploy.sample.py` and `local_settings.dev.sample.py` are available in that directory.

* Run celery **mail workers**: 
```sh
celery worker -A AIC_site -Q mail_queue
```

* Run celery **compile workers**:
read more at [AIC_game_runner](https://github.com/SharifAIChallenge/AIC_game_runner).
Note: this worker is not required if you are not interested in compiling uploaded codes.

* Run celery **game workers**:
read more at [AIC_game_runner](https://github.com/SharifAIChallenge/AIC_game_runner).
Note: this worker is not required if you are not interested in running uploaded games.
