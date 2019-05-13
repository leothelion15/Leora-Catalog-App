#!/usr/bin/python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask import session as login_session
import random, string, requests

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

app = Flask(__name__)

import os
import sys

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from databaseSetupCatalog import Base, Category, CatalogItem, UserLogOn

# Declare client ID
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog Application"

engine = create_engine('sqlite:///catalogApp.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

# Create a state token to prevent request forgery.
# Store it in the session for later validation.
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase +
                string.digits) for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

# Page to sign in through Google
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization placeholder
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    #data = answer.json()
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists. If not, make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    #Only disconnect a connected user
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        flash("No user connected")
        return redirect(url_for('catalogHome'))

    # Execute HTTP GET request to revoke current token.
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        #del login_session['credentials']
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        print response
        flash("You have successfully logged out")
        return redirect(url_for('catalogHome'))
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        print response
        flash("%s has not been logged out" % login_session['username'])
        return redirect(url_for('catalogHome'))

# Show all current categories and latest Items
@app.route('/')
@app.route('/catalog/')
def catalogHome():
    catalog = session.query(Category).order_by(asc(Category.name))
    items = session.query(CatalogItem).order_by(CatalogItem.id.desc()).limit(5)
    if 'username' not in login_session:
        return render_template('catalogHome.html', catalog = catalog, items = items)
    else:
        return render_template('catalogHomePrivate.html', catalog = catalog, items = items)

#The page will show  all the items in a category.
@app.route('/catalog/<category_name>/items/')
def categoryItems(category_name):
    catalog = session.query(Category).all()
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CatalogItem).filter_by(category_id = category.id).all()
    if 'username' not in login_session:
        return render_template('categoryItems.html', catalog = catalog, category = category, items = items)
    else:
        return render_template('categoryItemsPrivate.html', catalog = catalog, category = category, items = items)

#This page will display information about the item.
@app.route('/catalog/<category_name>/items/<item_name>/')
def itemInfo(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    categoryItems = session.query(CatalogItem).filter_by(category_id = category.id).all()
    item = session.query(CatalogItem).filter_by(title = item_name).one()
    if 'username' not in login_session:
        return render_template('itemInfo.html', item = item, category_name = category_name, categoryItems = categoryItems)
    else:
        return render_template('itemInfoPrivate.html', item = item, category_name = category_name, categoryItems = categoryItems, userID = login_session['user_id'])

#This page will allow signed in user to add a new item
@app.route('/catalog/new', methods=['GET', 'POST'])
def newItem():
    newItemCategory = session.query(Category).all()
    if request.method == 'POST':
        newItem = CatalogItem(title = request.form['title'], description = request.form['description'],
            category_id = request.form['category'], user_id = login_session['user_id'])
        session.add(newItem)
        flash('New Item %s Successfully added' % newItem.title)
        session.commit()
        return redirect(url_for('catalogHome'))
    else:
        return render_template('newItem.html', category = newItemCategory)

#This page will allow signed in user to add a new category
@app.route('/catalog/newcategory', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'], user_id = login_session['user_id'])
        session.add(newCategory)
        flash('New Category %s Successfully added' % newCategory.name)
        session.commit()
        return redirect(url_for('catalogHome'))
    else:
        return render_template('newCategory.html')

#This page lets you edit an item when logged in.
@app.route('/catalog/<category_name>/items/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    catalog = session.query(Category)
    editedItem = session.query(CatalogItem).filter_by(title = item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedItem.user_id != login_session['user_id']:
        return "<script> function myFunction(){alert('You are not authorized to edit this item. Please create your own item in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['category']:
            editedItem.category_id = request.form['category']
        session.add(editedItem)
        flash('%s Successfully Edited' % editedItem.title)
        session.commit()
        return redirect(url_for('categoryItems', category_name = category_name))
    else:
        return render_template('editItem.html', category_name = category_name,
            item = editedItem, catalog = catalog)

#This page lets you delete an item when logged in.
@app.route('/catalog/<category_name>/items/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    deletedItem = session.query(CatalogItem).filter_by(title = item_name).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedItem.user_id != login_session['user_id']:
        return "<script> function myFunction(){alert('You are not authorized to delete this item. Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedItem)
        flash('%s Successfully Deleted' % deletedItem.title)
        session.commit()
        return redirect(url_for('categoryItems', category_name = category_name))
    else:
        return render_template('deleteItem.html', category_name = category_name, item = deletedItem)

# Making an API Enpoint ( GET Request)
@app.route('/catalog/JSON')
def catalogHomeJSON():
    catalog = session.query(Category).all()
    return jsonify(CatalogList = [c.serialize for c in catalog])

# JSON API to view the user database
@app.route('/catalog/users/JSON')
def usersJSON():
    users = session.query(UserLogOn).all()
    return jsonify(users = [u.serialize for u in users])

# Helper functions
# Compare user signing in to database
def getUserID(email):
    try:
        userinfo = session.query(UserLogOn).filter_by(email = email).one()
        return userinfo.id
    except:
        return None

# Pull user information from the database
def getUserInfo(user_id):
    userinfo = session.query(UserLogOn).filter_by(id = user_id).one()
    return userinfo

# Add a new user to the database
def createUser(login_session):
    newUser = UserLogOn(name=login_session['username'],
        email = login_session['email'], picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    userinfo = session.query(UserLogOn).filter_by(email = login_session['email']).one()
    return userinfo.id

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)
