from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    content = TextAreaField('Looking for an article?', validators=[DataRequired()])
    submit = SubmitField('Search')

