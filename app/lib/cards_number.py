

def count(card1, card2):

    if len(card1) > 0 and len(card2) > 0:
        ncards = 2
    elif len(card1) > 0 or len(card2) > 0:
        ncards = 1
    else:
        ncards = 0

    return ncards
