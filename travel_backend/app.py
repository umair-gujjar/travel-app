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
    db_session.remove()
    return 'success'


@app.route('/rest/find-recommended', methods=['GET'])
def find_recommended():
    LLM = load_matrix('recommender/data/LLM')

    locations = []
    restaurants = Restaurant.query.all()
    locations += [r.name for r in restaurants if r]
    ULM = np.random.choice([0, 1], size=(20, len(locations)), p=[1. / 3, 2. / 3])
    u = 1
    k = 10
    r = 5

    recommendations = recommend_locations_CB(LLM, ULM, u, locations, k, r, OUTPUT=True)
    names = []
    names += [locations[r] for r in recommendations]
    recommendation_record = {}
    recommendation_records = []
    latlang = {}
    restaurants = Restaurant.query.all()
    names_ids = {}

    for r in restaurants:
        if r:
            names_ids[r.id] = r.name

    for r in restaurants:
        if r:
            for (j,i) in enumerate(names_ids.values()):
                latlang = {}
                recommendation_record = {}
                if i == r.name:
                    latlang['latitude'] = r.lat
                    latlang['longitude'] = r.lng
                    recommendation_record['coords'] = latlang
                    recommendation_record['title'] = r.name
                    recommendation_record['id'] = r.id
                    recommendation_record['types'] = r.types
                    recommendation_records.append(recommendation_record)

    print(recommendation_records)
    return 'recommended'
    # return jsonify(recommendation_records)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.run()

