from . import db
from sqlalchemy.sql import func
class User(db.Model):
    __tablename__="User"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    email = db.Column(db.String(100),nullable=True,unique=True)
    cread_at= db.Column(db.DateTime(timezone=True),server_default=func.now())
    relation = db.relationship('Relation',backref="User")

    def __repr__(self):
        return f'<User {self.name} {self.id}>'
    @property
    def serialize(self):
        relation= Relation.query.filter_by(id_user=self.id).first()
        relation_data = relation.serialize if relation else None
        # print(relation_data)
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "password":self.password,
            "create_time":self.cread_at,
            "amount":relation_data
        }
class Relation(db.Model):
    __tablename__="Relation"
    id=db.Column(db.Integer,primary_key=True)
    amount=db.Column(db.Numeric(10,2),default=0)
    id_user=db.Column(db.Integer,db.ForeignKey("User.id"))
    created_at=db.Column(db.DateTime(timezone=True),server_default=func.now())

    def __repr__(self):
        return f'<{self.id} {self.id_user}>'

    @property
    def serialize(self):
        return {
            "id":self.id,
            "id_user":self.id_user,
            "amount":self.amount,
            "created_at":self.created_at
        }