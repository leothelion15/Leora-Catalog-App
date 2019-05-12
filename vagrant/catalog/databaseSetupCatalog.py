import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

# Table of all users with account in my catalog
class UserLogOn(Base):
    __tablename__ = 'user_logon'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(500), nullable=False)
    picture = Column(String(500))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'email'      : self.email,
           'picture'    : self.picture
       }

# Table of all categories n my catalog
class Category(Base):
    #Table
    __tablename__ = 'category'

    #Mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    items = relationship("CatalogItem")
    user_id = Column(Integer, ForeignKey('user_logon.id'))
    userlogon = relationship(UserLogOn)

    # Allow for JSON intepretation of the data
    @property
    def serialize(self):
        return{
            'name'      : self.name,
            'id'        : self.id,
            'user_id'   :self.user_id,
            'items'     : [item.serialize for item in self.items]
        }

# Table of all items in the catalog
class CatalogItem(Base):
    #Table:
    __tablename__ = 'catalog_item'

    # Mapper
    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category, back_populates = 'items')
    user_id = Column(Integer, ForeignKey('user_logon.id'))
    userlogon = relationship(UserLogOn)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'title'      : self.title,
            'description'       : self.description,
            'id'        : self.id,
            'user_id'   :self.user_id
        }



#######insert at end of file #######

engine = create_engine('sqlite:///catalogApp.db')

Base.metadata.create_all(engine)
