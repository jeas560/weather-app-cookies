from typing import Annotated
from fastapi import FastAPI, Cookie, Request, HTTPException, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
import starlette.status as status

import requests
from dotenv import dotenv_values

config = dotenv_values(".env")
api_url = config["API_URL"]
api_key = config["API_KEY"]
secret_key = config["SECRET_KEY"]

MAX_AGE = 60 * 60 * 24 * 365 * 2


def flash(request: Request, message: str | None, category: str = "success") -> None:
    if "_messages" not in request.session:
        request.session["_messages"] = []
        request.session["_messages"].append({"message": message, "category": category})


def get_flashed_messages(request: Request):
    return request.session.pop("_messages") if "_messages" in request.session else []


def get_weather_data(cidade: str | None):
    if cidade is not None:
        url = f"{api_url}{ cidade }&units=metric&lang=pt_br&appid={api_key}"
        return requests.get(url).json()
    else:
        err_msg = "Favor inserir o nome da cidade no campo indicado!"
        print(err_msg)


middleware = [Middleware(SessionMiddleware, secret_key=secret_key)]

app = FastAPI(middleware=middleware)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates")
templates.env.globals["get_flashed_messages"] = get_flashed_messages


@app.get("/", response_class=HTMLResponse)
def root(
    request: Request,
    cidades: Annotated[str | None, Cookie()] = None,
):
    lista_dados_temporais = []

    if cidades:
        for cidade in cidades.split(", "):
            dados_temporais_api = get_weather_data(cidade)

            lista_dados_temporais.append(
                {
                    "city": cidade,
                    "temperature": dados_temporais_api["main"]["temp"],
                    "description": dados_temporais_api["weather"][0][
                        "description"
                    ].capitalize(),
                    "icon": dados_temporais_api["weather"][0]["icon"],
                }
            )
    return templates.TemplateResponse(
        "weather.html",
        {
            "request": request,
            "weather_data": lista_dados_temporais,
        },
    )


@app.post("/")
def index_post(
    request: Request,
    new_city: Annotated[str | None, Form()] = None,
    cidades: Annotated[str | None, Cookie()] = None,
    status_code=status.HTTP_201_CREATED,
):
    if not new_city:
        err_msg = "Favor inserir o nome da cidade no campo indicado!"
        flash(request, err_msg, "error")
        return RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    else:
        new_city = new_city.capitalize()

        if cidades and (new_city in cidades.split(", ")):
            err_msg = "Cidade já existente na base de dados!"
            flash(request, err_msg, "error")
        else:
            new_city_data = get_weather_data(new_city)

            if new_city_data["cod"] == 200:
                cidades = f"{cidades}, {new_city}" if cidades else new_city
            else:
                err_msg = "Cidade não encontrada!"
                flash(request, err_msg, "error")

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="cidades", value=cidades)
    return response


@app.get("/delete/{name}/", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(
    request: Request,
    name: str,
    cidades: Annotated[str | None, Cookie()] = None,
):
    list_cidades = cidades.split(", ")
    if name in list_cidades:
        list_cidades.remove(name)
        print(f"{ name } eliminada da base de dados!")
        flash(request, f"{ name } eliminada da base de dados!")
    else:
        flash(request, "Cidade não encontrada na base de dados!")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cidade não encontrada na base de dados!",
        )

    response = RedirectResponse("/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="cidades", value=", ".join(list_cidades))

    return response
