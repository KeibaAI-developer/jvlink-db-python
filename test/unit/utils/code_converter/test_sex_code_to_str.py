"""sex_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import sex_code_to_str


# 正常系
def test_sex_code_to_str_stallion() -> None:
    """性別コード1が牡に変換されることを確認"""
    assert sex_code_to_str("1") == "牡"


def test_sex_code_to_str_mare() -> None:
    """性別コード2が牝に変換されることを確認"""
    assert sex_code_to_str("2") == "牝"


def test_sex_code_to_str_gelding() -> None:
    """性別コード3がセに変換されることを確認"""
    assert sex_code_to_str("3") == "セ"


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
