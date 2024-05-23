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
from models import db, User,Planets,FavoritePlanets,FavoriteCharacters,Characters,FavoriteStarShips,StarShips
#from models import Person

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

@app.route('/user', methods=['GET'])
def handle_hello():
    #select * from user;
    all_users = User.query.all()
    user_serialized=[]
    for user in all_users:
        user_serialized.append(user.serialize())
    print(user_serialized)
    return jsonify({"data":user_serialized}), 200

@app.route('/user/<int:id>',methods=["GET"])
def get_single_user(id):
    single_user = User.query.get(id)
    if single_user==None:
        return jsonify({"msg":"No se encontro el id {} del usuario".format(id)}),400
    return jsonify({"data":single_user.serialize()}),200

@app.route("/planet", methods=["POST"])
def new_planet():
    body=request.get_json(silent=True)
    print(type(body),body)
    if body is None:
        return jsonify({"msg":"debes enviar informacion en el body"}),400
    if "name" not in body:
        return jsonify({"msg":"el campo name es obligatorio"}),400
    if "population" not in body:
        return jsonify({"msg":"el campo population es obligatorio"}),400
    new_planet = Planets()
    new_planet.name = body["name"]
    new_planet.population = body["population"]
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"msg":"nuevo planeta creado","data":new_planet.serialize()}),201

@app.route("/user/<int:id>/favorites",methods=['GET'])
def get_favorites(id):
    user=User.query.get(id)
    print (user)
    if user is None:
        return jsonify({"msg":f"El usuario cn id {id} no existe"}),404
    favorites= db.session.query(    FavoritePlanets, Planets,    FavoriteCharacters, Characters,    FavoriteStarShips, StarShips
    ).join(Planets, FavoritePlanets.planet_id == Planets.id)\
    .outerjoin(FavoriteCharacters, FavoriteCharacters.user_id == FavoritePlanets.user_id)\
    .outerjoin(Characters, FavoriteCharacters.character_id == Characters.id)\
    .outerjoin(FavoriteStarShips, FavoriteStarShips.user_id == FavoritePlanets.user_id)\
    .outerjoin(StarShips, FavoriteStarShips.starship_id == StarShips.id)\
    .filter(FavoritePlanets.user_id == id)\
    .all()
    favorite_planet_serialized=[]
    for favorite_planet,planet, favorite_character,character,favorite_starship, starship in favorites:
        favorite_planet_serialized.append({"favorite_planet":favorite_planet.id,"Planet":planet.serialize()\
                                           ,"favorite_character":favorite_character.id,"character":character.serialize()\
                                            ,"favorite_starships":favorite_starship.id,"starships":starship.serialize()})
    return jsonify({"msg":"ok","data":favorite_planet_serialized})


@app.route('/planet', methods=['GET'])
def get_planets():
    all_planets = Planets.query.all()
    planet_serialized=[]
    for planet  in all_planets:
        planet_serialized.append(planet.serialize())
    print(planet_serialized)
    return jsonify({"data":planet_serialized}), 200

@app.route('/planet/<int:id>',methods=["GET"])
def get_single_planet(id):
    single_planet = Planets.query.get(id)
    if single_planet==None:
        return jsonify({"msg":"No se encontro el id {} del planeta".format(id)}),400
    return jsonify({"data":single_planet.serialize()}),200

@app.route('/people', methods=['GET'])
def get_people():
    all_peoples = Characters.query.all()
    people_serialized=[]
    for people  in all_peoples:
        people_serialized.append(people.serialize())
    print(people_serialized)
    return jsonify({"data":people_serialized}), 200

@app.route('/people/<int:id>',methods=["GET"])
def get_single_people(id):
    single_people = Characters.query.get(id)
    if single_people==None:
        return jsonify({"msg":"No se encontro el id {} del people".format(id)}),400
    return jsonify({"data":single_people.serialize()}),200


@app.route("/people", methods=["POST"])
def new_poeple():
    body=request.get_json(silent=True)
    print(type(body),body)
    if body is None:
        return jsonify({"msg":"debes enviar informacion en el body"}),400
    if "name" not in body:
        return jsonify({"msg":"el campo name es obligatorio"}),400
    if "height" not in body:
        return jsonify({"msg":"el campo height es obligatorio"}),400
    if "mass" not in body:
        return jsonify({"msg":"el campo mass es obligatorio"}),400
    new_pople= Characters()
    new_pople.name = body["name"]
    new_pople.height = body["height"]
    new_pople.mass = body["mass"]
    db.session.add(new_pople)
    db.session.commit()
    return jsonify({"msg":"nuevo persona creada","data":new_pople.serialize()}),201

@app.route('/favorite/people/<int:people_id>',methods=["DELETE"])
def delete_sigle_favorite_people(people_id):
    single_favorite = FavoriteCharacters.query.get(people_id)
    print(single_favorite)
    # if single_favorite==None:
    #     return jsonify({"msg":"No se encontro el id {} del favorito people".format(people_id)}),400
    # db.session.delete(single_favorite)
    # db.session.commit()
    return jsonify({"msg":"se elimino correctamente la persona"}),200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
