import pandas as pd

from . import prepare_config_file
from . import solver_table_converter
from . import file_renamer
from . import card_config
from . import cards_number


coefficients_names = {'Table-0': 'VReg_Trim from 2-SetUpVreg',
                        'Table-1': 'TcVReg_Trim from 2-SetUpVreg',
                        'Table-2': 'CoeffA0',
                        'Table-3': 'CoeffB0',
                        'Table-4': 'CoeffC0',
                        'Table-5': 'CoeffA1',
                        'Table-6': 'CoeffB1',
                        'Table-7': 'CoeffC1',
                        'Table-8': 'CoeffA2',
                        'Table-9': 'CoeffB2',
                        'Table-10': 'CoeffC2',
                        'Table-11': 'CoeffA3',
                        'Table-12': 'CoeffB3',
                        'Table-13': 'CoeffC3',
                        'Table-14': 'CoeffA4',
                        'Table-15': 'CoeffB4',
                        'Table-16': 'CoeffC4',
                        'Table-17': 'CoeffA5',
                        'Table-18': 'CoeffB5',
                        'Table-19': 'CoeffC5',
                        'Table-20': 'CoeffA6',
                        'Table-21': 'CoeffB6',
                        'Table-22': 'CoeffC6',
                        'Table-23': 'CoeffB7',
                        'Table-24': 'CoeffC7',
                        'Table-25': 'CoeffA7',
                        'Table-26': 'CoeffD',
                        'Table-27': 'CoeffE'
                      }

script_file = "4-Soft Vfy with comp numbers.uscript"


def prepare(folder, card1, card2, frequency, solver_table, vreg_table_from_test3, temp_range):

    success = True
    message = "OK"
    solver_table_converted = pd.DataFrame()

    config_file = prepare_config_file.create_config(folder)

    rename_success, file_actual = file_renamer.rename(folder, script_file)

    try:
        solver_table_converted = solver_table_converter.convert(solver_table)
    except:
        success = False
        message = " *** Problem with converting Solver Table!"

    duts_number = '_define nDUTs-' + str(len(card1) + len(card2)) + ";\t\t\t\t\t\t// N number of DUTs\n"
    cards_number_str = '_define nCARDs-' + str(cards_number.count(card1, card2)) + ";\t\t\t\t\t\t// N number of Cards\n"
    frequency_string = '_define nominalFreq-' + str(frequency) + ";\t\t\t\t\t\t// Device Frequency\n"

    define_cards = ""

    define_cards = define_cards + card_config.create_card(card1, 0)
    define_cards = define_cards + card_config.create_card(card2, 1)

    define_cards = define_cards + "// Note:- numbers are card position numbers starting at 1 (not 0)\n"

    text_1 = "\n\n// Any Tables from previous Scripts go here\n"

    card1_int = list(map(int, card1))
    card2_int = list(map(int, card2))
    card_int = card1_int + card2_int

    vreg_table_cutted = vreg_table_from_test3[vreg_table_from_test3['pos'].isin(card_int)]

    table_0 = vreg_table_cutted['Table-0'].to_list()
    table_1 = vreg_table_cutted['Table-1'].to_list()

    define_tables = ""

    define_tables = define_tables + str(create_row_for_table(table_0, 'Table-0'))
    define_tables = define_tables + str(create_row_for_table(table_1, 'Table-1'))

    solver_table_converted_cutted = solver_table_converted[solver_table_converted['pos'].isin(card_int)]

    define_tables = define_tables + "\n"

    for column in solver_table_converted_cutted.columns:
        if column != 'DUT' and column != 'pos':
            table = solver_table_converted_cutted[column].to_list()
            define_tables = define_tables + str(create_row_for_table(table, column))

    temp_range_splitted = temp_range.split(" ")
    temp_range_comment = '// ' + temp_range_splitted[0] + "'C to " + temp_range_splitted[1] + " step -" + temp_range_splitted[2]
    temperature_range_string = "\n\n// Any Tables for what we are testing go here\n_define chamberTempRange-0 " + str(temp_range) + ";\t\t\t\t\t\t" + str(temp_range_comment) + "\n"


    with open('app/scripts/4-Soft Vfy with comp numbers_head.uscript', 'r') as file:
        data_head = file.read()

    with open('app/scripts/4-Soft Vfy with comp numbers_body.uscript', 'r') as file:
        data_body = file.read()

    with open(file_actual, 'w') as output_file:
        output_file.write(data_head)
        output_file.write(duts_number)
        output_file.write(cards_number_str)
        output_file.write(define_cards)
        output_file.write(frequency_string)
        output_file.write(text_1)
        output_file.write(define_tables)
        output_file.write(temperature_range_string)
        output_file.write(data_body)

    return success, message, config_file, script_file


def create_row_for_table(input_table, table_name):
    row = ''

    try:
        comment = coefficients_names[table_name]
    except:
        comment = ''

    if len(input_table) > 0:
        row = row + '_define ' + str(table_name) + ' [' + str(len(input_table)) + ']'
        row = row + " " + " ".join(str(int(x)) for x in input_table)
        row = row + ";\t\t\t\t\t\t// " + comment + "\n"

    return row
