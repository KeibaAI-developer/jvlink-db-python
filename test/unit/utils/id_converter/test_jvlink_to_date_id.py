"""jvlink_to_date_id関数の単体テスト"""

import pytest

from jvlink_db_python.exceptions import IDConversionError
from jvlink_db_python.utils.id_converter import jvlink_to_date_id


# 正常系
def test_jvlink_to_date_id_normal_conversion() -> None:
    """JV-Linkパラメータからdate_idを生成できることを確認"""
    result = jvlink_to_date_id("2025", "01", "05", "06", "01")

    assert result == "202501050601"


def test_jvlink_to_date_id_another_race() -> None:
    """別のJV-Linkパラメータでも正常に生成できることを確認"""
    result = jvlink_to_date_id("2024", "12", "25", "10", "12")

    assert result == "202412251012"


def test_jvlink_to_date_id_all_single_digit_values() -> None:
    """競馬場コードとレース番号が1桁でも正しく生成できることを確認"""
    result = jvlink_to_date_id("2025", "01", "01", "01", "01")

    assert result == "202501010101"


def test_jvlink_to_date_id_with_int_params() -> None:
    """year, month, day, race_numにint型を渡しても正しく変換されることを確認"""
    result = jvlink_to_date_id(2025, 1, 5, "06", 1)

    assert result == "202501050601"


def test_jvlink_to_date_id_with_all_int_params() -> None:
    """全ての数値パラメータにint型を渡しても正しく変換されることを確認"""
    result = jvlink_to_date_id(2024, 12, 25, "10", 12)

    assert result == "202412251012"


# 準正常系
def test_jvlink_to_date_id_year_not_4_digits() -> None:
    """yearが4桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="yearは4桁の数字文字列である必要があります"):
        jvlink_to_date_id("202", "01", "05", "06", "01")


def test_jvlink_to_date_id_year_not_numeric() -> None:
    """yearに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="yearは4桁の数字文字列である必要があります"):
        jvlink_to_date_id("202A", "01", "05", "06", "01")


def test_jvlink_to_date_id_month_not_2_digits() -> None:
    """monthが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="monthは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "1", "05", "06", "01")


def test_jvlink_to_date_id_month_not_numeric() -> None:
    """monthに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="monthは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "0A", "05", "06", "01")


def test_jvlink_to_date_id_day_not_2_digits() -> None:
    """dayが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="dayは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "01", "5", "06", "01")


def test_jvlink_to_date_id_day_not_numeric() -> None:
    """dayに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="dayは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "01", "0B", "06", "01")


def test_jvlink_to_date_id_jyo_cd_not_2_digits() -> None:
    """jyo_cdが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="jyo_cdは2桁の文字列である必要があります"):
        jvlink_to_date_id("2025", "01", "05", "6", "01")


def test_jvlink_to_date_id_jyo_cd_not_numeric() -> None:
    """jyo_cdに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="jyo_cdは数字のみで構成される必要があります"):
        jvlink_to_date_id("2025", "01", "05", "0A", "01")


def test_jvlink_to_date_id_race_num_not_2_digits() -> None:
    """race_numが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_numは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "01", "05", "06", "1")


def test_jvlink_to_date_id_race_num_not_numeric() -> None:
    """race_numに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_numは2桁の数字文字列である必要があります"):
        jvlink_to_date_id("2025", "01", "05", "06", "0B")


def test_jvlink_to_date_id_year_is_none() -> None:
    """yearがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_date_id(None, "01", "05", "06", "01")  # type: ignore


def test_jvlink_to_date_id_month_is_none() -> None:
    """monthがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_date_id("2025", None, "05", "06", "01")  # type: ignore


def test_jvlink_to_date_id_day_is_none() -> None:
    """dayがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_date_id("2025", "01", None, "06", "01")  # type: ignore


def test_jvlink_to_date_id_jyo_cd_is_none() -> None:
    """jyo_cdがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_date_id("2025", "01", "05", None, "01")  # type: ignore


def test_jvlink_to_date_id_race_num_is_none() -> None:
    """race_numがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_date_id("2025", "01", "05", "06", None)  # type: ignore
