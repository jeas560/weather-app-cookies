# weather-app-flask-cookies

Projeto de estudo flask e utilização de cookies do browser.

## Objetivos da implementação

- [x] Extração de dados da API da `Openweathermap`
- [ ] Refatoração do código para uma melhor leitura
- [ ] Adição de testes automatizados
- [ ] Fazer deploy na vercel e implmentação de CI/CD
- [ ] Adição de pre-commit?
- [ ] Adição de nova feature: `Limpar todas as Cidades`
- [ ] Adição de nova feature: `Exportar Cidades`
- [ ] Adição de nova feature: `Importar Cidades`

## 📦 Package manager

Foi utilizado `poetry` como gerenciador de pacotes. Você pode instalar `poetry` seguindo as instruções [aqui](https://python-poetry.org/docs/#installation).

Favor **Não** utilizar `pip` ou `conda` para instalar as dependencias. Para isso, utilize o seguinte comando:

```bash
poetry install
```

## Formatação de código com `black`

Foi utilizado `black` para reformatar o código executando o seguinte comando:

```bash
black weather-app-flask-cookies 
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

Na pasta contendo o arquivo `app.py` rode o comando

    flask run
