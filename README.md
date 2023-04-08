## Installation

Create virtual environment

`python3.10 -m virtualenv venv`

Activate it

`source venv/bin/activate`

Install required packages

`pip install -r requirements.txt`

Run a database and rabbitmq from a docker-compose file

```
docker-compose up -d 
```

Apply migrations 

```
alembic upgrade head
```

To fill the database with dummy data use 

```
python -m etc.fill_db_random
```

To send 10000 dummy requests

```
python -m etc.requests_test
```

if you need to reset the database use

```
docker-compose down && docker-compose up -d && sleep 1 && alembic upgrade head
```

To run the app 

`python app.py`

## To run the app from docker compose

Run docker compose

```
docker-compose --profile with_api up
```

## Tests

`pytest tests`
