import pytest
import pandas as pd

from app import app


@pytest.fixture(scope='session')
def client():
    app.config['SERVER_NAME'] = "chu.com"

    ctx = app.app_context()
    ctx.push()

    with app.test_client() as client:
        yield client

    ctx.pop()


@pytest.fixture(scope='session')
def dataframe_for_solver():
    df = pd.read_pickle('app/scripts/result_cutted_for_solver_testing.pkl')

    return df

