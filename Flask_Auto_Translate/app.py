import datetime as dt
import os

import dl_translate as dlt
from flask import Flask

from Flask_Auto_Translate.config_loader import config
from Flask_Auto_Translate.schedule import ScheduleManager
from Flask_Auto_Translate.flask_auto_translate_logger import logger_handler

LOG_LEVEL = config['DEFAULT']['LOG_LEVEL']

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.logger.addHandler(logger_handler)
app.logger.setLevel(LOG_LEVEL)
app.config['PERMANENT_SESSION_LIFETIME'] = dt.timedelta(hours=2)
app.config['SECRET_KEY'] = os.urandom(32)
app.logger.debug("Starting Flask Auto Translate service...")


def load_mt():
    model_name = config['DEFAULT']["model"]
    app.logger.debug("Load model:" + model_name)
    return dlt.TranslationModel(model_name)


def initialize():
    mt = load_mt()
    app.logger.debug("Load finished")
    app.logger.debug("Flask Auto Translate Mode: " + config['DEFAULT']["mode"] + " Start!")
    ScheduleManager.start(mt)
