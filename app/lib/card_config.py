

def create_card(card, card_number):

    define_cards = ""

    if len(card) > 0:
        define_cards = define_cards + '_define TableForCrd-' + str(card_number) + ' [' + str(len(card)) + ']'
        define_cards = define_cards + " " + " ".join(str(int(x)) for x in card)
        define_cards = define_cards + ";\t\t\t\t\t\t// Card-" + str(card_number) + " Using these Duts\n"


    return define_cards

