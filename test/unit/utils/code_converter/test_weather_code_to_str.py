"""weather_code_to_str関数の単体テスト"""

import pytest

from jvlink_db_python.utils.code_converter import weather_code_to_str


# 正常系
@pytest.mark.parametrize(
    ("code", "expected"),
    [
        ("1", "晴"),
        ("2", "曇"),
        ("3", "雨"),
        ("4", "小雨"),
        ("5", "雪"),
        ("6", "小雪"),
    ],
)
def test_weather_code_to_str_normal(code: str, expected: str) -> None:
    """天候コードが正しく変換されることを確認"""
    assert weather_code_to_str(code) == expected


# 準正常系
def test_weather_code_to_str_undefined() -> None:
    """未定義の天候コードの場合に不明を返すことを確認"""
    assert weather_code_to_str("9") == "不明"
