from livingdex import db

import flask.ext.sqlalchemy as flask_sqlalchemy
import sqlalchemy.sql.schema as sqlalchemy_schema
import sqlalchemy.sql.sqltypes as sqlalchemy_types

Model = db.Model
Column = sqlalchemy_schema.Column
String = sqlalchemy_types.String
Integer = sqlalchemy_types.Integer

class User(Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True)
    password = Column(String(20))
    friendCode = Column(String(16))
    def __init__(self):
        self.username = ''
        self.password = ''
        self.friendCode = ''

    def __repr__(self):
        return '<Username %r>' % self.username

