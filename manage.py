# import Flask-Script from Flask to help manage the development
# of application
import os
from flask.ext.script import Manager

# import the Flask app (defined in __init__.py)
from blog import app

# create instance of Manager
manager = Manager(app)

# setup the run command for the app
# name of function 'run' corresponds with argument given to 
# script at command line, eg python manage.py run
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# setup the __main__ function to call from command line
if __name__ == "__main__":
    manager.run()
