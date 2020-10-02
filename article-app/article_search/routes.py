from article_search import app
from flask import render_template, url_for, redirect, request
from article_search.forms import SearchForm


@app.route('/', methods=["GET", "POST"])
@app.route('/main')
def main():
    form = SearchForm()
    if form.validate_on_submit():
        query = form.content.data
        return render_template("results.html", query=query)
    return render_template("main.html", form=form)


