from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from resources import RandomNumberResource
from auth import authenticate

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Defina uma chave secreta para JWT
api = Api(app)
jwt = JWTManager(app)

# Dicionário para armazenar dados do usuário em memória
users = {}

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='Nome de usuário', required=True)
        parser.add_argument('email', help='Endereço de e-mail', required=True)
        data = parser.parse_args()

        username = data['username']
        email = data['email']

        # Simplesmente armazene o usuário em memória neste exemplo
        users[username] = {'email': email}

        return {'message': 'Usuário registrado com sucesso'}, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='Nome de usuário', required=True)
        data = parser.parse_args()

        username = data['username']

        # Verifique se o usuário está registrado em memória (substitua isso por um banco de dados em um aplicativo real)
        if username in users:
            access_token = create_access_token(identity=username)
            users[username]['access_token'] = access_token  # Armazene o token na memória
            return {'access_token': access_token, 'username': username}, 200
        else:
            return {'message': 'Usuário não registrado'}, 401

api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(RandomNumberResource, '/randomico/<int:min_val>/<int:max_val>', resource_class_kwargs={'auth': lambda token: authenticate(token, users)})

if __name__ == '__main__':
    app.run(debug=True)
