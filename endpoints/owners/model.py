from app import db

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    cars = db.relationship('Car', backref='owner', lazy=True)
    sale_opportunity = db.Column(db.Boolean, default=True)