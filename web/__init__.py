from flask import Flask
from dotenv import load_dotenv
from config import Config

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config.from_object(Config)
    return app