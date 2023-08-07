#############################################################################
from app import app 
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app.models import User, Score, Waste_category, Income_category, Waste, Income
#############################################################################


@app.route("/")
@login_required
def index():
	return render_template("index.html")

@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	data = {
		'username': username,
		'score': [i for i in Score.query.filter_by(user_id=user.id)]
	}
	print(data['score'])
	return render_template('user.html', user=user, data=data)


@app.route('/waste')
def waste(username):
	user = User.query.filter_by(username=username).first_or_404()

	return render_template('waste.html')


@app.route('/income')
def income(username):
	user = User.query.filter_by(username=username).first_or_404()

	return render_template('income.html')

@app.route("/edit")
def edit_score():

	return render_template('edit_score.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		return redirect(url_for('user', username=current_user.username))
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))