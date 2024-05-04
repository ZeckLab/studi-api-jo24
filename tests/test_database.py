from sqlalchemy import text

from src.core.config.database import engine

def test_database_connection():
    with engine.connect() as connection:
        result = connection.execute(text("select 'hello world'"))
        assert result.all() == [('hello world',)]