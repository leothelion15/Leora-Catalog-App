#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from databaseSetupCatalog import Base, Category, CatalogItem

engine = create_engine('sqlite:///catalogApp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Show all current categories and latest Items
@app.route('/')
@app.route('/catalog/')
def catalogHome():
    catalog = session.query(Category).all()
    items = session.query(CatalogItem).order_by(CatalogItem.id.desc()).limit(5)
    return render_template('catalogHome.html', catalog = catalog, items = items)

#The page will show  all the items in a category.
@app.route('/catalog/<category_name>/items/')
def categoryItems(category_name):
    catalog = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CatalogItem).filter_by(category_id = catalog.id)
    return render_template('categoryItems.html', catalog = catalog, items = items)

#This page will display information about the item.
@app.route('/catalog/<category_name>/items/<item_name>/')
def itemInfo(category_name, item_name):
    #catalog = session.query(Category).filter_by(name = category_name).one()
    item = session.query(CatalogItem).filter_by(title = item_name).one()
    return render_template('itemInfo.html', item = item)

#This page will allow signed in user to add a new item
@app.route('/catalog/new', methods = ['GET', 'POST'])
def newItem():
    if request.method == 'POST':
        newItem = CatalogItem(title = request.form['title'], description = request.form['description'],
        category_id = request.form['category'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('catalogHome'))
    else:
        return render_template('newItem.html')

#This page lets you edit an item when logged in.
@app.route('/catalog/<category_name>/items/<item_name>/edit')
def editItem(category_name, item_name, method = ['GET', 'POST']):
    editedItem = session.query(CatalogItem).filter_by(title = item_name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('categoryItems', category_name = category_name))
    else:
        return render_template('editItem.html', category_name = category_name, item = editedItem)


@app.route('/catalog/<category_name>/items/<item_name>/delete')
def deleteItem(category_name, item_name):
    return "This page lets you delete an item when logged in."

@app.route('/catalog/JSON')
def catalogHomeJSON():
    catalog = session.query(Category).all()
    items = session.query(CatalogItem).all()
    return jsonify(CatalogList = [c.serialize for c in catalog],
        CatalogItems = [i.serialize for i in items])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
