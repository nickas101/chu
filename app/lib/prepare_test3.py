from . import prepare_config_file
from . import file_renamer
from . import card_config

script_file = "3-Comp.uscript"

def prepare(folder, card1, card2, frequency, vregs_table, set_point):

    success = True
    message = "OK"

    config_file = prepare_config_file.create_config(folder)

    rename_success, file_actual = file_renamer.rename(folder, script_file)

    duts_number = '_define nDUTs-' + str(len(card1) + len(card2)) + ";\t\t\t\t\t\t// N number of DUTs\n"

    if len(card1) > 0 and len(card2) > 0:
        ncards = 2
    elif len(card1) > 0 or len(card2) > 0:
        ncards = 1
    else:
        ncards = 0

    cards_number = '_define nCARDs-' + str(ncards) + ";\t\t\t\t\t\t// N number of Cards\n"

    frequency_string = '_define nominalFreq-' + str(frequency) + ";\t\t\t\t\t\t// Device Frequency\n"

    define_cards = ""

    if len(card1) > 0:
        define_cards = define_cards + '_define TableForCrd-0 [' + str(len(card1)) + ']'
        define_cards = define_cards + " " + " ".join(str(int(x)) for x in card1)
        define_cards = define_cards + ";\t\t\t\t\t\t// Card-0 Using these Duts\n"

    if len(card2) > 0:
        define_cards = define_cards + '_define TableForCrd-1 [' + str(len(card2)) + ']'
        define_cards = define_cards + " " + " ".join(str(int(x)) for x in card2)
        define_cards = define_cards + ";\t\t\t\t\t\t// Card-1 Using these Duts\n"

    define_cards = define_cards + "// Note:- numbers are card position numbers starting at 1 (not 0)\n"

    text_1 = "\n\n// Tables from PreComp.uScript solve go here\n"

    table_0 = vregs_table['Table-0'].to_list()
    table_1 = vregs_table['Table-1'].to_list()

    define_tables = ""

    if len(table_0) > 0:
        define_tables = define_tables + '_define Table-0 [' + str(len(table_0)) + ']'
        define_tables = define_tables + " " + " ".join(str(int(x)) for x in table_0)
        define_tables = define_tables + ";\t\t\t\t\t\t// VReg_Trim from 2-SetUpVreg\n"

    if len(table_1) > 0:
        define_tables = define_tables + '_define Table-1 [' + str(len(table_1)) + ']'
        define_tables = define_tables + " " + " ".join(str(int(x)) for x in table_1)
        define_tables = define_tables + ";\t\t\t\t\t\t// TcVReg_Trim from 2-SetUpVreg\n"


    if "Pluto+" in set_point:
        set_point_string = "_define Table-2 [5] 50 41 32 23 15;\t\t\t\t\t\t// SetPt_N for Pluto+\n"
    elif "AKM2156" in set_point:
        set_point_string = "_define Table-2 [5] 48 35 25 16 7;\t\t\t\t\t\t// SetPt_N for AKM2156\n"
    else:
        set_point_string = ""


    with open('app/scripts/3-Comp_head.uscript', 'r') as file:
        data_head = file.read()

    with open('app/scripts/3-Comp_body.uscript', 'r') as file:
        data_body = file.read()

    with open(file_actual, 'w') as output_file:
        output_file.write(data_head)
        output_file.write(duts_number)
        output_file.write(cards_number)
        output_file.write(define_cards)
        output_file.write(frequency_string)
        output_file.write(text_1)
        output_file.write(define_tables)
        output_file.write(set_point_string)
        output_file.write(data_body)



    return success, message, config_file, script_file