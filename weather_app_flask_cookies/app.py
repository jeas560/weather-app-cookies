from dotenv import dotenv_values
import requests
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
)

MAX_AGE = 60 * 60 * 24 * 365 * 2

app = Flask(__name__)

config = dotenv_values(".env")
app.config["SECRET_KEY"] = config["SECRET_KEY"]
api_url = config["API_URL"]
api_key = config["API_KEY"]


def get_weather_data(city):
    url = f"{api_url}{ city }&units=metric&appid={api_key}"
    r = requests.get(url).json()
    return r


@app.route("/", methods=["GET"])
def index_get():
    if not request.cookies.get("accept"):
        flash("Aceitando cookies", "cookie_active")

    req = request.cookies.get("cidades")

    weather_data = []

    if req:
        for city in req.split(", "):
            r = get_weather_data(city)

            weather = {
                "city": city,
                "temperature": r["main"]["temp"],
                "description": r["weather"][0]["description"],
                "icon": r["weather"][0]["icon"],
            }

            weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data)


@app.route("/", methods=["POST"])
def index_post():
    req = request.cookies.get("cidades")
    err_msg = ""

    new_city = request.form.get("city").capitalize()

    if new_city and new_city != "":
        if req and (new_city in req.split(", ")):
            err_msg = "Cidade já existente na base de dados!"
            flash(err_msg, "error")
        else:
            new_city_data = get_weather_data(new_city)
            if new_city_data["cod"] == 200:
                flash("Cidade adicionada com sucesso!", "succes")
                if req:
                    req = req + ", " + new_city
                else:
                    req = new_city
            else:
                err_msg = "Cidade não encontrada!"
                flash(err_msg, "error")
    else:
        err_msg = "Favor inserir o nome da cidade no campo indicado!"
        flash(err_msg, "error")

    res = make_response(redirect(url_for("index_get")))

    if req:
        res.set_cookie("cidades", req, max_age=MAX_AGE)

    return res


@app.route("/delete/<name>")
def delete_city(name):
    cities = request.cookies.get("cidades").split(", ")
    cities.remove(name)

    flash(f"{ name } eliminada da base de dados!")

    res = make_response(redirect(url_for("index_get")))
    res.set_cookie("cidades", ", ".join(cities), max_age=MAX_AGE)

    return res


@app.route("/cookie")
def accept_cookies():
    res = make_response(redirect(url_for("index_get")))
    res.set_cookie("accept", "true", max_age=MAX_AGE)

    return res
