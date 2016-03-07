from livingdex import db

import flask.ext.sqlalchemy as flask_sqlalchemy
import sqlalchemy.sql.schema as sqlalchemy_schema
import sqlalchemy.sql.sqltypes as sqlalchemy_types

Model = db.Model
Column = sqlalchemy_schema.Column
Integer = sqlalchemy_types.Integer

class UserPokemonMap(Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    pokemon_id = Column(Integer)

    def __init__(self, userID, pokemonID):
        self.user_id = userID
        self.pokemon_id = pokemonID
