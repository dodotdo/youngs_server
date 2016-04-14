from flask_script import Manager
from flask import current_app
from database import db
from youngs_logger import Log
from youngs_app import youngs_app

manager = Manager(youngs_app)

@manager.command
def dropdb():
    db.init_app(current_app)
    db.drop_all()

@manager.command
def createdb():
    db.init_app(current_app)
    result = db.create_all()
    Log.info(result)

if __name__ == "__main__":
    manager.run()