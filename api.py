from flask import Flask
# create a DB
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource , reqparse, fields , marshal_with , abort


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

api = Api(app)

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f'<User {self.username} {self.email}>'

user_args = reqparse.RequestParser()
user_args.add_argument("username",type=str,required=True,help="Username is required")
user_args.add_argument("email",type=str,required=True,help="Email is required")
user_args.add_argument("password",type=str,required=True,help="Password is required")

userFields = {
    "id":fields.Integer,
    "username":fields.String,
    "email":fields.String,
    "password":fields.String
}

class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users

    @marshal_with(userFields)
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args["name"], email=args["email"])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users,201

api.add_resource(Users,"/api/users")

@app.route('/')
def home():
    return '<h1>Hello Flask</h1>'

if __name__ == '__main__':
    app.run(debug=True)