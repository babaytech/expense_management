#############################################################################
from app import app, db
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm, CreateScoreForm, EditScoreForm
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
	return render_template('user.html', title="Главная Страница", user=user, data=data)


@app.route('/waste/<username>')
def waste(username):
	user = User.query.filter_by(username=username).first_or_404()

	return render_template('waste.html', title="Главная Страница")


@app.route('/income/<username>')
def income(username):
	user = User.query.filter_by(username=username).first_or_404()

	return render_template('income.html', title="Главная Страница")


@app.route('/create_score/<username>', methods=['GET', 'POST'])
def create_score(username):
	user = User.query.filter_by(username=username).first_or_404()
	form = CreateScoreForm()

	if form.validate_on_submit():
		score = Score(user_id=user.id,
					  bank_name=form.name_bank.data,
					  amount=form.start_score.data)
		print(score)
		db.session.add(score)
		db.session.commit()

		return redirect(url_for('user', username=user.username))


	return render_template('create_score.html', title="Главная Страница", form=form)


@app.route("/edit/<username>", methods=['GET', 'POST'])
def edit_score(username):
	user = User.query.filter_by(username=username).first_or_404()
	score = Score.query.filter_by(user_id=user.id)
	print([i for i in Score.bank_name])
	form = EditScoreForm()

	if form.validate_on_submit():
		score.name_bank = form.bank_name.data
		score.amount = form.start_score.data
		db.session.commit()
		

	elif request.method == 'GET':
		pass


	return render_template('edit_score.html', title="Главная Страница", form=form)


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
	return render_template('login.html', title='Вход', form=form)


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
	return render_template('register.html', title='Регистрация', form=form)


@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))