"""race_id_to_jvlink関数の単体テスト"""

import pytest

from jvlink_db_python.exceptions import IDConversionError
from jvlink_db_python.utils.id_converter import race_id_to_jvlink


# 正常系
def test_race_id_to_jvlink_normal_conversion() -> None:
    """正常なrace_idとdate_idからJV-Linkパラメータに変換できることを確認"""
    result = race_id_to_jvlink("202506010101", "202501050601")

    assert result == {
        "idYear": "2025",
        "idMonthDay": "0105",
        "idJyoCD": "06",
        "idKaiji": "01",
        "idNichiji": "01",
        "idRaceNum": "01",
    }


def test_race_id_to_jvlink_another_race() -> None:
    """別のrace_idとdate_idでも正常に変換できることを確認"""
    result = race_id_to_jvlink("202410051012", "202412251012")

    assert result == {
        "idYear": "2024",
        "idMonthDay": "1225",
        "idJyoCD": "10",
        "idKaiji": "05",
        "idNichiji": "10",
        "idRaceNum": "12",
    }


def test_race_id_to_jvlink_single_digit_values_with_zero_padding() -> None:
    """競馬場コード、回、日目、レース番号が1桁でもゼロ埋めで正しく扱えることを確認"""
    result = race_id_to_jvlink("202501010101", "202501010101")

    assert result == {
        "idYear": "2025",
        "idMonthDay": "0101",
        "idJyoCD": "01",
        "idKaiji": "01",
        "idNichiji": "01",
        "idRaceNum": "01",
    }


# 準正常系
def test_race_id_to_jvlink_race_id_not_12_digits() -> None:
    """race_idが12桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_idは12桁の文字列である必要があります"):
        race_id_to_jvlink("20250601010", "202501050601")


def test_race_id_to_jvlink_race_id_not_numeric() -> None:
    """race_idに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_idは数字のみで構成される必要があります"):
        race_id_to_jvlink("2025060101AB", "202501050601")


def test_race_id_to_jvlink_date_id_not_12_digits() -> None:
    """date_idが12桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="date_idは12桁の文字列である必要があります"):
        race_id_to_jvlink("202506010101", "20250105060")


def test_race_id_to_jvlink_date_id_not_numeric() -> None:
    """date_idに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="date_idは数字のみで構成される必要があります"):
        race_id_to_jvlink("202506010101", "2025010506XY")


def test_race_id_to_jvlink_year_mismatch() -> None:
    """race_idとdate_idの年が一致しない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_idとdate_idの年が一致しません"):
        race_id_to_jvlink("202506010101", "202401050601")


def test_race_id_to_jvlink_jyo_cd_mismatch() -> None:
    """race_idとdate_idの競馬場コードが一致しない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_idとdate_idの競馬場コードが一致しません"):
        race_id_to_jvlink("202506010101", "202501050501")


def test_race_id_to_jvlink_race_num_mismatch() -> None:
    """race_idとdate_idのレース番号が一致しない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_idとdate_idのレース番号が一致しません"):
        race_id_to_jvlink("202506010101", "202501050602")


def test_race_id_to_jvlink_race_id_is_none() -> None:
    """race_idがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        race_id_to_jvlink(None, "202501050601")  # type: ignore


def test_race_id_to_jvlink_date_id_is_none() -> None:
    """date_idがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        race_id_to_jvlink("202506010101", None)  # type: ignore
