import os
from datetime import datetime
from pathlib import Path

from . import prepare_config_file
from . import card_config

script_file = "2- SetUpVreg.uscript"

def prepare(folder, card1, card2, frequency):

    config_file = prepare_config_file.create_config(folder)

    current_time = datetime.now()
    file_time = str(current_time)
    file_time = file_time.replace(" ", "_")
    file_time = file_time.replace(":", "-")
    file_time = file_time.split(".")

    data_folder = Path(folder)
    file_actual = data_folder / script_file
    file_old = data_folder / script_file.replace(".uscript", '_' + str(file_time[0]) + '.uscript')
    print(file_actual)
    print(file_old)

    try:
        os.rename(file_actual, file_old)
    except:
        pass

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

    with open('app/scripts/2-SetUpVreg_head.uscript', 'r') as file:
        data_head = file.read()

    with open('app/scripts/2-SetUpVreg_body.uscript', 'r') as file:
        data_body = file.read()

    with open(file_actual, 'w') as output_file:
        output_file.write(data_head)
        output_file.write(duts_number)
        output_file.write(cards_number)
        output_file.write(define_cards)
        output_file.write(frequency_string)
        output_file.write(data_body)


    success = True
    message = "OK"


    return success, message, config_file, script_file