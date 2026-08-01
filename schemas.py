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


    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Name cannot be blank.")

class WorkoutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = False
        sqla_session = db.session
        include_relationships = False

    id = auto_field(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1, max=300)
    )
    notes = fields.String(
        allow_none=True, load_default=None, validate=validate.Length(max=500)
    )

