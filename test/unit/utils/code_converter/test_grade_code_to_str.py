"""grade_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import grade_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("A", "G1"),
        ("B", "G2"),
        ("C", "G3"),
        ("D", "グレードのない重賞"),
        ("E", "重賞以外の特別競走"),
        ("F", "J･G1"),
        ("G", "J･G2"),
        ("H", "J･G3"),
        ("L", "リステッド"),
    ],
)
def test_grade_code_to_str_normal(code: str, expected: str) -> None:
    """グレードコードが正しく変換されることを確認"""
    assert grade_code_to_str(code) == expected


# 準正常系
def test_grade_code_to_str_undefined_code() -> None:
    """未定義のグレードコードの場合に不明を返すことを確認"""
    assert grade_code_to_str("X") == "不明"


def test_grade_code_to_str_empty_string() -> None:
    """空文字列の場合に不明を返すことを確認"""
    assert grade_code_to_str("") == "不明"


def test_grade_code_to_str_lowercase() -> None:
    """小文字の場合に不明を返すことを確認"""
    assert grade_code_to_str("a") == "不明"
