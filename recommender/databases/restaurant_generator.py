for i in range(-2, 2):
    for j in range(-2, 2):
        places = Caller.get_places("AIzaSyDS40mCvePWcb9_eI_SErFQpt98UoTI3UI",
                                   str(50.084062 + i / 100) + ', ' + str(14.421809 + j / 100),
                                   "500")
        for k in range(0, 59):
            ident = places[k]['id']
            x = places[k]['geometry']['location']['lat']
            y = places[k]['geometry']['location']['lat']
            name = places[k]['name']
            restaurant_list.append(Rest.Restaurant(ident, name, x, y))

restaurant_dictionary = dict()
for restaurant in restaurant_list:
    if not restaurant_dictionary.__contains__(restaurant.id):
        restaurant_dictionary[restaurant.id] = restaurant

for key in restaurant_dictionary.keys():
    print(restaurant_dictionary[key].name)

print(len(restaurant_dictionary))
dict().__contains('rating')


#c.execute("""
 #   CREATE TABLE restaurants (
  #      id string,
   #     name string,
    #    lat string,
     #   lng string
      #  )""")
for key in restaurant_dictionary.keys():
    A = restaurant_dictionary[key]
    c.execute("""
        INSERT INTO restaurants VALUES (:id, :name, :lat, :lng)
            """, {'id': A.id, 'name': A.name, 'lat': A.lat, 'lng': A.lon})