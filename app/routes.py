from app import app
from flask import abort, redirect, url_for
from .lib import tst


@app.route('/')
def index():
    return redirect(url_for('chu'))

@app.route('/chu')
def chu():
    #abort(401)
    res = tst.pr()
    print(res)
    return "Redirected!"