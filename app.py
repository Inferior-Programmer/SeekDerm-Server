from flask import Flask
from flask_graphql import GraphQLView
from collections import namedtuple
from graphene import ObjectType, String, Int, Schema, Field,Boolean, List 
from fireBaseCallers import UserAndAnimeDatabase
import coder

app = Flask(__name__)


@app.route('/')
def index():
    return 'API FOR APPCON!'


fb = UserAndAnimeDatabase()


UserValueObject = namedtuple("User", ["username", "password", "data", "ids"])
LoginValueObject = namedtuple("Login", ["user", "success"]) 
SignUpValueObject = namedtuple("SignUp", ["user", "success"])


class User(ObjectType): 
    username = String()
    password = String()
    ids = Int() 
    data = String()

class Login(ObjectType):
    user = Field(User) 
    success = Boolean()


class SignUp(ObjectType): 
    user = Field(User) 
    success = Boolean() 
    
class Query(ObjectType):
    hello = String(name=String(default_value="world"))
    number = Int(numbers=Int(default_value=-1))
    login = Field(Login,username = String(default_value="-1"), password=String(default_value=""))
    signup = Field(SignUp,username = String(default_value="-1"), password=String(default_value=""))
    predictions = String(val=String(default_value="-1"))

    def resolve_login(root, info, username, password):
        vals = fb.login(username, password)
        if(vals != -1):
            return LoginValueObject(user = UserValueObject(username = username, password = vals['password'], data = vals['data'], ids=vals['userId']), success=True)
        return LoginValueObject(user = UserValueObject(username = " ", password = " ", data = " ", ids=-1), success=False)
    def resolve_signup(root, info, username, password):
        vals = fb.signup(username, password)
        if(vals != -1):
            return SignUpValueObject(user = UserValueObject(username = username, password = password, data = " ", ids=vals), success=True)
        return SignUpValueObject(user = UserValueObject(username = " ", password = " ", data = " ", ids=-1), success=False)
    def resolve_predictions(root, info, val):
        return coder.make_prediction_from_base64(val)
    
schema = Schema(query=Query)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

if __name__ == '__main__':
    app.run(debug=True)
