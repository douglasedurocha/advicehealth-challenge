import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://carford:carford@db/carford'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('ADMIN_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('ADMIN_PASSWORD')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
api.prefix = '/api'

from endpoints.owners.resource import OwnerResource
from endpoints.cars.resource import CarResource

api.add_resource(OwnerResource, '/owners', '/owners/<int:owner_id>')
api.add_resource(CarResource, '/cars', '/cars/<int:car_id>')


if __name__ == '_main_':
    app.run()