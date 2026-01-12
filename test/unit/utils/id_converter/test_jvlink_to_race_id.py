"""jvlink_to_race_id関数の単体テスト"""

import pytest

from jvlink_db_python.exceptions import IDConversionError
from jvlink_db_python.utils.id_converter import jvlink_to_race_id


# 正常系
def test_jvlink_to_race_id_normal_conversion() -> None:
    """JV-Linkパラメータからrace_idを生成できることを確認"""
    result = jvlink_to_race_id("2025", "06", "01", "01", "01")

    assert result == "202506010101"


def test_jvlink_to_race_id_another_race() -> None:
    """別のJV-Linkパラメータでも正常に生成できることを確認"""
    result = jvlink_to_race_id("2024", "10", "05", "10", "12")

    assert result == "202410051012"


def test_jvlink_to_race_id_all_single_digit_values() -> None:
    """競馬場コード、回、日目、レース番号が全て1桁でも正しく生成できることを確認"""
    result = jvlink_to_race_id("2025", "01", "01", "01", "01")

    assert result == "202501010101"


def test_jvlink_to_race_id_with_int_params() -> None:
    """yearやkaiji等にint型を渡しても正しく変換されることを確認"""
    result = jvlink_to_race_id(2025, "06", 1, 1, 1)

    assert result == "202506010101"


def test_jvlink_to_race_id_with_all_int_params() -> None:
    """全ての数値パラメータにint型を渡しても正しく変換されることを確認"""
    result = jvlink_to_race_id(2024, "10", 5, 10, 12)

    assert result == "202410051012"


# 準正常系
def test_jvlink_to_race_id_year_not_4_digits() -> None:
    """yearが4桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="yearは4桁の数字文字列である必要があります"):
        jvlink_to_race_id("202", "06", "01", "01", "01")


def test_jvlink_to_race_id_year_not_numeric() -> None:
    """yearに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="yearは4桁の数字文字列である必要があります"):
        jvlink_to_race_id("202A", "06", "01", "01", "01")


def test_jvlink_to_race_id_jyo_cd_not_2_digits() -> None:
    """jyo_cdが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="jyo_cdは2桁の文字列である必要があります"):
        jvlink_to_race_id("2025", "6", "01", "01", "01")


def test_jvlink_to_race_id_jyo_cd_not_numeric() -> None:
    """jyo_cdに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="jyo_cdは数字のみで構成される必要があります"):
        jvlink_to_race_id("2025", "0A", "01", "01", "01")


def test_jvlink_to_race_id_kaiji_not_2_digits() -> None:
    """kaijiが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="kaijiは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "1", "01", "01")


def test_jvlink_to_race_id_kaiji_not_numeric() -> None:
    """kaijiに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="kaijiは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "0B", "01", "01")


def test_jvlink_to_race_id_nichiji_not_2_digits() -> None:
    """nichijiが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="nichijiは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "01", "1", "01")


def test_jvlink_to_race_id_nichiji_not_numeric() -> None:
    """nichijiに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="nichijiは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "01", "0C", "01")


def test_jvlink_to_race_id_race_num_not_2_digits() -> None:
    """race_numが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_numは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "01", "01", "1")


def test_jvlink_to_race_id_race_num_not_numeric() -> None:
    """race_numに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="race_numは2桁の数字文字列である必要があります"):
        jvlink_to_race_id("2025", "06", "01", "01", "0D")


def test_jvlink_to_race_id_year_is_none() -> None:
    """yearがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_race_id(None, "06", "01", "01", "01")  # type: ignore


def test_jvlink_to_race_id_jyo_cd_is_none() -> None:
    """jyo_cdがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_race_id("2025", None, "01", "01", "01")  # type: ignore


def test_jvlink_to_race_id_kaiji_is_none() -> None:
    """kaijiがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_race_id("2025", "06", None, "01", "01")  # type: ignore


def test_jvlink_to_race_id_nichiji_is_none() -> None:
    """nichijiがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_race_id("2025", "06", "01", None, "01")  # type: ignore


def test_jvlink_to_race_id_race_num_is_none() -> None:
    """race_numがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        jvlink_to_race_id("2025", "06", "01", "01", None)  # type: ignore
