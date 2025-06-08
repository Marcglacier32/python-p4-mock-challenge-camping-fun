#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# ✅ FIRST: initialize SQLAlchemy
db.init_app(app)

# ✅ THEN: initialize Migrate
migrate = Migrate(app, db)

@app.route('/')
def home():
    return ''

from models import db, Camper, Activity, Signup
from flask import request, jsonify, make_response

# GET /campers
@app.route('/campers', methods=['GET'])
def get_campers():
    campers = Camper.query.all()
    return jsonify([camper.to_dict() for camper in campers]), 200

# POST /campers
@app.route('/campers', methods=['POST'])
def create_camper():
    data = request.get_json()
    try:
        camper = Camper(name=data['name'], age=data['age'])
        db.session.add(camper)
        db.session.commit()
        return camper.to_dict(), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

# GET /campers/<id>
@app.route('/campers/<int:id>', methods=['GET'])
def get_camper_by_id(id):
    camper = Camper.query.get(id)
    if camper:
        return camper.to_dict(rules=('activities',)), 200
    return {'error': 'Camper not found'}, 404

# GET /activities
@app.route('/activities', methods=['GET'])
def get_activities():
    activities = Activity.query.all()
    return jsonify([activity.to_dict() for activity in activities]), 200

# DELETE /activities/<id>
@app.route('/activities/<int:id>', methods=['DELETE'])
def delete_activity(id):
    activity = Activity.query.get(id)
    if activity:
        db.session.delete(activity)
        db.session.commit()
        return {}, 204
    return {'error': 'Activity not found'}, 404

# POST /signups
@app.route('/signups', methods=['POST'])
def create_signup():
    data = request.get_json()
    try:
        signup = Signup(
            time=data['time'],
            camper_id=data['camper_id'],
            activity_id=data['activity_id']
        )
        db.session.add(signup)
        db.session.commit()
        return signup.to_dict(rules=('camper', 'activity')), 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)
