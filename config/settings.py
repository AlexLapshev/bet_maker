import os

LINE_PROVIDER_URL = os.getenv("LINE_PROVIDER_URL", "http://0.0.0.0:8000")


class QueueSettings:
    port = os.getenv("RMQ_PORT", 5672)
    host = os.getenv("RMQ_HOST", "localhost")
    queue_name_events = os.getenv("RMQ_Q_NAME_EVENTS", "events")
    queue_name_bets = os.getenv("RMQ_Q_NAME_BETS", "bets")
    username = os.getenv("RMQ_USER", "guest")
    password = os.getenv("RMQ_PASS", "guest")


class PostgresSettings:
    POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "bet_maker_db")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
