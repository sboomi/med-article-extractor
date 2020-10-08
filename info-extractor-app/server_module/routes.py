from server_module import app
from server_module.forms import UploadForm, FindDataForm
from server_module.utils import get_pdf_content, extract_pdf_information, return_information_as_batch
from flask import render_template, jsonify, redirect, flash, url_for
from werkzeug.utils import secure_filename
import os
from pymed.pymed import PubMed, retrieve_informations


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

        soup, metadata = get_pdf_content(file_path)
        description = extract_pdf_information(soup, metadata)
        return jsonify(description), 200

    return render_template("upload_pdf.html", form=form)


@app.route("/getarticles", methods=['GET', 'POST'])
def get_articles():
    form = FindDataForm()
    if form.validate_on_submit():
        query = form.keywords.data
        max_results = form.n_ids.data
        pm = PubMed()
        list_id_url = pm.search(query.split(), max_req=max_results)
        content = retrieve_informations(list_id_url)
        list_ids = content['esearchresult']['idlist']
        success_message = return_information_as_batch(list_ids, source_db=pm)
        flash(success_message, 'info')
        return redirect(url_for('upload_zone'))
    return render_template("getarticles.html", form=form)
