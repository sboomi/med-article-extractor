import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sqlalchemy.engine import Engine
import random
from sqlalchemy import create_engine
from st_model_conceptor.utils import load_sample, load_nlp_params, tokenize_text, filter_stopwords, clean_text, \
    create_word_freq, find_row_number

st.title("Text similarity model")
uri = "sqlite:///" + 'D:\\shadi\\PythonProjects\\pdf-information-extraction\\articlesdb.db'


@st.cache(suppress_st_warning=True)
def get_df(uri):
    df = load_sample(uri)
    return df


@st.cache(suppress_st_warning=True)
def get_nlp_params():
    return load_nlp_params()


@st.cache(suppress_st_warning=True, hash_funcs={Engine: id})
def initiate_lda(engine, n_topics):
    conn = engine.connect()
    df = pd.read_sql("SELECT * FROM clean_articles", con=conn)
    conn.close()
    cv = CountVectorizer()
    X = cv.fit_transform(df['clean_abstract'].values)
    y = df['id'].values
    lda = LatentDirichletAllocation(n_components=n_topics).fit(X)
    features = cv.get_feature_names()

    return X, y, lda, features


@st.cache(suppress_st_warning=True, hash_funcs={Engine: id})
def initiate_tfidf(engine):
    conn = engine.connect()
    df = pd.read_sql("SELECT * FROM clean_articles", con=conn)
    conn.close()
    tfidf_v = TfidfVectorizer()
    X = tfidf_v.fit_transform(df['clean_abstract'].values)
    y = df['id'].values
    return X, y, tfidf_v


def display_topics(model, feature_names, no_top_words):
    results = {
        "topic_number": [],
        "topic_result": []
    }
    for topic_idx, topic in enumerate(model.components_):
        results["topic_number"].append(topic_idx)
        results["topic_result"].append(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))
        return pd.DataFrame(results)


st.write("Example sample out of 200 samples:")
df = get_df(uri)
nlp_params = get_nlp_params()
conn = create_engine(uri, echo=False, connect_args={'timeout': 15})

random_i = random.randint(0, df.shape[0] - 1)
example_abstract = df['abstract'][random_i]

st.text(example_abstract)

# Preprocessing part
st.header("Preprocessing")

st.subheader("Tokenization")
tokenized_example = tokenize_text(example_abstract, tokenizer=nlp_params["tokenizer"])
st.text(" ".join(tokenized_example))

st.subheader("Use stopwords")

locale = st.selectbox(
    'Can you identify the language of the text?',
    ('en', 'fr', 'de'))

st.write('Language:', locale)

try:
    stopword_list = nlp_params["stop_words"][locale]
except KeyError:
    stopword_list = []
    st.error("This stopword list isn't available yet")

stopped_example = filter_stopwords(tokenized_example, stopword_list=stopword_list)
st.text(" ".join(stopped_example))

st.subheader("Analyze results over sample")

clean_df = df.copy()

clean_df['clean_abstract'] = [clean_text(text, tokenizer=nlp_params["tokenizer"], stopword_list=stopword_list)
                              for text in df['abstract'].values]
clean_df = clean_df.drop("abstract", axis=1)

word_counter = create_word_freq(clean_df['clean_abstract'].values)

max_display = st.slider('How many values?', 0, 50, 15)

st.bar_chart(word_counter.sort_values(ascending=False)[:max_display])

st.write("Are you satisfied with the results?")
if st.button('Yes'):
    st.write("Writing a new table...")

    curr_conn = conn.connect()
    total_entries = find_row_number("articles", conn=curr_conn)
    curr_conn.close()
    step = 1

    progress_bar = st.progress(0)
    for offset in range(0, total_entries, step):
        curr_conn = conn.connect()
        sql_query = f"SELECT id, abstract FROM articles LIMIT {step} OFFSET {offset}"
        sql_create_table = "CREATE TABLE IF NOT EXISTS clean_articles  (id PRIMARY KEY, clean_abstract TEXT);"
        curr_conn.execute(sql_create_table)
        rows = curr_conn.execute(sql_query)
        for row in rows:
            id, abstract = row
            clean_abstract = clean_text(abstract, tokenizer=nlp_params["tokenizer"], stopword_list=stopword_list)
            sql_insert_query = f'INSERT INTO clean_articles (id, clean_abstract) VALUES ({id}, "{clean_abstract}");'
            try:
                curr_conn.execute(sql_insert_query)
            except:
                sql_update_query = f'UPDATE clean_articles SET clean_abstract = "{clean_abstract}" WHERE id = {id}'
                curr_conn.execute(sql_update_query)
        curr_conn.close()
        progress_bar.progress(min(total_entries, (offset + step) / total_entries))
    st.write("Done!")


st.header("Bag of words")

st.subheader("TF-IDF")
X, y, tfidf_model = initiate_tfidf(curr_conn)

if st.button('Save TF-IDF'):
    with open("models/tfidf", "wb") as file:
        pickle.dump({"model": tfidf_model,
                     "X": X,
                     "y": y}, file)

st.write("Sparse matrix of dimension", X.shape)
st.dataframe(X.toarray()[:200, :10])

st.subheader("Latent Dirichlet Allocation")

n_topics = st.slider('Number of topics?', 2, 50, 20)

X_c, y_c, lda, feature_names = initiate_lda(curr_conn, n_topics)

no_top_words = st.slider('Show how many words?', 2, 20, 10)

st.dataframe(display_topics(lda, feature_names, no_top_words))

if st.button('Save LDA'):
    with open("models/lda", "wb") as file:
        pickle.dump({"model": lda,
                     "X": X,
                     "y": y}, file)

