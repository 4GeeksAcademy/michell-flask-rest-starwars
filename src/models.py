from flask_sqlalchemy import SQLAlchemy
import json

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    favorites = db.relationship("Favorite", backref= "User", lazy=True)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active
        }



class People(db.Model):
    __tablename__ = "Person"

    id = db.Column(db.Integer, primary_key=True)
    birth_year = db.Column(db.String(150), nullable=False)
    eye_color = db.Column(db.String(150), nullable=False)
    gender = db.Column(db.String(150), nullable=False)
    hair_color = db.Column(db.String(150), nullable=False)
    height = db.Column(db.String(150), nullable=False)
    homeworld = db.Column(db.String(150), nullable=False)
    mass = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    skin_color = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(150), nullable=False)

    favorites = db.relationship("Favorite", backref= "People", lazy=True)
    
    def serialize(self):
        return {
            "person_id": self.id,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "homeworld": self.homeworld,
            "mass": self.mass,
            "name": self.name,
            "skin_color": self.skin_color,
            "url": self.url
        }


class Planets(db.Model):
    __tablename__ = "Planets"

    id = db.Column(db.Integer, primary_key=True)
    climate = db.Column(db.String(150), nullable=False)
    diameter = db.Column(db.String(150), nullable=False)
    gravity = db.Column(db.String(150), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    orbital_period = db.Column(db.String(150), nullable=False)
    population = db.Column(db.String(150), nullable=False)
    residents = db.Column(db.ARRAY(db.String), nullable=False)
    rotation_period = db.Column(db.String(150), nullable=False)
    surface_water = db.Column(db.String(150), nullable=False)
    terrain = db.Column(db.String(150), nullable=False)
    url = db.Column(db.String(150), nullable=False)

    favorites = db.relationship("Favorite", backref= "Planets", lazy=True)

    def serialize(self):
        return {
            "planet_id": self.id,
            "climate": self.climate,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "name": self.name,
            "orbital_period": self.orbital_period,
            "population": self.population,
            "residents": self.residents,
            "rotation_period": self.rotation_period,
            "surface_water": self.surface_water,
            "terrain": self.terrain,
            "url": self.url
        }



class Favorite(db.Model):
    __tablename__ = "Favorite"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey(Planets.id))
    people_id = db.Column(db.Integer, db.ForeignKey(People.id))

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
            "people_id": self.people_id
        }