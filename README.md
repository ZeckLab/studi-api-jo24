# API Jeux Olympiques 2024 - Studi
Projet effectué dans le cadre de la validation du Bloc - développement d'une solution digitale avec Python.
Utilisation de FastAPI, SQLAchemy, PyTest, python-jose (JWT)
Utilisation de VisualStudiCode
Connexion avec une base de données PostgreQSL

## Pré-requis
[Python 3.12 or eather](https://www.python.org/downloads/)

## Installation

- Create a virtual environnement and activate it
- git clone this project
- install dependencies with this command in root folder of the project :

```python pip3 install -r ./requirements.txt ```

- create env file named '.env' in the root of the project to configure your database and your secrets :
    * DATABASE_URL
    * ALGORITHM = Algorithm used to encode the JWToken
    * SECREY_KEY = your secret key to encode the JWToken
    - ADMIN_EMAIL = user admin created when the server is launched
    - ADMIN_PASSWORD = in clear to be hashed in the database

- launch app with :
```python -m uvicorn main:app --reload```

- go to http://127.0.0.1:8000
- go to https://studi-api-jo24.azurewebsites.net/docs to see the api docs
- go to https://studi-api-jo24.azurewebsites.net/api/events to see the events via the endpoint
