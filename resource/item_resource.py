from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

items = []


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank.'
    )

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': f'An item with name {name} already exists'}, 400

        data = ItemResource.parser.parse_args()

        item = dict(name=name, price=data['price'])
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'item deleted'}

    def put(self, name):
        data = ItemResource.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = dict(name=name, price=data['price'])
            items.append(item)
        else:
            item.update(data)
        return item


class ItemListResource(Resource):

    def get(self):
        return {'items': items}
