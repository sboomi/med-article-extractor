from server_module import app
from server_module.forms import UploadForm
from flask import render_template, current_app
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=['GET', 'POST'])
def upload_zone():
    form = UploadForm()
    if form.validate_on_submit():
        pdf_file = form.pdf.data
        file_path = os.path.join(current_app.root_path, 'static/pdfs', secure_filename(pdf_file))
        pdf_file.save(file_path)
        return "Success!"

    return render_template("upload-pdf.html", form=form)
