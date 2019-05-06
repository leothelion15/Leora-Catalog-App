import os
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem

#Defining the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Importing to the web server
class webserverHandler(BaseHTTPRequestHandler):
#Reading the database on the website
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"): #path is a variable that contains the URL sent by client to server as a string
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()

                output = ""
                output += "<html><body>"
                output += "<a href='/restaurants/new'>Add a new restaurant</a></br></br>"

                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br>"
                    output += "</br>"
                    output += "</body></html>"
                self.wfile.write(output)
                return

            #Add a new restaurant
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Add a New restaurant</h1>"
                output += "<a href = '/restaurants'>Back to List</a>"
                output += '''<form method ='POST' enctype = 'multipart/form-data' action = '/restaurants/new'>
                            <input name = 'newRestaurantName' type = 'text' placeholder = 'New Restaurant Name'>
                            <input type = 'submit' value = 'Create'> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return

            # Edit an existing restaurant
            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output +="<h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<h2>Edit the restaurant name</h2>"
                    output += "<a href = '/restaurants'>Back to List</a></br>"
                    output += '''<form method ='POST' enctype = 'multipart/form-data'
                            action = '/restaurants/%s/edit'>''' % restaurantIDPath
                    output += '''<input name = 'newRestaurantName' type = 'text'
                                placeholder = '%s'>''' % myRestaurantQuery.name
                    output += "<input type = 'submit' value = 'Rename'> </form>"
                    output += "</body></html>"
                self.wfile.write(output)

            # Delete a restaurant
            if self.path.endswith('/delete'):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body>"
                    output += "<h2>Are you sure you want to delete %s?</h2>" % myRestaurantQuery.name
                    output += "<a href = '/restaurants'>Back to List</a></br>"
                    output += '''<form method ='POST' enctype = 'multipart/form-data'
                                action = '/restaurants/%s/delete'>''' % restaurantIDPath
                    output += "<input type = 'submit' value = 'Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)


#Add a new webserver
    def do_POST(self):
        try:
            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')

                #Create new Restaurant class
                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Conent-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                #Update the Restaurant class
                if myRestaurantQuery != []:
                    myRestaurantQuery.name = messagecontent[0]
                    session.add(myRestaurantQuery)
                    session.commit()

                self.send_response(301)
                self.send_header('Conent-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                #Delete the Restaurant class
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()

                self.send_response(301)
                self.send_header('Conent-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler) #webserverHandler is class that we defined
        print "Web server running on port %s" % property
        server.serve_forever() #command to keep it constantly listening until ctrlC or closed

    except KeyboardInterrupt: #User holds CTRL+C on keyboard
            print "^C entered, stopping web server..."
            server.socket.close() #shuts down the server

if __name__ == '__main__':
    main()
