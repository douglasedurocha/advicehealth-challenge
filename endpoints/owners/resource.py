from flask_restful import Resource, reqparse, request, abort
from flask_restful import fields, marshal_with, marshal
from endpoints.cars.model import Car
from .model import Owner
from app import db
from services.auth import login_required

owner_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sale_opportunity': fields.Boolean,
    'cars': fields.List(fields.Nested({
        'id': fields.Integer,
        'color': fields.String,
        'model': fields.String
    }))
}

owner_list_fields = {
    'count': fields.Integer,
    'owners': fields.List(fields.Nested(owner_fields))
}

owner_post_parser = reqparse.RequestParser()
owner_post_parser.add_argument('name', type=str, required=True, location=['json'], help='Name is required')

class OwnerResource(Resource):
    @login_required
    def get(self, owner_id=None):
        if owner_id:
            owner = Owner.query.get(owner_id)

            if not owner:
                abort(404, message='Owner not found')

            return marshal(owner, owner_fields)
        else:
            args = request.args.to_dict()
            limit = args.pop('limit', 0)
            offset = args.pop('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            owners = Owner.query.filter_by(**args).order_by(Owner.id)

            if limit:
                owners = owners.limit(limit)

            if offset:
                owners = owners.offset(offset)

            owners = owners.all()

            return marshal({
                'count': len(owners),
                'owners': [marshal(owner, owner_fields) for owner in owners]
            }, owner_list_fields)
    
    @login_required
    @marshal_with(owner_fields)
    def post(self):
        args = owner_post_parser.parse_args()

        owner = Owner(**args)
        db.session.add(owner)
        db.session.commit()

        return owner, 201
    
    @login_required
    @marshal_with(owner_fields)
    def put(self, owner_id=None):
        owner = Owner.query.get(owner_id)

        if not owner:
            abort(404, message='Owner not found')

        if 'name' in request.json:
            owner.name = request.json['name']

        db.session.commit()
        return owner
    
    @login_required
    @marshal_with(owner_fields)
    def delete(self, owner_id):
        owner = Owner.query.get(owner_id)

        if not owner:
            abort(404, message="Owner not found")

        # Delete all cars owned by this owner
        cars = Car.query.filter_by(owner_id=owner_id).all()
        for car in cars:
            db.session.delete(car)

        db.session.delete(owner)
        db.session.commit()

        return owner