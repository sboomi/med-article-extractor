from server_module import app
from server_module.forms import UploadForm
from server_module.utils import get_pdf_content, extract_pdf_information
from flask import render_template, jsonify
from werkzeug.utils import secure_filename
import os


@app.route("/", methods=['GET', 'POST'])
@app.route("/upload")
def upload_zone():
    form = UploadForm()
    if form.validate_on_submit():
        pdf_file = form.pdf.data

        # app.instance_path or current_app.root_path don't work for this one
        file_path = os.path.join(app.root_path, 'static', 'pdfs', secure_filename(pdf_file.filename))
        if not os.path.exists(file_path):
            pdf_file.save(file_path)

        soup, metatdata = get_pdf_content(file_path)
        description = extract_pdf_information(soup, metatdata)
        return jsonify(description), 200

    return render_template("upload_pdf.html", form=form)
