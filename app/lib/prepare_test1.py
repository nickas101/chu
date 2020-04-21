from . import prepare_config_file
from . import file_renamer
from . import card_config

script_file = "1-OvenLoad.uscript"

def prepare(folder, card1, card2, frequency):

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

    define_cards = define_cards + card_config.create_card(card1, 0)
    define_cards = define_cards + card_config.create_card(card2, 1)

    define_cards = define_cards + "// Note:- numbers are card position numbers starting at 1 (not 0)\n"

    with open('app/scripts/1-OvenLoad_head.uscript', 'r') as file:
        data_head = file.read()

    with open('app/scripts/1-OvenLoad_body.uscript', 'r') as file:
        data_body = file.read()

    with open(file_actual, 'w') as output_file:
        output_file.write(data_head)
        output_file.write(duts_number)
        output_file.write(cards_number)
        output_file.write(define_cards)
        output_file.write(frequency_string)
        output_file.write(data_body)



    return success, message, config_file, script_file