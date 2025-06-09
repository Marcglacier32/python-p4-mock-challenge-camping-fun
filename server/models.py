from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)

    missions = db.relationship('Mission', back_populates='scientist', cascade="all, delete")
    planets = association_proxy('missions', 'planet')

    serialize_rules = ('-missions.scientist',)

    @validates('name', 'field_of_study')
    def validate_not_empty(self, key, value):
        if not value or not value.strip():
            raise ValueError(f"{key} must be provided.")
        return value


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    missions = db.relationship('Mission', back_populates='planet', cascade="all, delete")
    scientists = association_proxy('missions', 'scientist')

    serialize_rules = ('-missions.planet',)


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)

    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')

    serialize_rules = ('-scientist.missions', '-planet.missions')

    @validates('name', 'scientist_id', 'planet_id')
    def validate_fields(self, key, value):
        if not value:
            raise ValueError(f"{key} must be provided.")
        return value
