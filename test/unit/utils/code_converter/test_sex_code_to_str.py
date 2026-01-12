"""sex_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import sex_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("1", "牡"),
        ("2", "牝"),
        ("3", "セ"),
    ],
)
def test_sex_code_to_str_normal(code: str, expected: str) -> None:
    """性別コードが正しく変換されることを確認"""
    assert sex_code_to_str(code) == expected


# 準正常系
def test_sex_code_to_str_undefined_code() -> None:
    """未定義の性別コードの場合に不明を返すことを確認"""
    assert sex_code_to_str("4") == "不明"


def test_sex_code_to_str_empty_string() -> None:
    """空文字列の場合に不明を返すことを確認"""
    assert sex_code_to_str("") == "不明"


def test_sex_code_to_str_invalid_format() -> None:
    """不正なフォーマットの場合に不明を返すことを確認"""
    assert sex_code_to_str("X") == "不明"
