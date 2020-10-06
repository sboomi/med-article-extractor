from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import SubmitField


class UploadForm(FlaskForm):
    pdf = FileField("Enter PDF here",
                    validators=[FileRequired, FileAllowed(['pdf'], 'Only pdfs allowed!')])
    submit = SubmitField("Upload PDF")
