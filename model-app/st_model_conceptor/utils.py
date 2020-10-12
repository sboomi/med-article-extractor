import pandas as pd
from sqlalchemy import create_engine
import json
import re
from collections import Counter


def load_sample(uri, n_samples=200, offset=0, save_df=None):
    """
    The fucntion loads a sample from a relational database and converts it to a dataframe
    **NOTE :** Only works with SQLite

    :param offset: The starting point of the sampling (0 by default)
    :param n_samples: Number of samples to get into the database (200)
    :param uri: URI of the SQL database
    :return: A df containing a number of samples
    """
    engine = create_engine(uri)
    sql_query = f"SELECT id, abstract FROM articles LIMIT {n_samples} OFFSET {offset}"

    conn = engine.connect()
    df = pd.read_sql_query(sql_query, con=conn)
    if save_df:
        save_df.to_df("clean_articles", con=conn, index="id", if_exists="append", index_label='id')
    conn.close()

    return df


def create_table_sql(table, id, columns):
    sql_req = f"CREATE TABLE {table} IF NOT EXISTS"
    id_req = f"{id} INTEGER PRIMARY KEY"
    col_req = ", ".join([f"{column} TEXT" for column in columns])
    sql_req += f" ({id_req}, {col_req});"
    return sql_req


def find_row_number(table, conn):
    sql_req = f"SELECT COUNT(*) FROM {table}"
    rows = conn.execute(sql_req)
    for row in rows:
        total_row = row[0]
    return int(total_row)


def load_nlp_params():
    ressource_path = 'st_model_conceptor/ressources/nlpparams.json'
    with open(ressource_path, 'r') as file:
        nlp_params = json.load(file)
    return nlp_params


def tokenize_text(text, tokenizer):
    matches = re.finditer(tokenizer, text, re.M)
    list_words = [match.group(0).replace(")", "").lower() for match in matches]
    return list_words


def filter_stopwords(list_words, stopword_list):
    sw = set(stopword_list)
    return [word for word in list_words if word not in sw]


def clean_text(text, tokenizer, stopword_list):
    tokenized_list = tokenize_text(text, tokenizer)
    return " ".join(filter_stopwords(tokenized_list, stopword_list))


def cleanup_corpus(df):
    df['clean_abstract'] = df['abstract'].apply(clean_text)
    return df.loc[['id', 'clean_abstract']]


def create_word_freq(text_list):
    total_counter = Counter(text_list[0].split())
    for text in text_list[1:]:
        total_counter += Counter(text.split())
    return pd.Series(total_counter)
