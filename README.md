# GYMCO
API for a workout tracking application used by personal trainers. The API will be responsible for tracking workouts and their associated exercises. Each workout can include multiple exercises, with sets, reps, or duration attached to each. Exercises need to be reusable so a trainer can add the same exercise to various workouts. 

# 🏋️ Workout Tracker API

A Flask + SQLAlchemy based API for tracking workouts, exercises, and workout details.  
This project includes models, schemas, and seed data for managing fitness routines.

---

## 📂 Project Structure

### Models
- **Exercise**
  - Fields: `id`, `name`, `category`, `equipment_needed`
- **Workout**
  - Fields: `id`, `date`, `duration_minutes`, `notes`
- **WorkoutExercise**
  - Fields: `id`, `workout_id`, `exercise_id`, `reps`, `sets`, `duration_seconds`
  - Constraints:
    - Unique `(workout_id, exercise_id)`
    - Positive values for reps, sets, duration
    - Requires either reps+sets or duration

### Schemas
- **ExerciseSchema** – Validates exercise data (name length, category options, equipment flag).
- **WorkoutSchema** – Validates workout data (date not in future, duration range, notes length).
- **WorkoutExerciseSchema** – Validates workout-exercise data (positive reps/sets/duration, schema-level effort validation).
- **Nested Schemas** – For detailed views:
  - `WorkoutExerciseDetailSchema`
  - `WorkoutExerciseWithWorkoutSchema`
  - `WorkoutDetailSchema`
  - `ExerciseDetailSchema`

### Seed Script
- Clears tables and populates sample exercises, workouts, and workout exercises.

---

## ⚙️ Features

- ✅ Validation for fields (e.g., notes ≤ 500 chars, positive reps/sets/duration).
- ✅ Schema-level validation ensuring either reps+sets or duration is provided.
- ✅ Relationships between workouts and exercises with `back_populates`.
- ✅ Seed data for quick testing and demo.

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd workout-tracker
