from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(64), unique=True, index=True)
	password_hash = db.Column(db.String(128))
	email = db.Column(db.String(128), unique=True)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def __repr__(self):
		return "<User {} {} {}>".format(self.id, self.username, self.email)

class Score(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	bank_name = db.Column(db.String(32))
	amount = db.Column(db.Float)

	def __repr__(self):
		return "<Score {} {} {}>".format(self.id, self.bank_name, self.amount)

class Waste_category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(db.String(32))

	def __repr__(self):
		return "<Waste Category {} {}>".format(self.id, self.name)

class Income_category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	name = db.Column(db.String(32))

	def __repr__(self):
		return "<Income Category {} {}>".format(self.id, self.name)

class Waste(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('waste_category.id'))
	score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
	amount = db.Column(db.Float)
	description = db.Column(db.String(128))

	def __repr__(self):
		return "<Waste {} {} {}>".format(self.id, self.amount, self.description)

class Income(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	category_id = db.Column(db.Integer, db.ForeignKey('income_category.id'))
	score_id = db.Column(db.Integer, db.ForeignKey('score.id'))
	amount = db.Column(db.Float)
	description = db.Column(db.String(128))

	def __repr__(self):
		return "<Income {} {} {}>".format(self.id, self.amount, self.description)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))