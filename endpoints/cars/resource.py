from flask_restful import Resource, reqparse, request, abort
from flask_restful import fields, marshal_with, marshal
from endpoints.owners.model import Owner
from .model import Car, ColorEnum, ModelEnum
from app import db
from services.auth import login_required

car_fields = {
    'id': fields.Integer,
    'color': fields.String,
    'model': fields.String,
    'owner_id': fields.Integer
}

car_list_fields = {
    'count': fields.Integer,
    'cars': fields.List(fields.Nested(car_fields))
}

cars_post_parser = reqparse.RequestParser()
cars_post_parser.add_argument('color', type=str, required=True, location=['json'],
                              help='Color is required')
cars_post_parser.add_argument('model', type=str, required=True, location=['json'],
                              help='Model is required')
cars_post_parser.add_argument('owner_id', type=int, required=True, location=['json'],
                              help='Owner ID is required')

class CarResource(Resource):
    @login_required
    def get(self, car_id=None):
        if car_id:
            car = Car.query.get(car_id)

            if not car:
                abort(404, message='Car not found')

            return marshal(car, car_fields)
        else:
            args = request.args.to_dict()
            limit = args.pop('limit', 0)
            offset = args.pop('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            cars = Car.query.filter_by(**args).order_by(Car.id)

            if limit:
                cars = cars.limit(limit)

            if offset:
                cars = cars.offset(offset)

            cars = cars.all()

            return marshal({
                'count': len(cars),
                'cars': [marshal(car, car_fields) for car in cars]
            }, car_list_fields)
    
    @login_required
    @marshal_with(car_fields)
    def post(self):
        args = cars_post_parser.parse_args()

        if args['color'] not in [color.value for color in ColorEnum]:
            abort(400, message=f"Invalid color '{args['color']}'. Must be one of {', '.join([color.value for color in ColorEnum])}.")

        if args['model'] not in [model.value for model in ModelEnum]:
            abort(400, message=f"Invalid model '{args['model']}'. Must be one of {', '.join([model.value for model in ModelEnum])}.")
        
        owner = Owner.query.get(args['owner_id'])
        if not owner:
            abort(400, message=f"Owner with ID '{args['owner_id']}' does not exist.")
        owner.sale_opportunity = False

        car = Car(**args)
        db.session.add(car)
        db.session.commit()

        return car, 201
    
    @login_required
    @marshal_with(car_fields)
    def put(self, car_id=None):
        car = Car.query.get(car_id)

        if not car:
            abort(404, message='Car not found')

        if 'color' in request.json:
            if request.json['color'] not in [color.value for color in ColorEnum]:
                abort(400, message=f"Invalid color '{request.json['color']}'. Must be one of {', '.join([color.value for color in ColorEnum])}.")
            car.color = request.json['color']

        if 'model' in request.json:
            if request.json['model'] not in [model.value for model in ModelEnum]:
                abort(400, message=f"Invalid model '{request.json['model']}'. Must be one of {', '.join([model.value for model in ModelEnum])}.")
            car.model = request.json['model']

        if 'owner_id' in request.json:
            owner = Owner.query.get(request.json['owner_id'])
            if not owner:
                abort(400, message=f"Owner with ID '{request.json['owner_id']}' does not exist.")
            car.owner_id = request.json['owner_id']
            owner.sale_opportunity = False

        db.session.commit()

        return car
    
    @login_required
    def delete(self, car_id):
        car = Car.query.get(car_id)

        if not car:
            abort(404, message="Car not found")

        db.session.delete(car)
        db.session.commit()

        return {}, 204