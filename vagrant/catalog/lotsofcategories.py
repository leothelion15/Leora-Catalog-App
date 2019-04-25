from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databaseSetupCatalog import Category, Base, CatalogItem

engine = create_engine('sqlite:///catalogApp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



#Items in Soccer
category1 = Category(name = "Soccer")

session.add(category1)
session.commit()

catalogItem2 = CatalogItem(title = "Soccer Ball", description = "Black and white ball. Perfect for kicking.", category = category1)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(title = "Soccer Net", description = "Full size net.", category = category1)

session.add(catalogItem1)
session.commit()

#Catelog for Basketball
category2 = Category(name = "Basketball")

session.add(category2)
session.commit()

catalogItem2 = CatalogItem(title = "Basketball", description = "Orange and black ball. Perfect for dribling.", category = category2)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(title = "Basketball Hoop", description = "Hoop can be adjusted in height.", category = category2)

session.add(catalogItem1)
session.commit()

#Catelog for Basebll
category3 = Category(name = "Baseball")

session.add(category3)
session.commit()

catalogItem2 = CatalogItem(title = "Baseball", description = "Small white and red ball. Perfect for catch.", category = category3)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(title = "Baseball Bat", description = "Wooden bat.", category = category3)

session.add(catalogItem1)
session.commit()

print "added catalog items!"
