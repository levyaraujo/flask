import jwt
from resources.times import Times, Time
from resources.user import User, UserRegister, UserLogin
from flask import Flask
from flask_restful import Api
from alchemy import db
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///storage.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '!?Ei39W#hv}'
jwt = JWTManager(app)


@app.before_first_request
def create_database():
    db.create_all()


api.add_resource(Times, '/times')
api.add_resource(Time, '/times/<string:time_id>')
api.add_resource(User, '/usuarios/<int:user_id>')
api.add_resource(UserRegister, '/cadastro')
api.add_resource(UserLogin, '/login')
if __name__ == '__main__':
    from alchemy import db
    db.init_app(app)
    app.run(debug=True)