"""weight_type_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import weight_type_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("1", "ハンデ"),
        ("2", "別定"),
        ("3", "馬齢"),
        ("4", "定量"),
    ],
)
def test_weight_type_code_to_str_normal(code: str, expected: str) -> None:
    """重量種別コードが正しく変換されることを確認"""
    assert weight_type_code_to_str(code) == expected


# 準正常系
def test_weight_type_code_to_str_undefined() -> None:
    """未定義の重量種別コードの場合に不明を返すことを確認"""
    assert weight_type_code_to_str("9") == "不明"
