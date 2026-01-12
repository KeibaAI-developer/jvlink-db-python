"""date_id_to_race_id関数の単体テスト"""

import pytest

from jvlink_db_python.exceptions import IDConversionError
from jvlink_db_python.utils.id_converter import date_id_to_race_id


# 正常系
def test_date_id_to_race_id_normal_conversion() -> None:
    """正常なdate_idと開催情報からrace_idを生成できることを確認"""
    result = date_id_to_race_id("202501050601", "01", "01")

    assert result == "202506010101"


def test_date_id_to_race_id_another_race() -> None:
    """別のdate_idと開催情報でも正常に生成できることを確認"""
    result = date_id_to_race_id("202412251012", "05", "10")

    assert result == "202410051012"


def test_date_id_to_race_id_all_single_digit_values() -> None:
    """競馬場コード、回、日目、レース番号が全て1桁でも正しく生成できることを確認"""
    result = date_id_to_race_id("202501010101", "01", "01")

    assert result == "202501010101"


def test_date_id_to_race_id_with_int_params() -> None:
    """kaijiとnichijiにint型を渡しても正しく変換されることを確認"""
    result = date_id_to_race_id("202501050601", 1, 1)

    assert result == "202506010101"


def test_date_id_to_race_id_with_mixed_types() -> None:
    """str型とint型を混在させても正しく変換されることを確認"""
    result = date_id_to_race_id("202412251012", "05", 10)

    assert result == "202410051012"


# 準正常系
def test_date_id_to_race_id_date_id_not_12_digits() -> None:
    """date_idが12桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="date_idは12桁の文字列である必要があります"):
        date_id_to_race_id("20250105060", "01", "01")


def test_date_id_to_race_id_date_id_not_numeric() -> None:
    """date_idに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="date_idは数字のみで構成される必要があります"):
        date_id_to_race_id("2025010506AB", "01", "01")


def test_date_id_to_race_id_kaiji_not_2_digits() -> None:
    """kaijiが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="kaijiは2桁の数字文字列である必要があります"):
        date_id_to_race_id("202501050601", "1", "01")


def test_date_id_to_race_id_kaiji_not_numeric() -> None:
    """kaijiに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="kaijiは2桁の数字文字列である必要があります"):
        date_id_to_race_id("202501050601", "0A", "01")


def test_date_id_to_race_id_nichiji_not_2_digits() -> None:
    """nichijiが2桁でない場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="nichijiは2桁の数字文字列である必要があります"):
        date_id_to_race_id("202501050601", "01", "1")


def test_date_id_to_race_id_nichiji_not_numeric() -> None:
    """nichijiに数字以外の文字が含まれる場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError, match="nichijiは2桁の数字文字列である必要があります"):
        date_id_to_race_id("202501050601", "01", "0B")


def test_date_id_to_race_id_date_id_is_none() -> None:
    """date_idがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        date_id_to_race_id(None, "01", "01")  # type: ignore


def test_date_id_to_race_id_kaiji_is_none() -> None:
    """kaijiがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        date_id_to_race_id("202501050601", None, "01")  # type: ignore


def test_date_id_to_race_id_nichiji_is_none() -> None:
    """nichijiがNoneの場合にIDConversionErrorが発生することを確認"""
    with pytest.raises(IDConversionError):
        date_id_to_race_id("202501050601", "01", None)  # type: ignore
