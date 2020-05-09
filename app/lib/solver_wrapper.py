import pandas as pd

from . import solver_table_converter
from .kepler import comp_solver


def wrap(result_cutted, cut_number):
    success = True
    message = ''
    solver_output = pd.DataFrame()
    solver_output_short = pd.DataFrame()
    prediction = pd.DataFrame()
    bad_units = ''

    try:
        solver, prediction = comp_solver.solve(result_cutted, cut_number)
        solver_output_short, solver_output, bad_units = solver_table_converter.convert(solver)
        # print(solver)
        # print(solver.info())
        # print(solver_output)
        # print(solver_output.info())
    except:
        message = " *** Problem with solver calculations"
        success = False

    return success, message, solver_output_short, prediction, bad_units
