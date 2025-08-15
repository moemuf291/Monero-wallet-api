from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_apscheduler import APScheduler

db = SQLAlchemy()
ma = Marshmallow()
scheduler = APScheduler() 