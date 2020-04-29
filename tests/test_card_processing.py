import pytest

from app.lib import card_processing


@pytest.mark.parametrize('cards, card, result',
                         [({1: False, 2: False, 3: True, 4: True, 5: False, 6: True},
                          [1, 3, 5],
                          {1: True, 2: False, 3: True, 4: False, 5: True, 6: False})])
def test_update_card(cards, card, result):
    assert card_processing.update_card(cards, card) == result


@pytest.mark.parametrize('card1, card2, result',
                        [([1, 3, 5, 6, 7],
                        [11, 13, 15],
                        '1, 3, 5, 6, 7, 11, 13, 15')])
def test_join_entered_cards(card1, card2, result):
    assert card_processing.join_entered_cards(card1, card2) == result
