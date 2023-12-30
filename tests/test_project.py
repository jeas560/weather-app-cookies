import responses
from dotenv import dotenv_values

config = dotenv_values(".env")
api_url = config["API_URL"]
api_key = config["API_KEY"]

MAX_AGE = 60 * 60 * 24 * 365 * 2


def test_home(client):
    response = client.get("/")
    title = bytes("<title>Como está o tempo agora?</title>", "utf-8")
    assert title in response.data


def test_add_blank_city(client):
    client.post("/", data={"city": ""})

    response = client.get("/")

    assert (
        bytes("Favor inserir o nome da cidade no campo indicado!", "utf-8")
        in response.data
    )


def test_add_repeat_city(client):
    client.set_cookie("cidades", value="Lima, Brasília", max_age=MAX_AGE, path="/")

    client.post("/", data={"city": "Lima"})

    response = client.get("/")

    assert bytes("Cidade já existente na base de dados!", "utf-8") in response.data


@responses.activate
def test_add_new_city(client):
    responses.add(
        responses.GET,
        f"{api_url}Lima&units=metric&lang=pt_br&appid={api_key}",
        json={
            "weather": [{"description": "céu limpo", "icon": "01d"}],
            "main": {
                "temp": 25.14,
            },
            "cod": 200,
        },
        status=200,
    )
    client.post("/", data={"city": "Lima"})

    response = client.get("/")

    assert b"Lima" in response.data
    assert bytes("Céu limpo", "utf-8") in response.data
    assert bytes("25.14° C", "utf-8") in response.data


def test_add_wrong_city(client):
    responses.add(
        responses.GET,
        f"{api_url}Tangamandapionildo&units=metric&lang=pt_br&appid={api_key}",
        status=400,
    )
    client.post("/", data={"city": "Tangamandapionildo"})

    response = client.get("/")

    assert bytes("Cidade não encontrada!", "utf-8") in response.data
