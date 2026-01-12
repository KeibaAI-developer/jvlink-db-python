"""baba_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import baba_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("1", "良"),
        ("2", "稍"),
        ("3", "重"),
        ("4", "不"),
    ],
)
def test_baba_code_to_str_normal(code: str, expected: str) -> None:
    """馬場状態コードが正しく変換されることを確認"""
    assert baba_code_to_str(code) == expected


# 準正常系
def test_baba_code_to_str_undefined() -> None:
    """未定義の馬場状態コードの場合に不明を返すことを確認"""
    assert baba_code_to_str("9") == "不明"
