from flask import Flask
from db_module.dbconnectors import SqliteConnector

db_conn = SqliteConnector('D:\\shadi\\PythonProjects\\pdf-information-extraction\\articlesdb.db')

app = Flask(__name__)

app.config["SECRET_KEY"] = 'd2da0f829ebe66aa0f5942055e83166dceee0e2c1fc6a88220a72d06671ea068'

param, uri, driver = db_conn.export_flask_config()
db = driver
app.config[param] = uri
db.init_app(app)

from server_module import routes