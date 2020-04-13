from flask import Flask

app = Flask(__name__)
#app = Flask(__name__, static_url_path='/chur')

from app import routes