import pytest
from pandas.testing import assert_frame_equal
import pandas as pd

from app.lib import read_results_test1
from app.lib import read_results_test2
from app.lib import read_results_test3
from app.lib import read_results_test4


@pytest.mark.parametrize('folder, result', [("c:\\Temp", False)])
def test_read_results_test1_success(folder, result):
    success, text, results_file, time, df = read_results_test1.read(folder)

    assert success is result


@pytest.mark.parametrize('folder, result', [("c:\\Temp", ' *** Input file not found!')])
def test_read_results_test1_text(folder, result):
    success, text, results_file, time, df = read_results_test1.read(folder)

    assert text == result


@pytest.mark.parametrize('folder, result', [("c:\\Temp", '1-OvenLoad.txt')])
def test_read_results_test1_file(folder, result):
    success, text, results_file, time, df = read_results_test1.read(folder)

    assert results_file == result


@pytest.mark.parametrize('folder', [("c:\\Temp")])
def test_read_results_test1_dataframe(folder):
    df_empty = pd.DataFrame()
    success, text, results_file, time, df = read_results_test1.read(folder)

    assert_frame_equal(df, df_empty)


@pytest.mark.parametrize('folder, result', [("c:\\Temp", False)])
def test_read_results_test2_success(folder, result):
    success, text, results_file, freq, time, df = read_results_test2.read(folder)

    assert success is result


@pytest.mark.parametrize('folder, result', [("c:\\Temp", ' *** Input file not found!')])
def test_read_results_test2_text(folder, result):
    success, text, results_file, freq, time, df = read_results_test2.read(folder)

    assert text == result


@pytest.mark.parametrize('folder, result', [("c:\\Temp", '2 -SetUpVreg.txt')])
def test_read_results_test2_file(folder, result):
    success, text, results_file, freq, time, df = read_results_test2.read(folder)

    assert results_file == result


@pytest.mark.parametrize('folder, result', [("c:\\Temp", '')])
def test_read_results_test2_freq(folder, result):
    success, text, results_file, freq, time, df = read_results_test2.read(folder)

    assert freq == result


@pytest.mark.parametrize('folder', [("c:\\Temp")])
def test_read_results_test2_dataframe(folder):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, df = read_results_test2.read(folder)

    assert_frame_equal(df, df_empty)


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, False)])
def test_read_results_test3_success(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert success is result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, ' *** Input file not found!(3-Comp.txt)  ')])
def test_read_results_test3_text(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert text == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '3-Comp.txt')])
def test_read_results_test3_file(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert results_file == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '')])
def test_read_results_test3_freq(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert freq == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '')])
def test_read_results_test3_bad_units(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert bad_units == result


@pytest.mark.parametrize('folder, limit', [("c:\\Temp", 1)])
def test_read_results_test3_result_full(folder, limit):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert_frame_equal(result_full, df_empty)


@pytest.mark.parametrize('folder, limit', [("c:\\Temp", 1)])
def test_read_results_test3_result_cutted(folder, limit):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert_frame_equal(result_cutted, df_empty)


@pytest.mark.parametrize('folder, limit', [("c:\\Temp", 1)])
def test_read_results_test3_vreg_table(folder, limit):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, bad_units, result_full, result_cutted, vreg_table = read_results_test3.read(folder, limit)

    assert_frame_equal(vreg_table, df_empty)


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, False)])
def test_read_results_test4_success(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert success is result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, ' *** Input file not found!(4-Soft Vfy with comp numbers.txt)  ')])
def test_read_results_test4_text(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert text == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '4-Soft Vfy with comp numbers.txt')])
def test_read_results_test4_file(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert results_file == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '')])
def test_read_results_test4_freq(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert freq == result


@pytest.mark.parametrize('folder, limit, result', [("c:\\Temp", 1, '')])
def test_read_results_test4_bad_units(folder, limit, result):
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert bad_units == result


@pytest.mark.parametrize('folder, limit', [("c:\\Temp", 1)])
def test_read_results_test4_result_fvt(folder, limit):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert_frame_equal(result_fvt, df_empty)


@pytest.mark.parametrize('folder, limit', [("c:\\Temp", 1)])
def test_read_results_test4_result_calculated(folder, limit):
    df_empty = pd.DataFrame()
    success, text, results_file, freq, time, bad_units, result_fvt, result_calculated = read_results_test4.read(folder, limit)

    assert_frame_equal(result_calculated, df_empty)
