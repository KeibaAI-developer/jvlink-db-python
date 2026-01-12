"""weather_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import weather_code_to_str


# 正常系
def test_weather_code_to_str_晴() -> None:
    """天候コード1が晴に変換されることを確認"""
    assert weather_code_to_str("1") == "晴"


def test_weather_code_to_str_曇() -> None:
    """天候コード2が曇に変換されることを確認"""
    assert weather_code_to_str("2") == "曇"


def test_weather_code_to_str_雨() -> None:
    """天候コード3が雨に変換されることを確認"""
    assert weather_code_to_str("3") == "雨"


def test_weather_code_to_str_小雨() -> None:
    """天候コード4が小雨に変換されることを確認"""
    assert weather_code_to_str("4") == "小雨"


def test_weather_code_to_str_雪() -> None:
    """天候コード5が雪に変換されることを確認"""
    assert weather_code_to_str("5") == "雪"


def test_weather_code_to_str_小雪() -> None:
    """天候コード6が小雪に変換されることを確認"""
    assert weather_code_to_str("6") == "小雪"


# 準正常系
def test_weather_code_to_str_undefined() -> None:
    """未定義の天候コードの場合に不明を返すことを確認"""
    assert weather_code_to_str("9") == "不明"
