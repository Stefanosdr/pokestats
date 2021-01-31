from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ResisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(8, 20)])
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(8,20)])
    confirm_password = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')