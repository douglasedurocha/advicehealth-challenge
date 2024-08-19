import pytest
from app import app, db
from endpoints.owners.model import Owner
from endpoints.cars.model import Car

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['BASIC_AUTH_USERNAME'] = 'testuser'
    app.config['BASIC_AUTH_PASSWORD'] = 'testpassword'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def init_database(test_client):
    with app.app_context():
        owner = Owner(name='John Doe')
        db.session.add(owner)

        car = Car(color='blue', model='sedan', owner_id=1)
        db.session.add(car)

        db.session.commit()

    yield  # This is where the testing happens

    with app.app_context():
        db.session.remove()
        db.drop_all()