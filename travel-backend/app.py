from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/places')
def places():
    return render_template("places.html")


if __name__ == '__main__':
    app.run()

