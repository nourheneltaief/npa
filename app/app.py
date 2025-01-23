from flask import Flask, request, redirect, render_template, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Park, User, Trail, Wildlife, Announcement, Booking, Feedback, Badge, UserBadges
from utilities import (seed_parks, create_fictive_trails, create_fictive_wildlife, create_fictive_announcements,
                       create_admin_user, fetch_weather_data, seed_badges)
import secrets, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parks.db'
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager_ = LoginManager(app)
login_manager_.login_view = "login"

db.init_app(app)


################################ LOGIN ################################

@login_manager_.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('view_parks'))
        else:
            flash('Invalid credentials. Please try again.')
    return render_template('login.html', is_logged_in=current_user.is_authenticated)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


################################ SIGNUP ################################

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists. Please choose another one.', 'danger')
            return redirect(url_for('register'))

        user_by_email = User.query.filter_by(email=email).first()
        if user_by_email:
            flash('Email already registered. Please use a different one.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            role='user'
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', is_logged_in=current_user.is_authenticated)

################################ PUBLIC ################################

@app.route('/')
def index():
    is_logged_in = current_user.is_authenticated
    return render_template('home.html', is_logged_in=is_logged_in)

@app.route('/parks')
def view_parks():
    parks = Park.query.all()
    is_admin = current_user.is_authenticated and current_user.role == 'admin'
    return render_template('parks.html', parks=parks, is_admin=is_admin,
                           is_logged_in=current_user.is_authenticated)

@app.route('/announcements')
def park_announcements_all():
    is_logged_in = current_user.is_authenticated
    parks = Park.query.all()  # Retrieve all parks
    park_announcements_ = {}

    for park in parks:
        park_announcements_[park] = Announcement.query.filter_by(park_id=park.id).all()

    return render_template('announcements.html', park_announcements=park_announcements_,
                           all_parks=True, is_logged_in=is_logged_in)

@app.route('/parks/<int:park_id>/announcements')
def park_announcements(park_id):
    is_logged_in = current_user.is_authenticated
    park = Park.query.get_or_404(park_id)
    announcements = Announcement.query.filter_by(park_id=park_id).all()
    park_announcements_ = {park: announcements}
    return render_template('announcements.html', park_announcements=park_announcements_,
                           all_parks=False, is_logged_in=is_logged_in)


@app.route("/parks/<int:park_id>", methods=["GET"])
def get_park_id(park_id):
    park = Park.query.get_or_404(park_id)
    feedbacks = Feedback.query.filter_by(park_id=park.id).all()
    is_admin = current_user.is_authenticated and current_user.role == 'admin'
    return render_template("parks_details.html", park=park, is_admin=is_admin,
                           is_logged_in=current_user.is_authenticated, feedbacks=feedbacks)

# TODO create HTML page for trails data
@app.route('/trails')
def view_trails():
    trails = Trail.query.all()
    trails_list = [
        {
            'trail_id': trail.trail_id,
            'name': trail.name,
            'park_id': trail.park_id,
            'difficulty': trail.difficulty,
            'distance': trail.distance,
            'description': trail.description,
            'created_at': trail.created_at
        }
        for trail in trails
    ]
    return jsonify(trails_list)

# TODO create HTML page for wildlife data
@app.route('/wildlife')
def view_wildlife():
    wildlives = Wildlife.query.all()
    wildlives_list = [
        {
            'wildlife_id': wildlife.wildlife_id,
            'park_id': wildlife.park_id,
            'species_name': wildlife.species_name,
            'description': wildlife.description,
            'created_at': wildlife.created_at
        }
        for wildlife in wildlives
    ]
    return jsonify(wildlives_list)


# TODO create HTML page for park_id/trail data
@app.route('/parks/<int:park_id>/trails', methods=['GET'])
def get_trails_for_park(park_id):
    park = Park.query.get_or_404(park_id)
    trails = Trail.query.filter_by(park_id=park.id).all()
    trails_list = [
        {
            'trail_id': trail.trail_id,
            'name': trail.name,
            'difficulty': trail.difficulty,
            'distance': trail.distance,
            'description': trail.description,
            'created_at': trail.created_at
        }
        for trail in trails
    ]
    return jsonify(trails_list)

# TODO create HTML page for park_id/wildlife data
@app.route('/parks/<int:park_id>/wildlife', methods=['GET'])
def get_wildlife_for_park(park_id):
    park = Park.query.get_or_404(park_id)
    wildlife_entries = Wildlife.query.filter_by(park_id=park.id).all()
    wildlife_list = [
        {
            'wildlife_id': wildlife.wildlife_id,
            'species_name': wildlife.species_name,
            'description': wildlife.description,
            'image_url': wildlife.image_url,
            'created_at': wildlife.created_at
        }
        for wildlife in wildlife_entries
    ]
    return jsonify(wildlife_list)


################################ ADMIN USER ################################

@app.route('/register-park', methods=['GET', 'POST'])
@login_required
def register_park():
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']

        image = request.files['image']
        image_filename = image.filename
        image_path = f'static/{image_filename}'
        image.save(image_path)

        new_park = Park(name=name, location=location, description=description, image_url=image_path.split("/")[1])
        db.session.add(new_park)
        db.session.commit()

        return redirect(url_for('view_parks'))

    return render_template('register_park.html', is_logged_in=current_user.is_authenticated)

@app.route('/parks/update/<int:park_id>', methods=['GET', 'POST'])
@login_required
def update_park(park_id):
    park = Park.query.get_or_404(park_id)
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        description = request.form['description']
        image = request.files['image']


        if name:
            park.name = name

        if location:
            park.location = location

        if description:
            park.description = description

        if image:
            image_filename = image.filename
            image_path = f'static/{image_filename}'
            image.save(image_path)
            park.image_url = image_path.split("/")[1]

        db.session.commit()

        return redirect(url_for('view_parks'))

    return render_template('update_park.html', park=park, is_logged_in=current_user.is_authenticated)

@app.route('/parks/delete/<int:park_id>', methods=['GET', 'POST'])
@login_required
def delete_park(park_id):
    is_admin = current_user.is_authenticated and current_user.role == 'admin'
    if is_admin:
        park = Park.query.get_or_404(park_id)

        if Trail.query.filter_by(park_id=park_id).first():
            return jsonify({'message': 'Cannot delete park. It has associated trails.'}), 400
        if Wildlife.query.filter_by(park_id=park_id).first():
            return jsonify({'message': 'Cannot delete park. It has associated wildlife entries.'}), 400
        if Announcement.query.filter_by(park_id=park_id).first():
            return jsonify({'message': 'Cannot delete park. It has associated announcements.'}), 400
        if Booking.query.filter_by(park_id=park_id).first():
            return jsonify({'message': 'Cannot delete park. It has associated bookings.'}), 400
        if Feedback.query.filter_by(park_id=park_id).first():
            return jsonify({'message': 'Cannot delete park. It has associated feedbacks.'}), 400


        db.session.delete(park)
        db.session.commit()
        flash("Park deleted successfully!", "success")
    return redirect(url_for('view_parks'))


################################ NORMAL USER ################################

@app.route('/profile')
@login_required
def user_profile():
    return render_template('profile.html', is_logged_in=current_user.is_authenticated)


@app.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    user_id = current_user.id
    bookings = Booking.query.filter_by(user_id=user_id).order_by(Booking.created_at.desc()).all()
    return render_template('bookings.html', bookings=bookings, is_logged_in=current_user.is_authenticated)

@app.route('/bookings/update/<int:booking_id>', methods=['GET', 'POST'])
@login_required
def update_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    parks = Park.query.all()  # Fetch all parks for the dropdown
    if request.method == 'POST':
        booking.activity = request.form['activity']
        booking.park_id = request.form['park_id']
        booking.date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d')
        db.session.commit()
        flash("Booking updated successfully!", "success")
        return redirect(url_for('get_bookings'))
    return render_template('update_booking.html', booking=booking, parks=parks,
                           is_logged_in=current_user.is_authenticated)

@app.route('/bookings/delete/<int:booking_id>', methods=['GET'])
@login_required
def delete_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    db.session.delete(booking)
    db.session.commit()
    flash("Booking deleted successfully!", "success")
    return redirect(url_for('get_bookings'))

@app.route('/book', methods=['GET', 'POST'])
@login_required
def create_booking():
    if request.method == 'POST':
        activity = request.form['activity']
        park_id = request.form['park_id']
        date = request.form['date']

        user_id = current_user.id

        current_user.points += 10  # Add 10 points for each booking

        booking = Booking(
            user_id=user_id,
            activity=activity,
            park_id=park_id,
            date=datetime.datetime.strptime(date, '%Y-%m-%d')
        )
        db.session.add(booking)
        db.session.commit()

        # Check and award badges
        award_badge(current_user)

        flash("Booking created successfully!", "success")
        return redirect(url_for('get_bookings'))  # Redirect after success

    parks = Park.query.all()
    return render_template('book.html', parks=parks, is_logged_in=current_user.is_authenticated)

@app.route('/parks/<int:park_id>/feedback', methods=['GET', 'POST'])
@login_required
def submit_feedback(park_id):
    park = Park.query.get_or_404(park_id)

    if request.method == 'POST':
        feedback_text = request.form.get('feedback')
        if not feedback_text:
            flash('Please provide feedback text.', 'error')
            return redirect(url_for('submit_feedback', park_id=park_id))

        new_feedback = Feedback(
            user_id=current_user.id,
            park_id=park_id,
            feedback=feedback_text
        )
        db.session.add(new_feedback)
        db.session.commit()
        flash('Feedback submitted successfully!', 'success')
        return redirect(url_for('get_park_id', park_id=park_id))

    return render_template('feedback_form.html', park=park,
                           is_logged_in=current_user.is_authenticated)

# TODO create html page for weather info
@app.route('/weather/<park_id>/<date>', methods=['GET'])
@login_required
def check_weather(park_id, date):
    park = Park.query.get_or_404(park_id)
    weather = fetch_weather_data(park.location, date)
    return jsonify(weather)

def award_badge(user):
    badges = Badge.query.all()

    for badge in badges:
        if user.points >= badge.points_required:
            user_badge = UserBadges(user_id=user.id, badge_id=badge.badge_id, badge_name=badge.badge_name)
            existing_user_badge = UserBadges.query.filter_by(user_id=user.id, badge_id=badge.badge_id).first()
            if not existing_user_badge:
                db.session.add(user_badge)
            db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    seed_parks(app, db)
    create_fictive_trails(app, db)
    create_fictive_wildlife(app, db)
    create_fictive_announcements(app, db)
    create_admin_user(app, db)
    seed_badges(app, db)
    app.run(debug=True)