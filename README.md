# weather-app-flask-cookies

Projeto de estudo flask e utilização de cookies do browser.

## Objetivos da implementação

- Extração de dados da API da `Openweathermap`
- Apresentação dos dados de Temperatura e descrição do tempo numa tela amigável e responsiva
- Armazenamento dos dados em cookies do browser para entregar uma experiência personalizada pra cada usuário e sem precisar criar uma conta pra utilizar o serviço

## 📦 Package manager

Foi utilizado `poetry` como gerenciador de pacotes. Você pode instalar `poetry` seguindo as instruções [aqui](https://python-poetry.org/docs/#installation).

Favor **Não** utilizar `pip` ou `conda` para instalar as dependencias. Para isso, utilize o seguinte comando:

```bash
poetry install
```

## Formatação de código com `black`

Foi utilizado `black` para reformatar o código executando o seguinte comando:

```bash
black weather_app_cookies 
```

## 🤖 Scripts de automação

Em construção

## 🧪 Testes

(Ainda em construção)

Utilizaremos `pytest` para testar nosso código. Você pode executar os testes executando o seguinte comando:

```bash
poetry run pytest
```

## Inicializando o servidor

Para inicializar o servidor utilize o comando:

```bash
poetry run flask --app weather_app_flask_cookies/app run
```
