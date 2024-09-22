from flask import render_template, redirect, url_for, flash, Blueprint, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from blueprintapp.app import db
from blueprintapp.models import User, Exerciselist, Workout, Exercise, Set

workout_bp = Blueprint('workout', __name__, template_folder='templates')

# user dashboard when logged in
@workout_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('index.html')
    
@workout_bp.route('/workout')
@login_required
def workout():
    print("Workout route reached")  # Debug line
    workouts = Workout.query.filter_by(user_id=current_user.uid).order_by(Workout.date.desc()).all()
    return render_template('workout_log.html', workouts=workouts)

@workout_bp.route('/add_workout', methods=['POST', 'GET'])
@login_required
def add_workout():
    if request.method == 'POST':
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
    return render_template('add_workout.html', exercises=exercises)

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
        return redirect(url_for('workout'))

@workout_bp.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    if request.method == 'POST':
        workout_id = int(request.form['workout_id'])
        workout = Workout.query.filter_by(id=workout_id).first()
        db.session.delete(workout)
        db.session.commit()
        flash("Workout deleted!", category="warning")
        return redirect(url_for('workout.workout'))

@workout_bp.route('/profile')
@login_required
def profile():
    # Calculate exercises in the last week
    last_week = datetime.now() - timedelta(days=7)
    exercises_last_week = Workout.query.filter(
        Workout.user_id == current_user.uid,
        Workout.date >= last_week
    ).count()

    # Calculate exercises in the last month
    last_month = datetime.now() - timedelta(days=30)
    exercises_last_month = Workout.query.filter(
        Workout.user_id == current_user.uid,
        Workout.date >= last_month
    ).count()

    return render_template('profile.html',
                           exercises_last_week=exercises_last_week,
                           exercises_last_month=exercises_last_month)

@workout_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category="warning")
    return redirect(url_for('home'))  # Redirect to a public page
