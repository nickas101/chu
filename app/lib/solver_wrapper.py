import pandas as pd

from . import solver_table_converter
from .kepler import comp_solver


def wrap(result_cutted, cut_number):
    """Wrap solver to catch exceptions."""

    success = True
    message = ''
    solver_output = pd.DataFrame()
    solver_output_short = pd.DataFrame()
    prediction = pd.DataFrame()
    result_cutted_converted = pd.DataFrame()
    bad_units = ''
    bad_units_list = []

    result_cutted_converted['DUT'] = result_cutted['DUT']
    result_cutted_converted['pos'] = result_cutted['pos']
    result_cutted_converted['temp'] = result_cutted['Temp']
    result_cutted_converted['resppm'] = result_cutted['residual']
    result_cutted_converted['coeffB'] = result_cutted['CoeffB']
    result_cutted_converted['coeffC'] = result_cutted['CoeffC']
    result_cutted_converted['chppm'] = result_cutted['ppm'] - result_cutted['residual']

    # to serilise a dataframe
    # result_cutted.to_pickle('app/scripts/result_cutted_for_solver_testing.pkl')

    try:
        solver, prediction = comp_solver.solve(result_cutted_converted, cut_number)
        solver_output_short, solver_output, bad_units, bad_units_list = solver_table_converter.convert(solver)
        prediction.sort_values(['Temp'], ascending=[True], inplace=True)
    except:
        message = " *** Problem with solver calculations"
        success = False

    return success, message, solver_output, solver_output_short, prediction, bad_units, bad_units_list
