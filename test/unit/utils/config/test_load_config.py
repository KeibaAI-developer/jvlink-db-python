"""load_config関数のテスト"""

from pathlib import Path

import pytest

from jvlink_db_python.exceptions import JVLinkDBError
from jvlink_db_python.utils.config import load_config


# 正常系
def test_load_config_with_valid_file(temp_config_dir: Path, valid_config_content: str) -> None:
    """正常な設定ファイルを読み込めることを確認"""
    # 設定ファイルを作成
    config_file = temp_config_dir / "config.yml"
    config_file.write_text(valid_config_content, encoding="utf-8")

    # 設定を読み込む
    config = load_config(str(config_file))

    # 期待値と一致することを確認
    assert config["database"]["path"] == "test.db"
    assert config["database"]["backup_dir"] == "test_backup/"
    assert config["jvlinktosqlite"]["path"] == "test/jvlinktosqlite.exe"
    assert config["jvlinktosqlite"]["setting_xml"] == "test_setting.xml"
    assert config["jvlinktosqlite"]["throttle_size"] == 50
    assert config["jvlinktosqlite"]["log_level"] == "Debug"
    assert config["data_specs"]["default"] == ["RA", "SE"]
    assert config["update"]["auto_update"] is True
    assert config["update"]["update_interval_minutes"] == 30
    assert config["update"]["realtime"] == ["RA"]


def test_load_config_returns_default_when_file_not_exists() -> None:
    """設定ファイルが存在しない場合にデフォルト設定を返すことを確認"""
    # 存在しないパスを指定
    config = load_config("nonexistent/config.yml")

    # デフォルト値が返されることを確認
    assert config["database"]["path"] == "./race.db"
    assert config["database"]["backup_dir"] == "./backup/"
    default_path = "./HRSoftUsingJVLinkToSQLite/HRSoftUsingJVLinkToSQLite/JVLinkToSQLiteArtifact/JVLinkToSQLite.exe"  # noqa: E501
    assert config["jvlinktosqlite"]["path"] == default_path
    assert config["jvlinktosqlite"]["setting_xml"] == "./setting.xml"
    assert config["jvlinktosqlite"]["throttle_size"] == 100
    assert config["jvlinktosqlite"]["log_level"] == "Info"
    assert "RA" in config["data_specs"]["default"]
    assert "SE" in config["data_specs"]["default"]
    assert config["update"]["auto_update"] is False
    assert config["update"]["update_interval_minutes"] == 15


def test_load_config_merges_partial_config(
    temp_config_dir: Path, partial_config_content: str
) -> None:
    """部分的な設定ファイルがデフォルト設定とマージされることを確認"""
    # 部分的な設定ファイルを作成
    config_file = temp_config_dir / "config.yml"
    config_file.write_text(partial_config_content, encoding="utf-8")

    # 設定を読み込む
    config = load_config(str(config_file))

    # ユーザー設定で上書きされた値を確認
    assert config["database"]["path"] == "custom.db"
    assert config["jvlinktosqlite"]["log_level"] == "Warn"

    # デフォルト値が残っていることを確認
    assert config["database"]["backup_dir"] == "./backup/"
    default_path = "./HRSoftUsingJVLinkToSQLite/HRSoftUsingJVLinkToSQLite/JVLinkToSQLiteArtifact/JVLinkToSQLite.exe"  # noqa: E501
    assert config["jvlinktosqlite"]["path"] == default_path
    assert config["jvlinktosqlite"]["setting_xml"] == "./setting.xml"
    assert config["jvlinktosqlite"]["throttle_size"] == 100
    assert "RA" in config["data_specs"]["default"]


def test_load_config_with_empty_file(temp_config_dir: Path) -> None:
    """空の設定ファイルの場合にデフォルト設定を返すことを確認"""
    # 空のファイルを作成
    config_file = temp_config_dir / "config.yml"
    config_file.write_text("", encoding="utf-8")

    # 設定を読み込む
    config = load_config(str(config_file))

    # デフォルト値が返されることを確認
    assert config["database"]["path"] == "./race.db"
    default_path = "./HRSoftUsingJVLinkToSQLite/HRSoftUsingJVLinkToSQLite/JVLinkToSQLiteArtifact/JVLinkToSQLite.exe"  # noqa: E501
    assert config["jvlinktosqlite"]["path"] == default_path


def test_load_config_with_none_path() -> None:
    """config_pathにNoneを指定した場合にデフォルトパスが使用されることを確認"""
    # Noneを指定（デフォルトパスの設定ファイルは存在しないと仮定）
    config = load_config(None)

    # デフォルト値が返されることを確認（ファイルが存在しない場合の動作）
    assert "database" in config
    assert "jvlinktosqlite" in config
    assert "data_specs" in config
    assert "update" in config


# 準正常系
def test_load_config_raises_error_on_invalid_yaml(
    temp_config_dir: Path, invalid_yaml_content: str
) -> None:
    """不正なYAML形式の場合にエラーが発生することを確認"""
    # 不正なYAMLファイルを作成
    config_file = temp_config_dir / "config.yml"
    config_file.write_text(invalid_yaml_content, encoding="utf-8")

    # エラーが発生することを確認
    with pytest.raises(JVLinkDBError, match="設定ファイルの読み込みに失敗しました"):
        load_config(str(config_file))


@pytest.mark.skip(reason="rootユーザーではパーミッションチェックが無効")
def test_load_config_raises_error_on_permission_denied(temp_config_dir: Path) -> None:
    """ファイルアクセス権限がない場合にエラーが発生することを確認"""
    # 設定ファイルを作成
    config_file = temp_config_dir / "config.yml"
    config_file.write_text("database:\n  path: test.db", encoding="utf-8")

    # ファイルを読み取り不可にする
    config_file.chmod(0o000)

    # エラーが発生することを確認
    try:
        with pytest.raises(JVLinkDBError, match="設定ファイルのアクセスに失敗しました"):
            load_config(str(config_file))
    finally:
        # テスト後にパーミッションを戻す
        config_file.chmod(0o644)
