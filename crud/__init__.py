import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from crud.celery_basic import make_celery
from flask_caching import Cache
from logging import FileHandler, WARNING


books = ""
title_book=""

config = {
	"DEBUG": True,
#CACHE_TYPE": "simple",
	"CACHE_DEFAULT_TIMEOUT": 300000000,
	'CACHE_TYPE': 'redis',
    'CACHE_KEY_PREFIX': 'fcache',
    'CACHE_REDIS_HOST': 'localhost',
    'CACHE_REDIS_PORT': '6379',
    'CACHE_REDIS_URL': 'redis://localhost:6379/1'
}
#project_dir = os.path.dirname(os.path.abspath(__file__))


database_file = "postgresql+psycopg2://kapil:kapil@localhost/assignment1"#.format(os.path.join(project_dir, "bookdatabase.db"))


app = Flask(__name__)

app.config.from_mapping(config)

app.config['CELERY_BROKER_URL'] ='amqp://localhost//'

app.config['CELERY_BACKEND'] = 'db+postgresql+psycopg2://kapil:kapil@localhost/celeryassigndb'

app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config['SECRET_KEY'] = '123d49b71501ccb96af126a151a6148a'

celery = make_celery(app)

cache = Cache(app)

db = SQLAlchemy(app)

file_handler = FileHandler('errorlog.txt')
file_handler.setLevel(WARNING)

app.logger.addHandler(file_handler)

from crud import routes
from crud import tasks
