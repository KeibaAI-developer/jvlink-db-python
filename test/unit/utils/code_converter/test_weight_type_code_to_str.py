"""weight_type_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import weight_type_code_to_str


# 正常系
def test_weight_type_code_to_str_ハンデ() -> None:
    """重量種別コード1がハンデに変換されることを確認"""
    assert weight_type_code_to_str("1") == "ハンデ"


def test_weight_type_code_to_str_別定() -> None:
    """重量種別コード2が別定に変換されることを確認"""
    assert weight_type_code_to_str("2") == "別定"


def test_weight_type_code_to_str_馬齢() -> None:
    """重量種別コード3が馬齢に変換されることを確認"""
    assert weight_type_code_to_str("3") == "馬齢"


def test_weight_type_code_to_str_定量() -> None:
    """重量種別コード4が定量に変換されることを確認"""
    assert weight_type_code_to_str("4") == "定量"


# 準正常系
def test_weight_type_code_to_str_undefined() -> None:
    """未定義の重量種別コードの場合に不明を返すことを確認"""
    assert weight_type_code_to_str("9") == "不明"
