from app import db
from sqlalchemy import Enum
from enum import Enum as pyEnum

class ColorEnum(pyEnum):
    yellow = 'yellow'
    blue = 'blue'
    gray = 'gray'

    def __str__(self):
        return self.value


class ModelEnum(pyEnum):
    hatch = 'hatch'
    sedan = 'sedan'
    convertible = 'convertible'

    def __str__(self):
        return self.value


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(Enum(ColorEnum), nullable=False)
    model = db.Column(Enum(ModelEnum), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'), nullable=False)