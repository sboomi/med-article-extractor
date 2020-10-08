from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class UploadForm(FlaskForm):
    pdf = FileField("Enter PDF here",
                    validators=[FileRequired(), FileAllowed(['pdf'], 'Only pdfs allowed!')])
    submit = SubmitField("Upload PDF")


class FindDataForm(FlaskForm):
    keywords = StringField('Enter keywords', validators=[DataRequired()])
    n_ids = IntegerField('N° of pdfs?', validators=[DataRequired()])
    submit = SubmitField("Submit")
