"""jyo_code_to_name関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import jyo_code_to_name


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("01", "札幌"),
        ("02", "函館"),
        ("03", "福島"),
        ("04", "新潟"),
        ("05", "東京"),
        ("06", "中山"),
        ("07", "中京"),
        ("08", "京都"),
        ("09", "阪神"),
        ("10", "小倉"),
    ],
)
def test_jyo_code_to_name_central(code: str, expected: str) -> None:
    """中央競馬場コードが正しく変換されることを確認"""
    assert jyo_code_to_name(code) == expected


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("30", "門別"),
        ("31", "北見"),
        ("32", "岩見沢"),
        ("33", "帯広"),
        ("34", "旭川"),
        ("35", "盛岡"),
        ("36", "水沢"),
        ("37", "上山"),
        ("38", "三条"),
        ("39", "足利"),
        ("40", "宇都宮"),
        ("41", "高崎"),
        ("42", "浦和"),
        ("43", "船橋"),
        ("44", "大井"),
        ("45", "川崎"),
        ("46", "金沢"),
        ("47", "笠松"),
        ("48", "名古屋"),
        ("49", "紀三井寺"),
        ("50", "園田"),
        ("51", "姫路"),
        ("52", "益田"),
        ("53", "福山"),
        ("54", "高知"),
        ("55", "佐賀"),
        ("56", "荒尾"),
        ("57", "中津"),
        ("58", "札幌(地方)"),
        ("59", "函館(地方)"),
        ("60", "新潟(地方)"),
        ("61", "中京(地方)"),
    ],
)
def test_jyo_code_to_name_local(code: str, expected: str) -> None:
    """地方競馬場コードが正しく変換されることを確認"""
    assert jyo_code_to_name(code) == expected


@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("K0", "パキスタン"),
        ("C0", "イタリア"),
    ],
)
def test_jyo_code_to_name_foreign(code: str, expected: str) -> None:
    """海外競馬場コードが正しく変換されることを確認"""
    assert jyo_code_to_name(code) == expected


# 準正常系
def test_jyo_code_to_name_undefined_code() -> None:
    """未定義の競馬場コードの場合に不明を返すことを確認"""
    assert jyo_code_to_name("99") == "不明"


def test_jyo_code_to_name_empty_string() -> None:
    """空文字列の場合に不明を返すことを確認"""
    assert jyo_code_to_name("") == "不明"


def test_jyo_code_to_name_invalid_format() -> None:
    """不正なフォーマットの場合に不明を返すことを確認"""
    assert jyo_code_to_name("ABC") == "不明"
