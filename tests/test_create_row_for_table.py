import pytest

from app.lib import prepare_test4


@pytest.mark.parametrize('input_table, table_name, result',
                         [([54, 87, 39, 53, 24, 26, 48, 41, 57],
                            'Table-10',
                            "_define Table-10 [9] 54 87 39 53 24 26 48 41 57;						// CoeffC2\n")])
def test_create_row_for_table(input_table, table_name, result):
    assert prepare_test4.create_row_for_table(input_table, table_name) == result, 'Create string for a test card'
