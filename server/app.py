from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Scientist, Planet, Mission

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return {'message': 'Cosmic Travel API running 🚀'}

### Scientists ###

@app.route('/scientists', methods=['GET'])
def get_scientists():
    scientists = Scientist.query.all()
    return jsonify([s.to_dict(rules=('-missions',)) for s in scientists])


@app.route('/scientists/<int:id>', methods=['GET'])
def get_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    return scientist.to_dict()


@app.route('/scientists', methods=['POST'])
def create_scientist():
    data = request.get_json()
    try:
        new_scientist = Scientist(
            name=data['name'],
            field_of_study=data['field_of_study']
        )
        db.session.add(new_scientist)
        db.session.commit()
        return new_scientist.to_dict(), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route('/scientists/<int:id>', methods=['PATCH'])
def update_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    data = request.get_json()
    try:
        if 'name' in data:
            scientist.name = data['name']
        if 'field_of_study' in data:
            scientist.field_of_study = data['field_of_study']
        db.session.commit()
        return scientist.to_dict(), 202
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


@app.route('/scientists/<int:id>', methods=['DELETE'])
def delete_scientist(id):
    scientist = Scientist.query.get(id)
    if not scientist:
        return jsonify({"error": "Scientist not found"}), 404
    db.session.delete(scientist)
    db.session.commit()
    return '', 204

### Planets ###

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([p.to_dict(rules=('-missions',)) for p in planets])


### Missions ###

@app.route('/missions', methods=['POST'])
def create_mission():
    data = request.get_json()
    try:
        new_mission = Mission(
            name=data['name'],
            scientist_id=data['scientist_id'],
            planet_id=data['planet_id']
        )
        db.session.add(new_mission)
        db.session.commit()
        return new_mission.to_dict(), 201
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 400


if __name__ == '__main__':
    app.run(port=5555, debug=True)
