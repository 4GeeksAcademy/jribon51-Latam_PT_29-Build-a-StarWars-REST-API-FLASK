from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return 'usuario con email {}'.format(self.email)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Planets(db.Model):
    __tablename__='planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    population = db.Column(db.Integer,nullable=False)

    def __repr__(self):
        return f'Planets {self.id} {self.name} '

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }

class FavoritePlanets(db.Model):
    __tablename__= "favorite_planets"
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user=db.relationship(User);
    planet_id=db.Column(db.Integer,db.ForeignKey('planets.id'),nullable=False)
    planet=db.relationship(Planets)

    def __repr__(self):
        return f'al usuario  {self.user_id} le gusta el planeta {self.planet_id}'
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }

class Characters(db.Model):
    __tablename__="characters"
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    height=db.Column(db.Integer,nullable=False)
    mass=db.Column(db.Integer,nullable=False)
    
    def __repr__(self):
        return f'info characters {self.name} {self.height} {self.mass}'
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass":self.mass,
        }


class FavoriteCharacters(db.Model):
    __tablename__="favorite_characters"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user=db.relationship(User);
    character_id=db.Column(db.Integer,db.ForeignKey('characters.id'),nullable=False)
    planet=db.relationship(Characters)

    def __repr__(self):
        return f'info FavoriteCharacters {self.user_id} {self.character_id} '
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass":self.mass,
        }


class StarShips(db.Model):
    __tablename__="starships"
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    model = db.Column(db.Integer, unique=True, nullable=False)
    lenght = db.Column(db.Integer, unique=True, nullable=False)

    def __repr__(self):
        return f'info StarShips {self.name} {self.model} {self.lenght} '
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "lenght":self.lenght,
        }


class FavoriteStarShips(db.Model):
    __tablename__="favorite_starShips"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    user=db.relationship(User);
    starship_id=db.Column(db.Integer,db.ForeignKey('starships.id'),nullable=False)
    starships=db.relationship(StarShips)

    def __repr__(self):
        return f'info FavoriteCharacters {self.id} {self.user_id}  {self.starship_id} '
    
    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "starship_id": self.starship_id,
        }