from flask import Flask
import mysql.connector

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'happy'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'maglasang'
    app.config['MYSQL_DB'] = 'ssis'

    from .constroller import views

    app.register_blueprint(views, url_prefix='/')

    return app