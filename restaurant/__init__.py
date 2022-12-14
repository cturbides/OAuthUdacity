from flask import Flask
import os

app = Flask(__name__)
app.secret_key = '9bb7bb35d2ccf6fc149f5c6cddc115181bc7154980ef9ac707a9c2671448f7cc145960cd6b2685d58f9e5d9006a3da1e40cec627278f5a94f477aae0'

app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' #Made for testing enviroments

import restaurant.routes