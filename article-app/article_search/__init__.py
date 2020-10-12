from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config["SECRET_KEY"] = '9e32b142c65b8de40a85a5e47bc85b2f66b847309cc683d68dab7033e913d15e'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + 'D:\\shadi\\PythonProjects\\pdf-information-extraction' \
                                                       '\\articlesdb.db '

from article_search import routes