import json
import numpy as np
import pickle
from collections import Counter
from travel_backend.database.database import db_session, engine
from travel_backend.models.restaurant import Restaurant


locations = {}
LLM_FILE = '../data/LLM.txt'

# with open('../data/test_json.txt', encoding='utf-8') as json_file:
#     data = json.load(json_file)
#     for l in data['results']:
#         locations[l['id']] = str(l['types'])

restaurants = Restaurant.query.all()

for r in restaurants:
    locations[r.id] = r.types


len_locations = len(locations)
location_sims = np.zeros(shape=(len_locations, len_locations), dtype=np.float32)


def cosine_sim(vec1, vec2):
    # count word occurrences
    vec1_counter = Counter(vec1)
    vec2_counter = Counter(vec2)

    # convert to word-vectors
    words = list(vec1_counter.keys() | vec2_counter.keys())
    vec1_occ = [vec1_counter.get(word, 0) for word in words]
    vec2_occ = [vec2_counter.get(word, 0) for word in words]

    # find cosine
    len_1 = sum(a * a for a in vec1_occ) ** 0.5
    len_2 = sum(b * b for b in vec2_occ) ** 0.5
    dot = sum(a * b for a, b in zip(vec1_occ, vec2_occ))
    cosine = dot / (len_1 * len_2)

    return cosine


if __name__ == '__main__':
    for i in range(0, len_locations):
        for j in range(i, len_locations):
            location_sims[i, j] = cosine_sim(list(locations.values())[i], list(locations.values())[j])

    np.savetxt(LLM_FILE, location_sims, fmt='%0.6f', delimiter='\t', newline='\n')
    pickle_out = open("../data/LLM.pickle", "wb")
    pickle.dump(location_sims, pickle_out)
    pickle_out.close()
