POSTGRES_USER = 'bank-rest-api'
POSTGRES_PASSWORD = 'bank-rest-api'
POSTGRES_DB = 'bank-rest-api'
POSTGRES_HOST = 'postgres'
POSTGRES_PORT = '5432'


def get_postgres_dsn():
    return f'postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
