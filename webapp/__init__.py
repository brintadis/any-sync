import os
from flask import Flask, render_template
from webapp.forms import PlaylistLinkForm


def create_app():
    app = Flask(__name__)

    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    @app.route("/", methods=['GET', 'POST'])
    def index():
        title = "AnySync"
        url_form = PlaylistLinkForm()
        return render_template('index.html', page_title=title, form=url_form)

    return app
