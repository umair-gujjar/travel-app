from flask import Flask, jsonify, abort, request, render_template
from providers.places import get_places
from database.database import db_session
from models.restaurant import Restaurant

app = Flask(__name__)
app.config.from_object("config.config.Config")


@app.route('/')
def hello():
    return render_template("home.html")


@app.route('/places')
def places():
    return render_template("places.html")


# REST API
@app.route('/rest/add-location', methods=['POST'])
def add_location():
    content = request.get_json()
    r = Restaurant(content['title'], content['coords']['latitude'], content['coords']['longitude'])
    db_session.add(r)
    db_session.commit()


@app.route('/rest/find-recommended', methods=['GET'])
def find_recommended():
    location = request.args.get("location")
    radius = request.args.get("radius")

    if location is None or radius is None:
        abort(400)
    places = get_places(app.config['API_KEY'], location, radius)
    return jsonify(places)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()

