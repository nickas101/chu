import pytest
from app import app


@pytest.fixture(scope='session')
def client():
    app.config['SERVER_NAME'] = "chu.com"

    ctx = app.app_context()
    ctx.push()

    with app.test_client() as client:
        yield client

    ctx.pop()