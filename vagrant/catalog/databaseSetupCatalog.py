import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    #Table
    __tablename__ = 'category'

    #Mapper
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

    # Allow for JSON intepretation of the data
    @property
    def serialize(self):
        return{
            'name'      : self.name,
            'id'        : self.id
        }

class CatalogItem(Base):
    #Table:
    __tablename__ = 'catalog_item'

    # Mapper
    title = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)

    @property
    def serialize(self):
        #Returns object data in easily serializeable format
        return {
            'title'      : self.title,
            'description'       : self.description,
            'id'        : self.id,
        }

#######insert at end of file #######

engine = create_engine('sqlite:///catalogApp.db')

Base.metadata.create_all(engine)
