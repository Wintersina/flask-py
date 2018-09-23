from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
import os
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

sql_lite_db = create_engine('sqlite:///restaurantmenu.db')  # say what database
Base.metadata.bind = sql_lite_db
DBsession = sessionmaker(bind = sql_lite_db)
session = DBsession()


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id,menu_id):
    menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItem=[menuItem.serialize])

@app.route('/restaurants/<int:restaurant_id>/JSON/')
def restaurantMenuJSON(restaurant_id):
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return jsonify(MenuItems=[i.serialize for i in menuItems])

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    restaurantResult = session.query(Restaurant).filter_by(id = restaurant_id)
    menuItems = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    restaurantFinalResult = restaurantResult.one()
    output = render_template('menu.html', restaurant=restaurantFinalResult, menuItems = menuItems)

    return output

#Create a new menu item
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(item_name = request.form['name'],restaurant_id = restaurant_id)
        session.add(newItem)
        session.commit()
        flash("Menu item created!")
        output = redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
        return output
    else:
        output = render_template('newMenuItem.html', restaurant_id= restaurant_id)
        return output

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods= ['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        editItem.item_name = request.form['name']
        session.add(editItem)
        session.commit()
        flash("Menu item edited!!")
        output = redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
        return output
    else:
        output = render_template('menuitemedit.html',restaurant_id= restaurant_id, menu_id=menu_id,i_name=editItem.item_name)
        return output
# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/' , methods= ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
        session.delete(editItem)
        session.commit()
        flash("Menu item DELETEEEEED!")
        output = redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
        return output
    else:
        output = render_template('delete.html',restaurant_id= restaurant_id, menu_id=menu_id,i_name=editItem.item_name)
        return output

if __name__ == '__main__':
    app.secret_key = "yum_yum_key"
    app.debug = True
    port = int(os.environ.get('PORT',5000))
    app.run(host = '0.0.0.0', port = port)