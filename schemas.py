from datetime import date

from marshmallow import ValidationError, fields, validate, validates, validates_schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field

from models import EXERCISE_CATEGORIES, Exercise, Workout, WorkoutExercise, db


class ExerciseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = False
        sqla_session = db.session
        include_relationships = False

    id = auto_field(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=2, max=80))
    category = fields.String(
        required=True,
        validate=validate.OneOf(EXERCISE_CATEGORIES, error="Invalid category: {input}."),
    )
    equipment_needed = fields.Boolean(load_default=False)