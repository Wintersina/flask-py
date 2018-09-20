import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#START OF FILE #
Base = declarative_base()

class Resturant(Base):
   __tablename__ = 'resturants'
   id = Column(Integer, primary_key = True)
   name = Column(String(80), nullable = False)


class MenuItem(Base):
   __tablename__ = 'menu_items'
   id = Column(Integer, primary_key = True)
   item_name = Column(String(80), nullable = False)
   item_type = Column(String( 250))
   price = Column(String(8))
   description = Column(String(250))
   resturant = relationship(Resturant)
   resturant_id = Column(Integer, ForeignKey('resturants.id'))

###END OF FILE ####
engine = create_engine('sqlite:///resturantmenu.db')

Base.metadata.create_all(engine)
