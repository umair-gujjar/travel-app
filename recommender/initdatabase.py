from recommender.model_classes import  User as U
from random import randint
import sqlite3

# In the file User.db is the user database with 50 randomly generated users with random relationship distances from us

userList = []
for i in range(0, 50):
    userList.append(U.User(i+1, 0, randint(0, 5)))


conn = sqlite3.connect('User.db')

c = conn.cursor()


#c.execute("DELETE FROM users")
#for i in range(0, 50):
#    x = U.User(i+1, 'Name' + str(i + 1), randint(1, 5))
#    c.execute("INSERT INTO users VALUES (:id, :name, :distance)", {'id': x.id, 'name': x.name, 'distance': x.relationshipdistance})

c.execute("SELECT * FROM users")
print(c.fetchall())

conn.commit()

conn.close()
