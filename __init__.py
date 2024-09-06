from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
db=SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"]="postgresql://postgres:root@localhost:5432/FlaskPython"

db.init_app(app)