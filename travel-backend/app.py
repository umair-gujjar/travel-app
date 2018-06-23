from flask import Flask, jsonify
from flask import abort
from flask import render_template
from flask import request
from providers.places import GooglePlacesDataProvider

app = Flask(__name__)
app.config.from_object("config.config.Config")


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/places')
def places():
    return render_template("places.html")


# REST API
@app.route('/rest/find-recommended', methods=['GET'])
def find_recommended():
    location = request.args.get("location")
    radius = request.args.get("radius")

    if location is None or radius is None:
        abort(400)
    google_api = GooglePlacesDataProvider()
    places = google_api.get_places(app.config['API_KEY'], location, radius)
    return jsonify(places)


if __name__ == '__main__':
    app.run()

