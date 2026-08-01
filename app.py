from flask import Flask, jsonify, request
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from config import Config
from models import Exercise, Workout, WorkoutExercise, db
from schemas import (
    exercise_detail_schema,
    exercise_schema,
    exercises_schema,
    workout_detail_schema,
    workout_exercise_detail_schema,
    workout_exercise_schema,
    workout_schema,
    workouts_schema,
)

migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    import os

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.shell_context_processor
    def shell_context():
        return {
            "db": db,
            "Exercise": Exercise,
            "Workout": Workout,
            "WorkoutExercise": WorkoutExercise,
        }

    register_routes(app)
    register_error_handlers(app)
    return app

def register_error_handlers(app):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return jsonify({"errors": error.messages}), 400

    @app.errorhandler(404)
    def handle_not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

def register_routes(app):
    @app.get("/")
    def index():
        return jsonify({"message": "GYMCO workout API"}), 200


