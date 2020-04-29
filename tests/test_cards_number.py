import pytest

from app.lib import cards_number


@pytest.mark.parametrize('card1, card2, result',
                        [([1, 2, 3], [1, 2, 3, 4, 5], 2),
                        ([], [1, 2, 3, 4, 5], 1),
                        ([1, 2, 3], [], 1),
                        ([], [], 0)])
def test_cards_number(card1, card2, result):
    assert cards_number.count(card1, card2) == result
