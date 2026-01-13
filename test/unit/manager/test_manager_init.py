"""JVLinkDBManagerの__init__メソッドの単体テスト"""

from pathlib import Path

import pytest

from jvlink_db_python.exceptions import JVLinkToSQLiteError
from jvlink_db_python.manager import JVLinkDBManager


# 正常系
def test_init_with_default_config(
    temp_jvlinktosqlite_exe: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """デフォルト設定でJVLinkDBManagerが初期化できることを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        monkeypatch (pytest.MonkeyPatch): pytestのmonkeypatch fixture
    """
    # JVLinkToSQLite実行ファイルのパスをモック
    monkeypatch.setattr(
        "jvlink_db_python.manager.Path",
        lambda p: temp_jvlinktosqlite_exe if "JVLinkToSQLite" in str(p) else Path(p),
    )

    # デフォルト設定で初期化
    manager = JVLinkDBManager()

    # デフォルト値が設定されていることを確認
    assert manager.db_path == Path("./race.db")
    assert manager.jvlinktosqlite_path == temp_jvlinktosqlite_exe
    assert "database" in manager.config
    assert "jvlinktosqlite" in manager.config


def test_init_with_custom_paths(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """カスタムパスでJVLinkDBManagerが初期化できることを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
        monkeypatch (pytest.MonkeyPatch): pytestのmonkeypatch fixture
    """
    custom_db_path = tmp_path / "custom_race.db"

    # カスタムパスで初期化
    manager = JVLinkDBManager(
        db_path=str(custom_db_path),
        jvlinktosqlite_path=str(temp_jvlinktosqlite_exe),
    )

    # カスタムパスが設定されていることを確認
    assert manager.db_path == custom_db_path
    assert manager.jvlinktosqlite_path == temp_jvlinktosqlite_exe


def test_init_with_config_file(temp_config_file: Path, temp_jvlinktosqlite_exe: Path) -> None:
    """設定ファイルを指定してJVLinkDBManagerが初期化できることを確認する

    Args:
        temp_config_file (Path): テスト用設定ファイル
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
    """
    # 設定ファイルのパスをモック用に書き換え
    import yaml

    with open(temp_config_file, "r", encoding="utf-8") as f:
        config_content = yaml.safe_load(f)

    config_content["jvlinktosqlite"]["path"] = str(temp_jvlinktosqlite_exe)

    with open(temp_config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_content, f, allow_unicode=True)

    # 設定ファイルを指定して初期化
    manager = JVLinkDBManager(config_path=str(temp_config_file))

    # 設定ファイルの内容が反映されていることを確認
    assert manager.db_path == Path("./test_race.db")
    assert manager.jvlinktosqlite_path == temp_jvlinktosqlite_exe
    assert manager.config["jvlinktosqlite"]["throttle_size"] == 200
    assert manager.config["jvlinktosqlite"]["log_level"] == "Debug"


def test_init_argument_priority(
    temp_config_file: Path, temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """引数 > 設定ファイル > デフォルト の優先順位を確認する

    Args:
        temp_config_file (Path): テスト用設定ファイル
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    # 設定ファイルのパスをモック用に書き換え
    import yaml

    with open(temp_config_file, "r", encoding="utf-8") as f:
        config_content = yaml.safe_load(f)

    config_content["jvlinktosqlite"]["path"] = str(temp_jvlinktosqlite_exe)

    with open(temp_config_file, "w", encoding="utf-8") as f:
        yaml.dump(config_content, f, allow_unicode=True)

    # 引数でカスタムパスを指定
    custom_db_path = tmp_path / "argument_priority.db"
    manager = JVLinkDBManager(
        db_path=str(custom_db_path),
        config_path=str(temp_config_file),
    )

    # 引数が最優先されることを確認
    assert manager.db_path == custom_db_path
    # 引数で指定しなかったパスは設定ファイルの値が使用される
    assert manager.jvlinktosqlite_path == temp_jvlinktosqlite_exe


# 準正常系
def test_init_jvlinktosqlite_not_found(tmp_path: Path) -> None:
    """JVLinkToSQLite実行ファイルが存在しない場合にエラーが発生することを確認する

    Args:
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    non_existent_path = tmp_path / "non_existent.exe"

    # 存在しないパスを指定してエラーが発生することを確認
    with pytest.raises(JVLinkToSQLiteError) as exc_info:
        JVLinkDBManager(jvlinktosqlite_path=str(non_existent_path))

    # エラーメッセージに実行ファイルが見つからない旨が含まれることを確認
    assert "non_existent.exeが見つかりません" in str(exc_info.value)


def test_init_jvlinktosqlite_is_directory(tmp_path: Path) -> None:
    """JVLinkToSQLiteパスがディレクトリの場合にエラーが発生することを確認する

    Args:
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    # ディレクトリを作成
    dir_path = tmp_path / "jvlinktosqlite_dir"
    dir_path.mkdir()

    # ディレクトリパスを指定してエラーが発生することを確認
    with pytest.raises(JVLinkToSQLiteError) as exc_info:
        JVLinkDBManager(jvlinktosqlite_path=str(dir_path))

    # エラーメッセージにファイルではない旨が含まれることを確認
    assert "jvlinktosqlite_dirがファイルではありません" in str(exc_info.value)
