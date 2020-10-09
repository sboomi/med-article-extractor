from flask import Flask
from modelmodule.config import Config

app = Flask(__name__)

app.config.from_object(Config())

from modelmodule import routes