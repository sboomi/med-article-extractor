from article_search import db


class Article(db.Model):
    __tablename__ = "articles"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    publication_date = db.Column(db.DateTime)
    abstract = db.Column(db.Text)
    keywords = db.Column(db.String(250))
    doi = db.Column(db.String(100))
    authors = db.Column(db.String(250))

    def __repr__(self):
        return f"Article('{self.title}','{self.authors}', '{self.publication_date}')"