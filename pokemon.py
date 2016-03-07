from livingdex import db

import flask.ext.sqlalchemy as flask_sqlalchemy
import sqlalchemy.sql.schema as sqlalchemy_schema
import sqlalchemy.sql.sqltypes as sqlalchemy_types

Model = db.Model
Column = sqlalchemy_schema.Column
String = sqlalchemy_types.String
Integer = sqlalchemy_types.Integer

class Pokemon(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    number = Column(Integer)
    
    # Variations
    shinyInteger = Column(Integer)
    variant = Column(String(3))
