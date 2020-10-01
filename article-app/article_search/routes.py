from article_search import app


@app.route('/')
def hello_world():
    return 'Hello World!'
