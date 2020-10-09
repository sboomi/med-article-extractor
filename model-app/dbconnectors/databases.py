from sqlalchemy import create_engine
import pandas as pd


class DbConnector:
    def __init__(self, uri):
        self.uri = uri

    def retrieve_abstracts(self):
        pass


class SqlConnector(DbConnector):
    def __init__(self, uri):
        super().__init__(uri)
        self.driver = create_engine(self.uri)

    def retrieve_information_as_df(self, table, columns=None, limit=20, offset=20):
        if columns:
            col_string = ",".join(columns)
        else:
            col_string = "*"
        sql_query = f"SELECT {col_string} FROM {table} LIMIT {limit} OFFSET {offset}"
        return pd.read_sql_query(sql_query, con=self.driver)


class SqlLiteConnector(SqlConnector):
    def __init__(self, path_to_db):
        self.uri = "sqlite:///" + path_to_db
