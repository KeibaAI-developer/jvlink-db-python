"""track_code_to_str関数の単体テスト"""

from jvlink_db_python.utils.code_converter import track_code_to_str


# 正常系
def test_track_code_to_str_turf() -> None:
    """トラックコード10が芝・直線に変換されることを確認"""
    assert track_code_to_str("10") == "芝・直線"


def test_track_code_to_str_turf_straight() -> None:
    """トラックコード11が芝・左回りに変換されることを確認"""
    assert track_code_to_str("11") == "芝・左回り"


def test_track_code_to_str_turf_right() -> None:
    """トラックコード12が芝・左外回りに変換されることを確認"""
    assert track_code_to_str("12") == "芝・左外回り"


def test_track_code_to_str_turf_left() -> None:
    """トラックコード13が芝・左内-外回りに変換されることを確認"""
    assert track_code_to_str("13") == "芝・左内-外回り"


def test_track_code_to_str_dirt_right() -> None:
    """トラックコード24がダート・右回りに変換されることを確認"""
    assert track_code_to_str("24") == "ダート・右回り"


def test_track_code_to_str_dirt_left() -> None:
    """トラックコード23がダート・左回りに変換されることを確認"""
    assert track_code_to_str("23") == "ダート・左回り"


def test_track_code_to_str_obstacle_turf() -> None:
    """トラックコード51が障害・芝・欅に変換されることを確認"""
    assert track_code_to_str("51") == "障害・芝・欅"


def test_track_code_to_str_obstacle_turf_right() -> None:
    """トラックコード52が障害・芝・ダートに変換されることを確認"""
    assert track_code_to_str("52") == "障害・芝・ダート"


# 準正常系
def test_track_code_to_str_undefined_code() -> None:
    """未定義のトラックコードの場合に不明を返すことを確認"""
    assert track_code_to_str("99") == "不明"


def test_track_code_to_str_empty_string() -> None:
    """空文字列の場合に不明を返すことを確認"""
    assert track_code_to_str("") == "不明"


def test_track_code_to_str_invalid_format() -> None:
    """不正なフォーマットの場合に不明を返すことを確認"""
    assert track_code_to_str("XX") == "不明"
