from datetime import date

from marshmallow import ValidationError, fields, validate, validates, validates_schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from models import EXERCISE_CATEGORIES, Exercise, Workout, WorkoutExercise, db


