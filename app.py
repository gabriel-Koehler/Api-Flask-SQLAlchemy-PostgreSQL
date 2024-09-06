from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, make_response, render_template
from sqlalchemy.sql.functions import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db
from .models import User,Relation

@app.route("/")
def hello():
    users=User.query.all()
    return render_template('index.html',users=users)

@app.route("/signup",methods=["POST"])
def signup():
    data=request.json
    email=data.get("email")
    name=data.get("name")
    password=data.get("password")

    if name and email and password:
        user= User.query.filter_by(email=email).first()
        if user:
            return make_response(
                {"menssage":"Please Sign in"},
                200
            )
        user=User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {"menssage":"User Created"},
            201
        )
    return make_response(
        {"menssage":"Unable to create User"},
        500
    )
@app.route("/loggin",methods=["POST"])
def loggin():
    data=request.json
    if not data or not data.get("email") or not data.get("password"):
        return  make_response(
            "Falta de credencias",
            401
        )
    user = User.query.filter_by(email=data.get("email")).first()
    if not user:
        return make_response(
            "Usuario não existe",
            401
        )
    if check_password_hash(user.password,data.get("password")):
        token = jwt.encode({
            'id':user.id,
            'exp': datetime.now()+timedelta(minutes=30)
        },
            "secret",
            "HS256"
        )
        return make_response({'token':token},201)
    return make_response(
        'Verifique suas Credencias'
    )

def token_required(f):
    token=None
    @wraps(f)
    def decorated(*args,**kwargs):
        if 'Authorization' in request.headers:
            token=request.headers["Authorization"]
        if not token:
            return make_response({"menssage":"Token is missing"},401)
        try:
            data=jwt.decode(token,"secret",algorithms=["HS256"])
            current_user=User.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return make_response({
                "menssage":"Token is Invalid"
            },401)
        return f(current_user,*args,**kwargs)



@app.route("/relation",methods=["POST"])
def relationCreate():
    data=request.json
    amount=data.get("amount")
    user_id=data.get("userId")
    relation=Relation(id_user=user_id,amount=amount)
    try:
        db.session.add(relation)
        db.session.commit()
    except TypeError:
        print(TypeError)
    return make_response({
        "data":relation.serialize,
        "menssage":"successful"
    },200)

@app.route("/getuser",methods=["GET"])
def getUser():
    users=User.query.all()
    print()
    return make_response({
        "data":[user.serialize for user in users]
    })