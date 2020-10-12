import pickle
import re
import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def load_model(filepath):
    with open(filepath, 'rb') as file:
        model = pickle.load(file)
    return model


def load_parameters():
    with open('article_search/ressources/nlpparams.json', 'r') as file:
        nlp_params = json.load(file)
    return nlp_params


def display_topics(model, feature_names, no_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic {}:".format(topic_idx))
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))


def query_preprocessing(query):
    nlp_params = load_parameters()
    tokenizer = re.compile(nlp_params["tokenizer"], re.M)
    matches = re.finditer(tokenizer, query)
    list_words = [match.group(0).replace(")", "").lower() for match in matches]
    sw = set(nlp_params["stop_words"]["en"])
    return " ".join([word for word in list_words if word not in sw])


def abstract_similarity(query_results):
    tfidf_params = load_model('article_search/mlmodels/tfidf')
    query_vec = tfidf_params["model"].transform(query_results)
    cos_d = cosine_similarity(query_vec, tfidf_params["X"])
    get_ids = [tfidf_params["y"][i] for i in np.argsort(cos_d[0])[::-1]]
    return get_ids


def find_best_topics(n_max=10):
    lda_params = load_model('article_search/mlmodels/lda')
    tf_idf = load_model('article_search/mlmodels/tfidf')
    feature_names = tf_idf["model"].get_feature_names()
    topic_set = set()
    for component in lda_params['model'].components_:
        for i in component.argsort()[:-n_max-1:-1].tolist():
            topic_set.add(feature_names[i])
    return topic_set
