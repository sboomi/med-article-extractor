from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField


class WhichDataBaseForm(FlaskForm):
    db_choice = RadioField('From which database?',
                           choices=[('sqlite3', 'SQLite3'), ('mongo', 'MongoDB')],
                           default='1')
    submit = SubmitField('Search')
