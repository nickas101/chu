import pytest

from app.lib import card_config


@pytest.mark.parametrize('card, card_number, result',
                         [([1, 2, 3, 4], 0,
                        "_define TableForCrd-0 [4] 1 2 3 4;						// Card-0 Using these Duts\n")])
def test_card_config(card, card_number, result):
    assert card_config.create_card(card, card_number) == result, 'Create string for a test card'
