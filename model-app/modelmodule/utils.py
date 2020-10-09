from modelmodule.config import NlpParameters
import re
from dbconnectors.databases import SqlLiteConnector


def load_options():
    options = {"database": ""}
    return options


def load_connector(option):
    connectors = {
        'sqlite3': SqlLiteConnector()
    }
    return connectors[option]


def tokenize_text(text):
    tokenizer = re.compile(NlpParameters().tokenizer)
    matches = re.finditer(tokenizer, text, re.M)
    list_words = [match.replace(")", "").lower() for match in matches]
    return list_words


def filter_stopwords(list_words, language='en'):
    sw = set(NlpParameters(language).stop_words)
    return [word for word in list_words if word not in sw]


def clean_text(text):
    tokenized_list = tokenize_text(text)
    return filter_stopwords(tokenized_list)


def cleanup_corpus(df):
    df['clean_abstract'] = df['abstract'].apply(clean_text)
    return df.loc[['id', 'clean_abstract']]


def save_model():
    pass

