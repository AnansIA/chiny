from flask import render_template
# from . import db
from flask import current_app as app


@app.route('/')
def index():
    return render_template('index.html')
