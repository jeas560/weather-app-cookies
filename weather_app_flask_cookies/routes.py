from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    make_response,
    Blueprint,
)
import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
api_url = config["API_URL"]
api_key = config["API_KEY"]


MAX_AGE = 60 * 60 * 24 * 365 * 2


def get_weather_data(city):
    url = f"{api_url}{ city }&units=metric&lang=pt_br&appid={api_key}"
    r = requests.get(url).json()
    return r


main = Blueprint("main", __name__)


@main.route("/", methods=["GET"])
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
                "description": r["weather"][0]["description"].capitalize(),
                "icon": r["weather"][0]["icon"],
            }

            weather_data.append(weather)

    return render_template("weather.html", weather_data=weather_data)


@main.route("/", methods=["POST"])
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

    res = make_response(redirect(url_for("main.index_get")))

    if req:
        res.set_cookie("cidades", req, max_age=MAX_AGE)

    return res


@main.route("/delete/<name>")
def delete_city(name):
    cities = request.cookies.get("cidades").split(", ")
    cities.remove(name)

    flash(f"{ name } eliminada da base de dados!")

    res = make_response(redirect(url_for("main.index_get")))
    res.set_cookie("cidades", ", ".join(cities), max_age=MAX_AGE)

    return res


@main.route("/cookie")
def accept_cookies():
    res = make_response(redirect(url_for("main.index_get")))
    res.set_cookie("accept", "true", max_age=MAX_AGE)

    return res
