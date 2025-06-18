from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Event, EventRegistration, db
from .forms import RegisterForm, LoginForm, EventForm
from . import bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pw,
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('Login failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out!', 'info')
    return redirect(url_for('main.home'))

@main.route('/dashboard')
@login_required
def dashboard():
    # Pass registered events (via registrations) to template
    registered_events = [reg.event for reg in current_user.registrations]
    return render_template('dashboard.html', user=current_user, registered_events=registered_events)

@main.route('/events')
@login_required
def view_events():
    events = Event.query.order_by(Event.date.asc()).all()
    return render_template('events.html', events=events)

@main.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.role != 'creator':
        flash('Only event creators can access this page.', 'danger')
        return redirect(url_for('main.home'))

    form = EventForm()
    if form.validate_on_submit():
        new_event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            venue=form.venue.data,
            creator_id=current_user.id
        )
        db.session.add(new_event)
        db.session.commit()
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.view_events'))
    return render_template('create_event.html', form=form)

@main.route('/register/<int:event_id>', methods=['POST'])
@login_required
def register_event(event_id):
    event = Event.query.get_or_404(event_id)

    existing_registration = EventRegistration.query.filter_by(
        event_id=event.id,
        user_id=current_user.id
    ).first()

    if existing_registration:
        flash('You are already registered for this event.', 'warning')
    else:
        registration = EventRegistration(event_id=event.id, user_id=current_user.id)
        db.session.add(registration)
        db.session.commit()
        flash('Successfully registered for the event!', 'success')

    return redirect(url_for('main.view_events'))
