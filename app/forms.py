############################################################################
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
import email_validator
############################################################################

class LoginForm(FlaskForm):
	username = StringField('Имя Пользователя', validators=[DataRequired()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	remember_me = BooleanField('Запомнить Меня')
	submit = SubmitField('Вход')


class RegistrationForm(FlaskForm):
	username = StringField('Имя Пользователя', validators=[DataRequired()])
	email = StringField('Почта', validators=[DataRequired(), Email()])
	password = PasswordField('Пароль', validators=[DataRequired()])
	password2 = PasswordField('Повторить Пароль', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Регистрация')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username.')

	def vaildate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address')


class CreateScoreForm(FlaskForm):
	name_bank = StringField("Название Банка", validators=[DataRequired()])
	start_score = FloatField("Начальный Баланс", validators=[DataRequired()])
	submit = SubmitField("Сохранить")


class EditScoreForm(FlaskForm):
	name_bank = StringField("Название Банка", validators=[DataRequired()])
	start_score = FloatField("Начальный Баланс", validators=[DataRequired()])
	submit = SubmitField('Сохранить')

class CreateIncomeCategoryForm(FlaskForm):
	name_category = SubmitField("Название Категории", validators=[DataRequired()])
	submit = SubmitField("Сохранить")