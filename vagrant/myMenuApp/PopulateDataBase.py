import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

#Know which database engine we want to communicate with
engine = create_engine('sqlite:///restaurantmenu.db')

# bind lets you define the cnxn btw class definitions and correspong tables in
# our database
Base.metadata.bind = engine

# Create comm link betwen our code executions and the engines we just created
DBSession = sessionmaker(bind = engine)

# session lets you write down all the commands want to execute,
# but not send to the db until we call a commit
session = DBSession()

# Create a new item for the db
myFirstRestaurant = Restaurant(name = "Pizza Palace")

# To add to the db, first stage and then commit
session.add(myFirstRestaurant)
session.commit()

# To find out what's in the db:
print(session.query(Restaurant).all())

# When adding to the db, make sure to fill out all the columns
cheesepizza = MenuItem(name = "Cheese Pizza", description = "Made with all natural ingrediants and fresh mozzarella",
                       course = "Entree", price ="$8.99", restaurant = myFirstRestaurant)

session.add(cheesepizza)
session.commit()

print(session.query(MenuItem).all())

# Create a variable to refere to a single row in the db
firstResult = session.query(Restaurant).first()

print(firstResult.name)
