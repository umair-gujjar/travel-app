from flask import Flask, jsonify, abort, request, render_template
from providers.places import get_places
from database.database import db_session, init_db
from models.restaurant import Restaurant
from recommender.CB_recommender import recommend_locations_CB, load_matrix
import json
import numpy as np

init_db()

app = Flask(__name__)
app.config.from_object("config.config.Config")



@app.route('/')
def hello():

    res = Restaurant.query.all()
    print(res)

    return render_template("home.html")


@app.route('/places')
def places():
    return render_template("places.html")


# REST API
@app.route('/rest/add-location', methods=['POST'])
def add_location():
    content = request.get_json()
    r = Restaurant(content['id'], content['title'], content['coords']['latitude'], content['coords']['longitude'], content['google_ratings'], content['types'])
    db_session.add(r)
    db_session.commit()
    return 'success'


@app.route('/rest/find-recommended', methods=['GET'])
def find_recommended():
    LLM = load_matrix('recommender/data/LLM')

    locations = []
    with open('recommender/data/test_json.txt', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for l in data['results']:
            locations += [l['name']]
    ULM = np.ones(shape=(15, 8), dtype=np.float32)
    # ULM = [[1, 1, 1, 1, 1, 1, 0, 0][1, 1, 1, 1, 1, 1, 1, 1][0, 0, 0, 0, 0, 0, 0, 0][1, 0, 0, 0, 1, 0, 0, 0][0, 0, 0, 0, 1, 1, 1, 1][0, 0, 0, 0, 0, 1, 1, 0][1, 0, 0, 0, 0, 0, 0, 0][1, 1, 1, 1, 1, 1, 1, 1]]
    u = 1

    k = 3
    r = 2
    recommendations = recommend_locations_CB(LLM, ULM, u, locations, k, r, OUTPUT=True)
    names = []
    names += [locations[r] for r in recommendations]
    recommendation_record = {}
    recommendation_records = []
    latlang = {}
    with open('recommender/data/test_json.txt', encoding='utf-8') as json_file:
        data = json.load(json_file)
        for l in data['results']:
            for j in names:
                if j == l['name']:
                    latlang['latitude'] = l['geometry']['location']['lat']
                    latlang['longitude'] = l['geometry']['location']['lng']
                    recommendation_record['coords'] = latlang
                    recommendation_record['title'] = l['name']
                    recommendation_record['id'] = l['id']
                    recommendation_record['types'] = l['types']
                    recommendation_records.append(recommendation_record)

    return jsonify(recommendation_records)

    # location = request.args.get("location")
    # radius = request.args.get("radius")
    #
    # if location is None or radius is None:
    #     abort(400)
    # places = get_places(app.config['API_KEY'], location, radius)
    # return jsonify(places)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()

