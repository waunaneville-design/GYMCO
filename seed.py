from datetime import date, timedelta

from app import create_app
from models import Exercise, Workout, WorkoutExercise, db


def seed():
    print("Clearing tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print("Seeding exercises...")
    squat = Exercise(name="Back Squat", category="strength", equipment_needed=True)
    pushup = Exercise(name="Push Up", category="strength", equipment_needed=False)
    row = Exercise(name="Rowing Machine", category="cardio", equipment_needed=True)
    plank = Exercise(name="Plank", category="core", equipment_needed=False)
    lunge = Exercise(name="Walking Lunge", category="mobility", equipment_needed=False)
    db.session.add_all([squat, pushup, row, plank, lunge])
    db.session.commit()
