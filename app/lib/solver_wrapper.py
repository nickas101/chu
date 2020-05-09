import pandas as pd

from . import solver_table_converter
from .kepler import comp_solver


def wrap(result_cutted, cut_number):
    success = True
    message = ''
    solver_output = pd.DataFrame()
    bad_units = ''

    try:
        solver, prediction = comp_solver.solve(result_cutted, cut_number)
        solver_output, bad_units = solver_table_converter.convert_short(solver)
    except:
        message = " *** Problem with solver calculations"
        success = False

    return success, message, solver_output, prediction, bad_units
