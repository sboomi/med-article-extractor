from flask_sqlalchemy import SQLAlchemy
from pymongo import MongoClient


class DbConnector:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password


class PostGreSqlConnector(DbConnector):
    def __init__(self, uri, username, password):
        super().__init__(uri, username, password)
        self.driver = SQLAlchemy()


class SqliteConnector(DbConnector):
    def __init__(self, path):
        self.uri = "sqlite:///" + path
        self.driver = SQLAlchemy()

    def export_flask_config(self):
        return "SQLALCHEMY_DATABASE_URI", self.uri, SQLAlchemy()

    def create_database(self):
        pass

    def read_table(self, table, columns=None):
        pass


class MongoDbConnector(DbConnector):
    def __init__(self, uri, username, password):
        super().__init__(uri, username, password)
        self.driver = MongoClient(self.uri)
        self.db = self.driver.get_default_database()

    def connect_with_host_port(self, host='localhost', port=27017):
        self.driver = MongoClient(host, port)
        return f"Connected to {host}:{port}..."

    def select_database(self, dbname):
        self.db = self.driver[dbname]
        return f"Switched to {dbname}"

    def export_flask_config(self):
        return "MONGO_URI", self.uri


class Neo4jConnector(DbConnector):
    def __init__(self, uri, username, password):
        super().__init__(uri, username, password)
