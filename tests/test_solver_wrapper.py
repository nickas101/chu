import pytest
import pandas as pd

from app.lib import solver_wrapper


@pytest.mark.parametrize('cut_number, result', [(7, True)])
def test_solver_wrapper_success(dataframe_for_solver, cut_number, result):
    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert success == result


@pytest.mark.parametrize('cut_number, result', [(7, False)])
def test_solver_wrapper_failure(cut_number, result):
    dataframe_for_solver = pd.DataFrame()

    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert success == result


@pytest.mark.parametrize('cut_number, result', [(7, '')])
def test_solver_wrapper_text_success(dataframe_for_solver, cut_number, result):
    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert message == result


@pytest.mark.parametrize('cut_number, table, result', [(7,
                                                        {0: ['0', 1, 0, 0, 0, 0, 0]},
                                                        ' *** Problem with solver calculations')])
def test_solver_wrapper_text_failure(cut_number, table, result):
    dataframe_for_solver = pd.DataFrame.from_dict(table, orient='index')
    dataframe_for_solver.columns = ['DUT', 'pos', 'residual', 'Temp', 'CoeffB', 'CoeffC', 'ppm']

    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert message == result


@pytest.mark.parametrize('cut_number, result', [(7, ' *** Problem with an input table for a solver *** Problem with solver calculations')])
def test_solver_wrapper_text_double_failure(cut_number, result):
    dataframe_for_solver = pd.DataFrame()

    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert message == result


@pytest.mark.parametrize('cut_number, result', [(7, '')])
def test_solver_wrapper_bad_units(dataframe_for_solver, cut_number, result):
    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert bad_units == result


@pytest.mark.parametrize('cut_number, result', [(7, [])])
def test_solver_wrapper_bad_units_list(dataframe_for_solver, cut_number, result):
    success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list = solver_wrapper.wrap(dataframe_for_solver, cut_number)

    assert bad_units_list == result
