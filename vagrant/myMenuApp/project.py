#!/usr/bin/python
from flask import Flask

app = Flask(__name__) # Instance of this class with the running of the application
# as the argument. name is a special variable that's automatically created when
# starting a new application and all of the imports it uses.

@app.route('/') # Decorater - wraps our fnctn inside the fnctn that flask has already created
@app.route('/hello')

def HelloWorld():
    return "Hello World"

if __name__ == '__main__': # if statement allows it to run only from python interpreter and not from any imported modules
    # __main__ is the name automatically set for the python interpreter, while most others get it set to the actual name of the file
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000) # run function to run the application; listen on all public IPs
