"""track_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import track_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("10", "芝・直線"),
        ("11", "芝・左回り"),
        ("12", "芝・左外回り"),
        ("13", "芝・左内-外回り"),
        ("14", "芝・左外-内回り"),
        ("15", "芝・左回り内2周"),
        ("16", "芝・左回り外2周"),
        ("17", "芝・右回り"),
        ("18", "芝・右外回り"),
        ("19", "芝・右内-外回り"),
        ("20", "芝・右外-内回り"),
        ("21", "芝・右回り内2周"),
        ("22", "芝・右回り外2周"),
        ("23", "ダート・左回り"),
        ("24", "ダート・右回り"),
        ("25", "ダート・左内回り"),
        ("26", "ダート・右外回り"),
        ("27", "サンド・左回り"),
        ("28", "サンド・右回り"),
        ("29", "ダート・直線"),
        ("51", "障害・芝・欅"),
        ("52", "障害・芝・ダート"),
        ("53", "障害・芝・左回り"),
        ("54", "障害・芝"),
        ("55", "障害・芝・外回り"),
        ("56", "障害・芝・外-内回り"),
        ("57", "障害・芝・内-外回り"),
        ("58", "障害・芝・内2周以上"),
        ("59", "障害・芝・外2周以上"),
    ],
)
def test_track_code_to_str_normal(code: str, expected: str) -> None:
    """トラックコードが正しく変換されることを確認"""
    assert track_code_to_str(code) == expected


# 準正常系
def test_track_code_to_str_undefined_code() -> None:
    """未定義のトラックコードの場合に不明を返すことを確認"""
    assert track_code_to_str("99") == "不明"


def test_track_code_to_str_empty_string() -> None:
    """空文字列の場合に不明を返すことを確認"""
    assert track_code_to_str("") == "不明"


def test_track_code_to_str_invalid_format() -> None:
    """不正なフォーマットの場合に不明を返すことを確認"""
    assert track_code_to_str("XX") == "不明"
