from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class ResisterForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(8, 20)])
    email = StringField("Email: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(8,20)])
    confirm_password = PasswordField("Confirm Password: ", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class PokemonTeamForm(FlaskForm):
    pokemon1 = StringField("Pokemon 1 ", validators=[DataRequired()])
    pokemon2 = StringField("Pokemon 2 ", validators=[DataRequired()])
    pokemon3 = StringField("Pokemon 3 ", validators=[DataRequired()])
    pokemon4 = StringField("Pokemon 4 ", validators=[DataRequired()])
    pokemon5 = StringField("Pokemon 5 ", validators=[DataRequired()])
    pokemon6 = StringField("Pokemon 6 ", validators=[DataRequired()])
    submit = SubmitField("Evaluate")