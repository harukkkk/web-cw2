# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import (
    DateField, StringField, TextAreaField,
    SelectMultipleField, SubmitField,
    PasswordField, BooleanField,
    DateTimeField, IntegerField, FloatField, FileField, SelectField)
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from flask_login import current_user
from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=64, min=1, message='Accept 1-64 chars')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, max=32, message='Accept 6-32 chars')])
    password2 = PasswordField(
        'Password Repeat', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Submit')

    def validate_username(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user is not None:
            raise ValidationError(f'User {name.data} already exist')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, max=32, message='Accept 6-32 chars')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class ArticleCreateForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), Length(min=3, max=128, message='Title Accepts 3-128 Chars')])
    content = TextAreaField('Body', validators=[DataRequired()])
    categories = SelectMultipleField('Categories', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Submit')

