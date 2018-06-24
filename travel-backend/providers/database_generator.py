import sqlite3
import recommender.model_classes.User as U
import recommender.model_classes.Restaurant as Rest

conn = sqlite3.connect('restaurant.db')
c = conn.cursor()


print(c.fetchall())
conn.commit()
conn.close()
