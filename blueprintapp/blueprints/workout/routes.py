from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from blueprintapp.app import db
from blueprintapp.models import User, Exerciselist, Workout, Exercise, Set

workout_bp = Blueprint('workout', __name__, template_folder='templates')


@workout_bp.route('/workout')
@login_required
def workout_log():
    workouts = Workout.query.filter_by(user_id=current_user.uid).order_by(Workout.date.desc()).all()
    return render_template('workout/workout_log.html', workouts=workouts)

@workout_bp.route('/add_workout', methods=['POST', 'GET'])
@login_required
def add_workout():
    if request.method == 'POST':
        user = User.query.filter_by(username=current_user.username).first()
        workout = Workout(date=datetime.now(), user_id=current_user.uid)
        exercise_count = int(request.form['exercise_count'])

        for exercise_num in range(1, exercise_count + 1):
            exercise = Exercise(order=exercise_num, exercise_id=request.form['exercise' + str(exercise_num)], workout=workout)
            weights = request.form.getlist('weight' + str(exercise_num))
            reps = request.form.getlist('reps' + str(exercise_num))
            set_order = 1
            for weight, rep in zip(weights, reps):
                work_set = Set(order=set_order, exercise=exercise, weight=weight, reps=rep)
                set_order += 1

        db.session.add(workout)
        db.session.commit()
        flash("Workout Added!", category="success")
        return redirect(url_for('workout.add_workout'))

    exercises = Exerciselist.query.all()
    return render_template('workout/add_workout.html', exercises=exercises)

@workout_bp.route('/edit', methods=['POST', 'GET'])
@login_required
def edit():
    if request.method == 'POST':
        workout_id = int(request.form['workout_id'])
        workout = Workout.query.filter_by(id=workout_id).first()
        for exercise in workout.exercises:
            for set in exercise.sets:
                set.weight = request.form['weight' + str(set.id)]
                set.reps = request.form['reps' + str(set.id)]
        db.session.commit()
        flash("Workout updated!", category="success")
        return redirect(url_for('workout.workout_log'))

@workout_bp.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    if request.method == 'POST':
        workout_id = int(request.form['workout_id'])
        workout = Workout.query.filter_by(id=workout_id).first()
        db.session.delete(workout)
        db.session.commit()
        flash("Workout deleted!", category="warning")
        return redirect(url_for('workout.workout_log'))
