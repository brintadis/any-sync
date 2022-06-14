from flask import Flask, render_template
from webapp.forms import PlaylistLinkForm
from webapp.model import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route("/", methods=['GET', 'POST'])
    def index():
        title = "AnySync"
        url_form = PlaylistLinkForm()
        if url_form.validate_on_submit():
            print(url_form.link.data)
        return render_template('index.html', page_title=title, form=url_form)

    return app
