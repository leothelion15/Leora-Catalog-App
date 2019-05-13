from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databaseSetupCatalog import Category, Base, CatalogItem, UserLogOn

engine = create_engine('sqlite:///catalogApp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Add original user to the database
user1 = UserLogOn(name = 'Leora Skaist', email = 'leoraskaist@gmail.com', picture = "https://lh5.googleusercontent.com/-1Xb7dUiT0y0/AAAAAAAAAAI/AAAAAAAAAAA/ACHi3rdEUHl9O-4oq9BlNSTMCdt-wlLLkg/mo/photo.jpg")

session.add(user1)
session.commit()

# Add Soccer items to catalog
category1 = Category(name = "Soccer", user_id = 1)

session.add(category1)
session.commit()

catalogItem1 = CatalogItem(title = "Soccer Ball", description = "Black and white ball.", category = category1, user_id = 1)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(title = "Soccer Net", description = "Full size net.", category = category1, user_id = 1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Soccer Cleats", description = "Black and white sneakers with spikes on the bottom.", category = category1, user_id = 1)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(title = "Shin Gaurds", description = "Protective gear for shins. Comes in children and adults sizing.", category = category1, user_id = 1)

session.add(catalogItem4)
session.commit()

# Add Basketball items to catalog
category2 = Category(name = "Basketball", user_id = 1)

session.add(category2)
session.commit()

catalogItem1 = CatalogItem(title = "Basketball", description = "Orange and black ball.", category = category2, user_id = 1)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(title = "Basketball Hoop", description = "Hoop can be adjusted in height.", category = category2, user_id = 1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Basketball Shorts", description = "Loose shorts. Available for men and women", category = category2, user_id = 1)

session.add(catalogItem3)
session.commit()

# Add baseball items to catalog
category3 = Category(name = "Baseball", user_id = 1)

session.add(category3)
session.commit()

catalogItem1 = CatalogItem(title = "Baseball", description = "Small white and red ball.", category = category3, user_id = 1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Baseball Bat", description = "Made from wood.", category = category3, user_id = 1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Baseball Glove", description = "Made from leather. Available in brown or black.", category = category3, user_id = 1)

session.add(catalogItem3)
session.commit()

# Add hockey items to catalog
category4 = Category(name = "Ice Hockey", user_id = 1)

session.add(category4)
session.commit()

catalogItem1 = CatalogItem(title = "Hockey Stick", description = "Made from wood.", category = category4, user_id = 1)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(title = "Hockey Puck", description = "Small black puck for ice hockey.", category = category4, user_id = 1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Hockey Skates", description = "Ice skates with thick blade.", category = category4, user_id = 1)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(title = "Hockey Helmet", description = "Protective gear for the head. Comes in children and adults sizing.", category = category4, user_id = 1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(title = "Hockey Gloves", description = "Protective gear for the hands. Extra thick to keep fingers warm.", category = category4, user_id = 1)

session.add(catalogItem5)
session.commit()

# Add football items to catalog
category5 = Category(name = "Football", user_id = 1)

session.add(category5)
session.commit()

catalogItem1 = CatalogItem(title = "Football", description = "Brown leather ball in the shape of a foot.", category = category5, user_id = 1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Football Cleats", description = "Black and white sneakers with spikes on the bottom.", category = category5, user_id = 1)

session.add(catalogItem2)
session.commit()

catalogItem4 = CatalogItem(title = "Football Helmet", description = "Protective gear for the head. Comes in children and adults sizing.", category = category4, user_id = 1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(title = "Football Gloves", description = "Protective gear for the hands.", category = category5, user_id = 1)

session.add(catalogItem5)
session.commit()

print "added catalog items!"
