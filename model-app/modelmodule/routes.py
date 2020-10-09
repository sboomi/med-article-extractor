from modelmodule import app
from modelmodule.forms import WhichDataBaseForm
from modelmodule.utils import load_options
from flask import render_template


@app.route('/', methods=['GET', 'POST'])
@app.route('/main')
def init_model():
    options = load_options()

    # Example abstract
    dbform = WhichDataBaseForm()
    if dbform.validate_on_submit():
        options['database'] = dbform.db_choice.data

    return render_template("main.html", dbform=dbform, options=options)
