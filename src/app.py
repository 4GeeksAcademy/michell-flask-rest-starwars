"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorite

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

########## Metodo GET ########
#------GET USERS-------
@app.route('/users', methods=['GET'])
def get_all_users():   
    users = User.query.all()

    return jsonify([user.serialize() for user in users]), 200

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200


#------GET PEOPLE-------
@app.route('/people', methods=['GET'])
def get_all_people():
    people = People.query.all()
    all_people = [person.serialize() for person in people]

    return jsonify(all_people), 200

@app.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    people = People.query.get(people_id)

    if people is None:
        return jsonify({"error": "No people with this id"}), 404
    return jsonify(people.serialize()), 200


#------GET PLANETS-------
@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planets.query.all()

    return jsonify([planet.serialize() for planet in planets])

@app.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)

    if planet is None:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize())



#---GET USER FAVORITES---
@app.route('/users/favorites', methods=['GET'])
def get_user_favorites():
    user_id = request.args.get('user_id')  
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404

    favorites = Favorite.query.filter_by(user_id=user_id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

#---POST ADD FAVORITE PLANET---
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    planet = Planets.query.get(planet_id)

    if user is None or planet is None:
        return jsonify({"error": "User or Planet not found"}), 404

    # Verificar si ya existe el favorito
    existing_favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favorite:
        return jsonify({"error": "Favorite already exists"}), 400

    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201

#---POST ADD FAVORITE PEOPLE---
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    people = People.query.get(people_id)

    if user is None or people is None:
        return jsonify({"error": "User or People not found"}), 404

    # Verificar si ya existe el favorito
    existing_favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()
    if existing_favorite:
        return jsonify({"error": "Favorite already exists"}), 400

    new_favorite = Favorite(user_id=user_id, people_id=people_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify(new_favorite.serialize()), 201

#---DELETE FAVORITE PLANET---
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite planet deleted"}), 200

#---DELETE FAVORITE PEOPLE---
@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.args.get('user_id')
    favorite = Favorite.query.filter_by(user_id=user_id, people_id=people_id).first()

    if favorite is None:
        return jsonify({"error": "Favorite not found"}), 404

    db.session.delete(favorite)
    db.session.commit()

    return jsonify({"message": "Favorite people deleted"}), 200






