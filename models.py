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

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Workout date is required.")
        if value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value

    @validates("duration_minutes")
    def validate_duration_minutes(self, key, value):
        if value is None:
            raise ValueError("duration_minutes is required.")
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("duration_minutes must be an integer.")
        if value <= 0 or value > 300:
            raise ValueError("duration_minutes must be between 1 and 300.")
        return value

    @validates("notes")
    def validate_notes(self, key, value):
        if value is not None and len(value) > 500:
            raise ValueError("notes must be 500 characters or fewer.")
        return value

    def __repr__(self):
        return f"<Workout {self.id}: {self.date} ({self.duration_minutes} min)>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        UniqueConstraint(
            "workout_id", "exercise_id", name="uq_workout_exercises_workout_id"
        ),
        CheckConstraint("reps IS NULL OR reps > 0", name="reps_positive"),
        CheckConstraint("sets IS NULL OR sets > 0", name="sets_positive"),
        CheckConstraint(
            "duration_seconds IS NULL OR duration_seconds > 0",
            name="duration_seconds_positive",
        ),
        CheckConstraint(
            "(reps IS NOT NULL AND sets IS NOT NULL) OR duration_seconds IS NOT NULL",
            name="reps_sets_or_duration_required",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(
        db.Integer, db.ForeignKey("workouts.id", ondelete="CASCADE"), nullable=False
    )
    exercise_id = db.Column(
        db.Integer, db.ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False
    )
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    @validates("reps", "sets", "duration_seconds")
    def validate_positive_numbers(self, key, value):
        if value is None:
            return value
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{key} must be an integer.")
        if value <= 0:
            raise ValueError(f"{key} must be a positive integer.")
        return value

    def validate_effort(self):
        """A WorkoutExercise must record either reps and sets, or a duration."""
        has_reps_and_sets = self.reps is not None and self.sets is not None
        if not has_reps_and_sets and self.duration_seconds is None:
            raise ValueError(
                "A workout exercise requires either reps and sets, "
                "or duration_seconds."
            )

    def __repr__(self):
        return (
            f"<WorkoutExercise {self.id}: workout={self.workout_id} "
            f"exercise={self.exercise_id}>"
        )


@event.listens_for(WorkoutExercise, "before_insert")
@event.listens_for(WorkoutExercise, "before_update")
def enforce_effort(mapper, connection, target):
    target.validate_effort()
