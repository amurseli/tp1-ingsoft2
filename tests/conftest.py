import os
os.environ["DATABASE_HOST"] = "db-test"

import app.database
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
app.database.engine = create_async_engine(app.database.DATABASE_URL, poolclass=NullPool)
app.database.AsyncSessionLocal = async_sessionmaker(bind=app.database.engine, expire_on_commit=False, autoflush=False)

import pytest
import psycopg2
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        conn = psycopg2.connect(
            host="db-test",
            port=5432,
            dbname=os.getenv("DATABASE_NAME", "db"),
            user=os.getenv("DATABASE_USER", "admin"),
            password=os.getenv("DATABASE_PASSWORD", "password"),
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute("DELETE FROM cart_items")
        cur.execute("DELETE FROM products")
        cur.close()
        conn.close()
        yield c