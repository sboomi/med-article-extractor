from flask import Flask

app = Flask(__name__)

app.config["SECRET_KEY"] = '9e32b142c65b8de40a85a5e47bc85b2f66b847309cc683d68dab7033e913d15e'

from article_search import routes