import responses
from dotenv import dotenv_values

config = dotenv_values(".env")
api_url = config["API_URL"]
api_key = config["API_KEY"]


def test_home(client):
    response = client.get("/")
    title = bytes("<title>Como está o tempo agora?</title>", "utf-8")
    assert title in response.data


@responses.activate
def test_add_city(client):
    responses.add(
        responses.GET,
        f"{api_url}Lima&units=metric&lang=pt_br&appid={api_key}",
        json={
            "coord": {"lon": -77.0282, "lat": -12.0432},
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
