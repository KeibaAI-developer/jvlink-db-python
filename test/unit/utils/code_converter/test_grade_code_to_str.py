"""grade_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import grade_code_to_str


# 正常系
def test_grade_code_to_str_g1() -> None:
    """グレードコードAがG1に変換されることを確認"""
    assert grade_code_to_str("A") == "G1"


def test_grade_code_to_str_g2() -> None:
    """グレードコードBがG2に変換されることを確認"""
    assert grade_code_to_str("B") == "G2"


def test_grade_code_to_str_g3() -> None:
    """グレードコードCがG3に変換されることを確認"""
    assert grade_code_to_str("C") == "G3"


def test_grade_code_to_str_重賞_open_special() -> None:
    """グレードコードDがグレードのない重賞に変換されることを確認"""
    assert grade_code_to_str("D") == "グレードのない重賞"


def test_grade_code_to_str_open() -> None:
    """グレードコードEが重賞以外の特別競走に変換されることを確認"""
    assert grade_code_to_str("E") == "重賞以外の特別競走"


def test_grade_code_to_str_3_wins() -> None:
    """グレードコードFがJ･G1に変換されることを確認"""
    assert grade_code_to_str("F") == "J･G1"


def test_grade_code_to_str_2_wins() -> None:
    """グレードコードGがJ･G2に変換されることを確認"""
    assert grade_code_to_str("G") == "J･G2"


def test_grade_code_to_str_1_win() -> None:
    """グレードコードHがJ･G3に変換されることを確認"""
    assert grade_code_to_str("H") == "J･G3"


def test_grade_code_to_str_listed() -> None:
    """グレードコードLがリステッドに変換されることを確認"""
    assert grade_code_to_str("L") == "リステッド"


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
