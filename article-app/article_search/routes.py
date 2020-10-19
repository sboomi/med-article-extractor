from article_search import app
from flask import render_template, url_for
from article_search.forms import SearchForm
from article_search.utils import query_preprocessing, abstract_similarity, find_best_topics
from article_search.models import Article


@app.route('/', methods=["GET", "POST"])
@app.route('/main')
def main():
    """
    The main page of the app. A simple page showing popular topics through LDA modelling and showing a form returning
    similar articles.

    :return: Either the result page (POST) or the main page (GET)
    """
    form = SearchForm()
    topics = find_best_topics(n_max=5)
    if form.validate_on_submit():
        query = form.content.data
        query_vector = query_preprocessing(query)
        id_list = abstract_similarity(query_vector.split())
        articles = [Article.query.filter_by(id=int(new_id)).first() for new_id in id_list]
        return render_template("results.html", articles=articles[:30])
    return render_template("main.html", form=form, topics=list(topics))


