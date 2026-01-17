"""JVLinkDBManager単体テスト用のpytest設定"""

from pathlib import Path

import pytest
import yaml


@pytest.fixture
def temp_config_file(tmp_path: Path) -> Path:
    """テスト用の設定ファイルを作成するfixture

    Args:
        tmp_path (Path): pytestが提供する一時ディレクトリ

    Returns:
        Path: 作成された設定ファイルのパス
    """
    config_content = {
        "database": {
            "path": "./test_race.db",
            "backup_dir": "./test_backup/",
        },
        "jvlinktosqlite": {
            "path": "./JVLinkToSQLite.exe",
            "setting_xml": "./test_setting.xml",
            "throttle_size": 200,
            "log_level": "Debug",
        },
        "data_specs": {
            "default": ["RA", "SE"],
        },
    }

    config_file = tmp_path / "test_config.yml"
    with open(config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_content, f, allow_unicode=True)

    return config_file


@pytest.fixture
def temp_jvlinktosqlite_exe(tmp_path: Path) -> Path:
    """テスト用のJVLinkToSQLite実行ファイルを作成するfixture

    Args:
        tmp_path (Path): pytestが提供する一時ディレクトリ

    Returns:
        Path: 作成された実行ファイルのパス
    """
    exe_path = tmp_path / "JVLinkToSQLite.exe"
    exe_path.write_text("dummy exe file")
    return exe_path
