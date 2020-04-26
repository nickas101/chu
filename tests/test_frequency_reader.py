import pytest

from app.lib import frequency_reader


def test_frequency_reader():
    # assert 1==1
    assert frequency_reader.read_frequency("\t_define nominalFreq-30.720;", '_define nominalFreq-') == '30.72'