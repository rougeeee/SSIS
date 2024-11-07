from flask import Flask
import mysql.connector
import cloudinary
import cloudinary.uploader

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'happy'

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'maglasang'
    app.config['MYSQL_DB'] = 'ssis'

    cloudinary.config(
        cloud_name="dg8n4acmb",
        api_key="275737612612121",
        api_secret="Nf-YWaKpI6-4SYa1byZZeTXFY9o"
    )

    from .constroller import views

    app.register_blueprint(views, url_prefix='/')

    return app