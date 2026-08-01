from datetime import date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, MetaData, UniqueConstraint, event
from sqlalchemy.orm import validates

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

EXERCISE_CATEGORIES = ("strength", "cardio", "mobility", "balance", "core")

class Exercise(db.Model):
    __tablename__ = "exercises"
    __table_args__ = (
        UniqueConstraint("name", name="uq_exercises_name"),
        CheckConstraint("length(trim(name)) >= 2", name="name_min_length"),
        CheckConstraint(
            "category IN ('strength', 'cardio', 'mobility', 'balance', 'core')",
            name="category_allowed",
        ),
    )


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    category = db.Column(db.String(40), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan",
    )
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True,
    )

    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name is required.")
        value = value.strip()
        if len(value) < 2:
            raise ValueError("Exercise name must be at least 2 characters long.")
        return value

    @validates("category")
    def validate_category(self, key, value):
        if not value:
            raise ValueError("Exercise category is required.")
        value = value.strip().lower()
        if value not in EXERCISE_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(EXERCISE_CATEGORIES)}."
            )
        return value
    @validates("equipment_needed")
    def validate_equipment_needed(self, key, value):
        if not isinstance(value, bool):
            raise ValueError("equipment_needed must be a boolean.")
        return value
    def __repr__(self):
        return f"<Exercise {self.id}: {self.name} ({self.category})>"

    class Workout(db.Model):
     __tablename__ = "workouts"
     __table_args__ = (
    CheckConstraint(
            "duration_minutes > 0 AND duration_minutes <= 300",
            name="duration_minutes_range",
        ),

  CheckConstraint("notes IS NULL OR length(notes) <= 500", name="notes_length"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
    )
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True,
    )
