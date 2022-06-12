from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    title = "Список треков"
    return render_template('track_list.html', page_title=title)


if __name__ == "__main__":
    app.run(debug=True)
