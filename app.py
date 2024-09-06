from html.entities import html5

from flask import request, make_response, render_template
from werkzeug.security import generate_password_hash
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