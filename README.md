# GYMCO

API for a workout tracking application used by personal trainers. The API tracks workouts and
their associated exercises. Each workout can include multiple exercises, with sets, reps, or
duration attached to each. Exercises are reusable, so a trainer can add the same exercise to
various workouts.

Built with Flask, SQLAlchemy, Flask-Migrate, and Marshmallow.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export FLASK_APP=app.py
flask db upgrade          # create the SQLite database in instance/app.db
python seed.py            # reset and seed sample data
flask run -p 5555         # or: python app.py
```

Jump into the shell to explore relationships and validations:

```bash
flask shell               # db, Exercise, Workout, WorkoutExercise are preloaded
```

## Models

| Model | Columns |
| --- | --- |
| `Exercise` | `id`, `name`, `category`, `equipment_needed` |
| `Workout` | `id`, `date`, `duration_minutes`, `notes` |
| `WorkoutExercise` | `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds` |

Relationships:

- A `WorkoutExercise` belongs to a `Workout` and to an `Exercise`.
- A `Workout` has many `WorkoutExercises`, and many `Exercises` through them.
- An `Exercise` has many `WorkoutExercises`, and many `Workouts` through them.
- Deleting a `Workout` or an `Exercise` cascades to its `WorkoutExercises`.

## Validations

**Table constraints**

- `exercises.name` unique, and at least 2 non-blank characters.
- `exercises.category` restricted to `strength`, `cardio`, `mobility`, `balance`, `core`.
- `workouts.duration_minutes` between 1 and 300; `workouts.notes` at most 500 characters.
- `workout_exercises` unique on (`workout_id`, `exercise_id`); `reps`, `sets`, and
  `duration_seconds` must be positive when present, and a row must have either reps *and* sets,
  or a duration.
- `NOT NULL` on every required column plus foreign keys with `ON DELETE CASCADE`.

**Model validations** (`@validates`)

- `Exercise.name` is required, trimmed, and at least 2 characters.
- `Exercise.category` is normalized to lowercase and must be an allowed category.
- `Workout.date` is required and cannot be in the future.
- `Workout.duration_minutes` must be an integer between 1 and 300.
- `WorkoutExercise.reps` / `sets` / `duration_seconds` must be positive integers, and a
  `before_insert`/`before_update` hook requires reps + sets or a duration.

**Schema validations** (Marshmallow)

- `ExerciseSchema`: `name` required with length 2–80 and non-blank, `category` restricted to the
  allowed values.
- `WorkoutSchema`: `date` required and not in the future, `duration_minutes` in range 1–300,
  `notes` at most 500 characters.
- `WorkoutExerciseSchema`: positive `reps`/`sets`/`duration_seconds`, plus a `@validates_schema`
  rule requiring reps + sets or a duration.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| GET | `/workouts` | List all workouts |
| GET | `/workouts/<id>` | Show a workout with its exercises and reps/sets/duration data |
| POST | `/workouts` | Create a workout |
| DELETE | `/workouts/<id>` | Delete a workout and its workout exercises |
| GET | `/exercises` | List all exercises |
| GET | `/exercises/<id>` | Show an exercise with its associated workouts |
| POST | `/exercises` | Create an exercise |
| DELETE | `/exercises/<id>` | Delete an exercise and its workout exercises |
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with reps/sets/duration |

Example requests:

```bash
curl -X POST http://localhost:5555/exercises \
  -H "Content-Type: application/json" \
  -d '{"name": "Burpee", "category": "cardio", "equipment_needed": false}'

curl -X POST http://localhost:5555/workouts \
  -H "Content-Type: application/json" \
  -d '{"date": "2026-08-01", "duration_minutes": 45, "notes": "Conditioning"}'

curl -X POST http://localhost:5555/workouts/1/exercises/1/workout_exercises \
  -H "Content-Type: application/json" \
  -d '{"reps": 10, "sets": 3}'
```

Validation failures return `400` with an `errors` payload; missing records return `404`.
