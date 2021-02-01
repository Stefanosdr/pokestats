from flask import Flask, flash, redirect
from flask import render_template, url_for
from datetime import datetime as dt
from flask_sqlalchemy import SQLAlchemy
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import requests
from pokemon_class import Pokemon
from forms import ResisterForm, PokemonTeamForm
from pokemon_team_manager import get_pokemon_triads

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.email}')"



class PokeForm(FlaskForm):
    pokemon_name = StringField('Insert a Pokemon Name:', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/", methods=["GET", "POST"])
def index():
    form = PokeForm()
    pokemon = None
    pokemon_object= None
    if form.validate_on_submit():
        pokemon = form.pokemon_name.data
        form.pokemon_name.data = ''
        try:
            pokemon_object = Pokemon(pokemon)
        except Exception as err:
            print(err)

    current_year = dt.now().year
    random_number = random.randint(1, 10)
    return render_template("index.html", num=random_number, footer_year=current_year, form=form, pokemon=pokemon_object)



@app.route("/guess/<name>")
def guess_info(name):
    agify_endpoint = f"https://api.agify.io?name={name.lower()}"
    age_response = requests.get(url=agify_endpoint)
    age = age_response.json().get("age")

    gender_endpoint = f"https://api.genderize.io?name={name.lower()}"
    gender_response = requests.get(url=gender_endpoint)
    gender = gender_response.json().get("gender")
    return render_template("name_info.html", name=name, age=age, gender=gender)


@app.route("/blog")
def get_blog():
    blog_url = "https://api.npoint.io/5abcca6f4e39b4955965"
    response = requests.get(url=blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


@app.route("/team_evaluation", methods=["GET", "POST"])
def team_evaluation():
    team_evaluation_form = PokemonTeamForm()
    pokemon_data = None
    pokemon_list = None
    if team_evaluation_form.validate_on_submit():
        pokemon_list = [
            team_evaluation_form.pokemon1.data,
            team_evaluation_form.pokemon2.data,
            team_evaluation_form.pokemon3.data,
            team_evaluation_form.pokemon4.data,
            team_evaluation_form.pokemon5.data,
            team_evaluation_form.pokemon6.data
        ]
        return render_template("team_evaluation.html", form=team_evaluation_form, pokemon_list=pokemon_list,
                               pokemon_data=get_pokemon_triads(pokemon_list))

    return render_template("team_evaluation.html", form=team_evaluation_form, pokemon_list=pokemon_list,
                           pokemon_data=pokemon_data)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = ResisterForm()
    if register_form.validate_on_submit():
        flash(f"Registration requested for user {register_form.username.data}")
        return redirect("/")
    return render_template("register.html", form=register_form)


@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)