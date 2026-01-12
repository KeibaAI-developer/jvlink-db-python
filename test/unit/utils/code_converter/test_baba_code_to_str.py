"""baba_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import baba_code_to_str


# 正常系
def test_baba_code_to_str_良() -> None:
    """馬場状態コード1が良に変換されることを確認"""
    assert baba_code_to_str("1") == "良"


def test_baba_code_to_str_稍() -> None:
    """馬場状態コード2が稍に変換されることを確認"""
    assert baba_code_to_str("2") == "稍"


def test_baba_code_to_str_重() -> None:
    """馬場状態コード3が重に変換されることを確認"""
    assert baba_code_to_str("3") == "重"


def test_baba_code_to_str_不() -> None:
    """馬場状態コード4が不に変換されることを確認"""
    assert baba_code_to_str("4") == "不"


# 準正常系
def test_baba_code_to_str_undefined() -> None:
    """未定義の馬場状態コードの場合に不明を返すことを確認"""
    assert baba_code_to_str("9") == "不明"
