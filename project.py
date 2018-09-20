from flask import Flask
import os
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Resturant, MenuItem

sql_lite_db = create_engine('sqlite:///resturantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()


@app.route('/')
@app.route('/restaurants/<int:resturant_id>/')
def HelloWorld(resturant_id):
    results = session.query(Resturant).all()

    output = ""
    menuItem = session.query(MenuItem).filter_by(resturant_id = resturant_id)
    output+= "<br><h2>Menu Items For %s : </h2> <br>" % menuItem.first().resturant.name

    for i in menuItem:
        output += "%s %s <br>"% (i.item_name,i.price)
        output += "%s <br>"%i.description

    return output

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get('PORT',5000))
    app.run(host = '0.0.0.0', port = port)