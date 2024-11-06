from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Mapping to the database
from main.conf.db_conf import *

from flask_cors import CORS

# Generate a db instance and bind it to the app
db = SQLAlchemy(session_options={"autoflush": False})

sqlalchemy_db_uri = "mysql+pymysql://" + dbms_usr + ":" + \
    dbms_pwd + "@" + dbms_addr + ":" + dbms_port + "/" + dbms_db


class SingletonApp(object):
    """
    Get the app in singleton mode to ensure that the app is unique throughout the project
    """

    def __new__(self):
        if not hasattr(self, 'instance'):
            self.instance = Flask("OpenDataology_Service_Toolset")
            CORS(self.instance, supports_credentials=True)
            self.instance.config['DEBUG'] = True
            self.instance.config['SQLALCHEMY_DATABASE_URI'] = sqlalchemy_db_uri
            self.instance.config['SQLALCHEMY_POOL_SIZE'] = 5
            self.instance.config['SQLALCHEMY_POOL_TIMEOUT'] = 10
            self.instance.config['SQLALCHEMY_POOL_RECYCLE'] = 10
            # Changes to the database are automatically tracked
            self.instance.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
            # While initializing the app, bind the app to the DB instance
            db.init_app(self.instance)
        return self.instance  # self.instance is the app
