
import os
from flask import Flask, redirect
from .api.v2.views.products import products
from .api.v2.views.users import users

app = Flask(__name__)

app.register_blueprint(products, url_prefix='/api/v2')
app.register_blueprint(users, url_prefix='/api/v2')


@app.route('/')
def root():
    return redirect("https://storemanager.docs.apiary.io/", code=302)


@app.route('/ping', methods=['GET'])
def pong():
    return 'pong', 200


app_settings = os.getenv(
    'APP_SETTINGS',
    'instance.config.DevConfig'
)
app.config.from_object(app_settings)