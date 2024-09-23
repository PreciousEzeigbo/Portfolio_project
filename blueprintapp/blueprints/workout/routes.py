from flask import jsonify, render_template, redirect, url_for, flash, Blueprint, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from blueprintapp.app import db
from blueprintapp.models import User, Exerciselist, Workout, Exercise, Set
from blueprintapp.models import Post, Comment
from werkzeug.utils import secure_filename
import os

workout_bp = Blueprint('workout', __name__, template_folder='templates')

# user dashboard when logged in
@workout_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    print("Workout route reached for index")  # debug line
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
        if 'new_exercise' in request.form:
            # Handle adding a new exercise
            new_exercise_name = request.form['new_exercise']
            new_exercise = Exerciselist(name=new_exercise_name)
            db.session.add(new_exercise)
            db.session.commit()
            return jsonify({'success': True, 'id': new_exercise.uid, 'name': new_exercise.name})
        else:
            # Handle adding a workout
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

    return render_template('feed.html')
@workout_bp.route('/delete', methods=['POST', 'GET'])
@login_required
def delete():
    workout_id = request.form.get('workout_id', None)
    if workout_id is None:
        flash("Workout ID not provided!", category="error")
        return redirect(url_for('workout.workout'))
    
    try:
        workout_id = int(workout_id)
        workout = Workout.query.filter_by(uid=workout_id, user_id=current_user.uid).first()
        if workout:
            db.session.delete(workout)
            db.session.commit()
            flash("Workout deleted!", category="warning")
        else:
            flash("Workout not found or you are not authorized to delete it.", category="error")
    except ValueError:
        flash("Invalid workout ID.", category="error")
    
    return redirect(url_for('workout.workout'))

@workout_bp.route('/feed', methods=['GET'])
@login_required
def feed():
    # Get all posts in descending order
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('feed.html', posts=posts)

@workout_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    if request.method == 'POST':
        # Extract data from form fields
        content = request.form.get('content')
        image = request.files.get('image')  # Assuming form allows image upload
        
        # Save image if provided
        image_url = None
        if image:
            # Ensure upload directory exists
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save the image
            image_filename = secure_filename(image.filename)  # Use secure_filename to avoid issues
            image.save(os.path.join(upload_folder, image_filename))
            image_url = 'uploads/' + image_filename  # Create the image URL

        # Create new post instance
        new_post = Post(content=content, image_url=image_url, user_id=current_user.uid)
        
        # Add the new post to the database
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Post created successfully!', 'success')
            return redirect(url_for('workout.feed'))  # Redirect to the feed
        except Exception as e:
            db.session.rollback()
            flash('Error creating post. Please try again.', 'danger')
            print(str(e))

    return render_template('create_post.html')


@workout_bp.route('/comment/<int:post_id>', methods=['POST'])
@login_required
def comment_post(post_id):
    post = Post.query.get_or_404(post_id)
    comment_content = request.form['comment']
    if comment_content:
        new_comment = Comment(content=comment_content, post_id=post.id, user_id=current_user.uid)
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    else:
        flash('Comment cannot be empty.', 'danger')

    return redirect(url_for('workout.feed'))

@workout_bp.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user in post.likes:
        post.likes.remove(current_user)
    else:
        post.likes.append(current_user)
    db.session.commit()
    return redirect(url_for('workout.feed'))


@workout_bp.route('/view/<int:workout_id>', methods=['GET'])
@login_required
def view(workout_id):
    workout = Workout.query.filter_by(uid=workout_id, user_id=current_user.uid).first()
    if workout:
        return render_template('view_workout.html', workout=workout)
    else:
        flash("Workout not found or you are not authorized to view it.", category="error")
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
