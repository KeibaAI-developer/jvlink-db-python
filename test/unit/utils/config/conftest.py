"""config.pyのテスト用共通fixture"""

from pathlib import Path

import pytest


@pytest.fixture
def temp_config_dir(tmp_path: Path) -> Path:
    """一時的な設定ファイルディレクトリを作成

    Args:
        tmp_path (Path): pytestが提供する一時ディレクトリ

    Returns:
        Path: 作成した一時ディレクトリのパス
    """
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return config_dir


@pytest.fixture
def valid_config_content() -> str:
    """正常な設定ファイルの内容を返す

    Returns:
        str: YAML形式の設定内容
    """
    return """
database:
  path: "test.db"
  backup_dir: "test_backup/"

jvlinktosqlite:
  path: "test/jvlinktosqlite.exe"
  setting_xml: "test_setting.xml"
  throttle_size: 50
  log_level: "Debug"

data_specs:
  default:
    - "RA"
    - "SE"

update:
  auto_update: true
  update_interval_minutes: 30
  realtime:
    - "RA"
"""


@pytest.fixture
def invalid_yaml_content() -> str:
    """不正なYAML形式の内容を返す

    Returns:
        str: 不正なYAML形式の文字列
    """
    return """
database:
  path: "test.db"
  invalid_indent
    nested: "value"
"""


@pytest.fixture
def partial_config_content() -> str:
    """部分的な設定ファイルの内容を返す

    Returns:
        str: 一部の設定のみを含むYAML形式の文字列
    """
    return """
database:
  path: "custom.db"

jvlinktosqlite:
  log_level: "Warn"
"""
