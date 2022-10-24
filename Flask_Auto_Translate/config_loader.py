import configparser

from flask import Blueprint

config = configparser.ConfigParser()
config.read('flask_auto_translate_config.ini')
config_bp = Blueprint('config', __name__)