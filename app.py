from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from resource import ItemResource, ItemListResource
from service import authenticate, identity

app = Flask(__name__)
app.secret_key = 'secret_key'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(ItemListResource, '/items')
api.add_resource(ItemResource, '/item/<string:name>')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
