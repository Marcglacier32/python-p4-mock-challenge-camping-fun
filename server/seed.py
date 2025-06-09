from models import db, Scientist, Planet, Mission
from app import app

with app.app_context():
    print("Deleting existing data...")
    Mission.query.delete()
    Scientist.query.delete()
    Planet.query.delete()

    print("Seeding planets...")
    planet1 = Planet(name="TauCeti E", distance_from_earth=1234567, nearest_star="TauCeti")
    planet2 = Planet(name="Maxxor", distance_from_earth=99887766, nearest_star="Canus Minor")

    print("Seeding scientists...")
    scientist1 = Scientist(name="Mel T. Valent", field_of_study="xenobiology")
    scientist2 = Scientist(name="P. Legrange", field_of_study="orbital mechanics")

    print("Seeding missions...")
    mission1 = Mission(name="Explore TauCeti", scientist=scientist1, planet=planet1)
    mission2 = Mission(name="Study Maxxor Atmosphere", scientist=scientist2, planet=planet2)

    db.session.add_all([planet1, planet2, scientist1, scientist2, mission1, mission2])
    db.session.commit()
    print("✅ Seeding complete.")
