import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#START OF FILE #
Base = declarative_base()

class Restaurant(Base):
   __tablename__ = 'restaurants'
   id = Column(Integer, primary_key = True)
   name = Column(String(80), nullable = False)


class MenuItem(Base):
   __tablename__ = 'menu_items'
   id = Column(Integer, primary_key = True)
   item_name = Column(String(80), nullable = False)
   item_type = Column(String( 250))
   price = Column(String(8))
   description = Column(String(250))
   restaurant = relationship(Restaurant)
   restaurant_id = Column(Integer, ForeignKey('restaurants.id'))

   @property
   def serialize(self):
      return {
         'id': self.id,
         'item_name': self.item_name,
         'description': self.description,
         'price': self.price,
         'course': self.item_type,
         'affiliated_restaurant': self.restaurant_id
      }


###END OF FILE ####
engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)

