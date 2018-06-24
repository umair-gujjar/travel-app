from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from models.restaurant import Restaurant
from providers.places import get_places

engine = create_engine('sqlite:///providers/restaurant.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
c = db_session()

restaurant_list = []
rating = ''
for i in range(-2, 2):
    for j in range(-2, 2):
        places = get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI",
                                   str(50.084062 + i / 100) + ', ' + str(14.421809 + j / 100),
                                   "10")

        print("Current location: " + str(50.084062 + i / 100) + ', ' + str(14.421809 + j / 100))
        for k in range(0, len(places)):
            ident = places[k]['id']
            result_proxy = c.execute("SELECT * FROM restaurants WHERE id = :id", {'id': ident})
            result = result_proxy.fetchall()
            if len(result) != 0:
                print("Row with id: " + ident + " already exists")
                continue
            x = places[k]['geometry']['location']['lat']
            y = places[k]['geometry']['location']['lat']
            name = places[k]['name']
            if places[k].__contains__('rating'):
                rating = places[k]['rating']
            types = ','.join(places[k]['types'])
            restaurant_list.append(Restaurant(ident, name, x, y, rating, types))

restaurant_dictionary = dict()
for restaurant in restaurant_list:
    if not restaurant_dictionary.__contains__(restaurant.id):
        restaurant_dictionary[restaurant.id] = restaurant

for key in restaurant_dictionary.keys():
    print(restaurant_dictionary[key].name)

print(len(restaurant_dictionary))

for key in restaurant_dictionary.keys():
    A = restaurant_dictionary[key]
    c.execute("""
        INSERT INTO restaurants VALUES (:id, :lat, :lng, :name, :google_ratings, :types)
            """, {'id': A.id, 'lat': A.lat, 'lng': A.lng, 'name': A.name, 'google_ratings': A.google_ratings, 'types': A.types})
c.commit()
