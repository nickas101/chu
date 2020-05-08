import pytest
import pandas as pd

from app.lib import solver_wrapper


@pytest.mark.parametrize('result', [True])
def test_solver_wrapper_success(dataframe_for_solver, result):
    success_solver, message_solver, solver_output, bad_units = solver_wrapper.wrap(dataframe_for_solver)

    assert success_solver == result


@pytest.mark.parametrize('result', [''])
def test_solver_wrapper_text(dataframe_for_solver, result):
    success_solver, message_solver, solver_output, bad_units = solver_wrapper.wrap(dataframe_for_solver)

    assert message_solver == result


@pytest.mark.parametrize('result', [False])
def test_solver_wrapper_failure(result):
    dataframe_for_solver = pd.DataFrame()

    success_solver, message_solver, solver_output, bad_units = solver_wrapper.wrap(dataframe_for_solver)

    assert success_solver == result


@pytest.mark.parametrize('result', [' *** Problem with solver calculations'])
def test_solver_wrapper_text_failure(result):
    dataframe_for_solver = pd.DataFrame()

    success_solver, message_solver, solver_output, bad_units = solver_wrapper.wrap(dataframe_for_solver)

    assert message_solver == result
