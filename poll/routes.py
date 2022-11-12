import flask_login
from poll import app, db
from flask import render_template, request, redirect, url_for, flash
from poll.models import User, Poll
from poll.form import RegisterForm, LoginForm, PollForm
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/')
@app.route('/home')
def home():
    poll = Poll.query.all()
    for i in poll:
        print(i.owned_user)
    return render_template('home.html', poll=poll)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask_login.current_user.is_authenticated:
        flash('user already logged in ', category='info')

        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address=form.email.data).first()
        if attempted_user:
            if check_password_hash(attempted_user.password_hash, form.password.data):
                login_user(attempted_user)
                flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
                return redirect(url_for('user'))
            else:
                flash('Password does not match! Please try again', category='danger')
        else:
            flash('Email does not exist! Please enter valid email or register to login', category='danger')

    return render_template('login.html', form=form)


@app.route('/polls/<poll_id>', methods=['GET', 'POST'])
def polls(poll_id):
    poll = Poll.query.filter_by(id=poll_id)
    for i in poll:
        if request.method == 'POST':
            poll_option = request.form.get("poll_option")
            if poll_option == '1':
                i.one_count += 1
            elif poll_option == '2':
                i.two_count += 1
            elif poll_option == '3':
                i.three_count += 1
            elif poll_option == '4':
                i.four_count += 1
            else:
                flash('Please select a option', category='info')

            i.total_count += 1
            db.session.commit()
            flash('Vote submitted successfully', category='success')
            return redirect(url_for('home'))
    return render_template('polls.html', poll=poll)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = request.form
        # id_user = int(data.get('id'))
        username_s = data.get('username')
        email_s = data.get('email_address')

        # if id_user < 0:
        # flash('ID must be a positive integer', category='danger')
        # else:
        new_user = User(id=form.id.data, username=username_s.strip(), email_address=email_s.strip(),
                        password_hash=generate_password_hash(form.password1.data, method='sha256'))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash(f"Account created successfully! You are now logged in as {new_user.username}", category='success')
        return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/create-poll', methods=["GET", 'POST'])
@login_required
def create_poll():
    form = PollForm()
    if form.validate_on_submit():
        data = request.form
        id_user = int(data.get('id'))
        question = data.get('question')
        one = data.get('option1')
        two = data.get('option2')
        three = data.get('option3')
        four = data.get('option4')

        if id_user < 0:
            flash('ID must be a positive integer', category='danger')
        else:
            # '''id=form.id.data,''',
            new_poll = Poll(
                question=question.strip(),
                option_one=one.strip(),
                option_two=two.strip(),
                option_three=three.strip(),
                option_four=four.strip(),
                owner=flask_login.current_user.username)
            db.session.add(new_poll)
            db.session.commit()
            flash('Poll created successfully', category='success')
            return redirect(url_for('home'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating the poll: {err_msg}', category='danger')

    return render_template('createpoll.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home"))


@app.route('/user')
def user():
    poll = Poll.query.filter_by(owner=flask_login.current_user.username)

    return render_template('user.html', poll=poll)


@app.route('/result/<poll_id>')
def result(poll_id):
    poll = Poll.query.filter_by(id=poll_id)
    return render_template('result.html', poll=poll)


@app.route('/delete/<poll_id>')
def delete_poll(poll_id):
    flash('Poll Deleted successfully', category='success')
    poll_to_delete = Poll.query.get(poll_id)
    db.session.delete(poll_to_delete)
    db.session.commit()

    return redirect(url_for('home'))
