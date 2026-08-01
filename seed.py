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


    print("Seeding workouts...")
    today = date.today()
    leg_day = Workout(
        date=today, duration_minutes=60, notes="Heavy lower body session."
    )
    conditioning = Workout(
        date=today - timedelta(days=2),
        duration_minutes=35,
        notes="Cardio and core circuit.",
    )
    recovery = Workout(
        date=today - timedelta(days=5),
        duration_minutes=25,
        notes="Light mobility work.",
    )
    db.session.add_all([leg_day, conditioning, recovery])
    db.session.commit()

    print("Seeding workout exercises...")
    db.session.add_all(
        [
            WorkoutExercise(workout=leg_day, exercise=squat, reps=8, sets=5),
            WorkoutExercise(workout=leg_day, exercise=lunge, reps=12, sets=3),
            WorkoutExercise(workout=conditioning, exercise=row, duration_seconds=900),
            WorkoutExercise(workout=conditioning, exercise=plank, duration_seconds=120),
            WorkoutExercise(workout=conditioning, exercise=pushup, reps=15, sets=3),
            WorkoutExercise(workout=recovery, exercise=lunge, reps=10, sets=2),
        ]
    )
    db.session.commit()
    print("Done seeding!")


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed()
