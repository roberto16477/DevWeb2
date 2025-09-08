from flask import Flask

from os import name
app = Flask (__name__)

from routes import *
    
if __name__ == "__main__":
    app.run()