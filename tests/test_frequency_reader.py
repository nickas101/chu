import pytest

from app.lib import frequency_reader


@pytest.mark.parametrize('line, input_string, result', [("\t_define nominalFreq-30.720;",
                                                         '_define nominalFreq-',
                                                         '30.72')])
def test_frequency_reader(line, input_string, result):
    assert frequency_reader.read_frequency(line, input_string) == result
