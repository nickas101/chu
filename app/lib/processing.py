


def update_card(cards, card):
    for key in cards:
        if key in card:
            cards[key] = True
        else:
            cards[key] = False

    return cards


def join_entered_cards(card1, card2):

    entered_card1 = ", ".join(str(int(x)) for x in card1)
    entered_card2 = ", ".join(str(int(x)) for x in card2)

    if entered_card1 and entered_card2:
        entered_card = entered_card1 + ", " + entered_card2
    elif entered_card1:
        entered_card = entered_card1
    elif entered_card2:
        entered_card = entered_card2
    else:
        entered_card = ""

    return entered_card
