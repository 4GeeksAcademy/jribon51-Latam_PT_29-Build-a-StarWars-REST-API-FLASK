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
from models import db, User,Planets,FavoritePlanets
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
    #favorite_planets=FavoritePlanets.query.filter_by(user_id=id).all()
    # favorite_planets_serialized=[]
    # for favorite_planet in favorite_planets:
    #     favorite_planets_serialized.append(favorite_planet.serialize())
    #favorite_planets_serialized=list(map(lambda planet:planet.serialize(),favorite_planets))
    favorite_planets=db.session.query(FavoritePlanets,Planets).join(Planets).filter(FavoritePlanets.user_id==id).all()
    print(favorite_planets)
    favorite_planet_serialized=[]
    for favorite_planet,planet in favorite_planets:
        favorite_planet_serialized.append({"favorite_planet_serialized":favorite_planet.id,"planet":planet.serialize()})
    return jsonify({"msg":"ok","data":favorite_planet_serialized})

#,



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
