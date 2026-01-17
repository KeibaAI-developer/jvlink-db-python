"""JVLinkDBManagerのinitialize_databaseメソッドの単体テスト"""

import xml.etree.ElementTree as Et
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from jvlink_db_python.exceptions import JVLinkToSQLiteError
from jvlink_db_python.manager import JVLinkDBManager


# 正常系
def test_initialize_database_creates_database_successfully(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """正常にデータベースが生成されることを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path),
        jvlinktosqlite_path=str(temp_jvlinktosqlite_exe),
    )

    # setting.xmlの出力先を一時ディレクトリに設定
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="データベース生成完了",
            stderr="",
        )

        # 初期化実行
        manager.initialize_database(start_date="2024-01-01")

        # subprocessが呼ばれたことを確認
        assert mock_run.called
        call_args = mock_run.call_args[0][0]
        assert str(temp_jvlinktosqlite_exe) in call_args
        assert str(db_path) in call_args
        assert str(setting_xml) in call_args

        # setting.xmlが生成されたことを確認
        assert setting_xml.exists()


def test_initialize_database_reflects_start_date_correctly(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """開始日がsetting.xmlに正しく反映されることを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path),
        jvlinktosqlite_path=str(temp_jvlinktosqlite_exe),
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # 初期化実行
        start_date = "2023-06-01"
        manager.initialize_database(start_date=start_date)

        # setting.xmlの内容を確認
        tree = Et.parse(setting_xml)
        root = tree.getroot()

        # JVSetupDataUpdateSettingが存在することを確認
        setup_settings = root.findall(".//JVSetupDataUpdateSetting")
        assert len(setup_settings) > 0

        # IsEnabledがtrueであることを確認
        is_enabled = setup_settings[0].find("IsEnabled")
        assert is_enabled is not None
        assert is_enabled.text == "true"

        # KaisaiDateTimeが正しく設定されていることを確認
        datetime_keys = root.findall(".//JVKaisaiDateTimeKey/KaisaiDateTime")
        if datetime_keys:
            # 最初の日付が開始日と一致することを確認
            datetime_text = datetime_keys[0].text
            assert datetime_text is not None
            assert start_date in datetime_text


def test_initialize_database_reflects_data_specs_correctly(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """data_specsの指定が正しく反映されることを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path), jvlinktosqlite_path=str(temp_jvlinktosqlite_exe)
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")

        # 特定のdata_specsで初期化実行
        data_specs = ["RA", "SE", "UM"]
        manager.initialize_database(start_date="2024-01-01", data_specs=data_specs)

        # setting.xmlの内容を確認
        tree = Et.parse(setting_xml)
        root = tree.getroot()

        # DataSpecの値を取得
        data_spec_elements = root.findall(".//DataSpec")
        data_spec_values = {elem.text for elem in data_spec_elements}

        # 指定したレコード種別に対応するDataSpecが含まれていることを確認
        # RA, SE -> RACE, UM -> DIFF
        assert "RACE" in data_spec_values
        assert "DIFF" in data_spec_values


def test_initialize_database_succeeds_with_warning_on_returncode_4294966893(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """終了コード4294966893（RC=-403）で警告付きで正常終了することを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
        capsys (pytest.CaptureFixture[str]): 標準出力キャプチャ用fixture
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path), jvlinktosqlite_path=str(temp_jvlinktosqlite_exe)
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化して終了コード4294966893を返す
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=4294966893, stdout="", stderr="")

        # 初期化実行（例外が発生しないことを確認）
        manager.initialize_database(start_date="2024-01-01")

        # 標準出力に警告メッセージが含まれることを確認
        captured = capsys.readouterr()
        assert "[WARNING]" in captured.out
        assert "警告付きで終了しました" in captured.out
        assert "4294966893" in captured.out


# 準正常系
def test_initialize_database_raises_value_error_for_invalid_date_format(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """不正な日付形式でValueErrorが発生することを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"

    manager = JVLinkDBManager(
        db_path=str(db_path),
        jvlinktosqlite_path=str(temp_jvlinktosqlite_exe),
    )

    # 不正な日付形式（スラッシュ区切り）
    with pytest.raises(ValueError, match="日付形式が不正です"):
        manager.initialize_database(start_date="2024/01/01")


def test_initialize_database_raises_error_on_non_zero_returncode(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """0と4294966893以外の終了コードでJVLinkToSQLiteErrorが発生することを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path), jvlinktosqlite_path=str(temp_jvlinktosqlite_exe)
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化して異常な終了コード（1）を返す
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=1, stdout="", stderr="")

        # JVLinkToSQLiteErrorが発生することを確認
        with pytest.raises(JVLinkToSQLiteError, match="JVLinkToSQLite.exeの実行に失敗しました"):
            manager.initialize_database(start_date="2024-01-01")


def test_initialize_database_raises_error_on_execution_failure(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """JVLinkToSQLite.exe実行エラーでJVLinkToSQLiteErrorが発生することを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path), jvlinktosqlite_path=str(temp_jvlinktosqlite_exe)
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化してエラーを発生させる
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = Exception("実行エラー")

        # JVLinkToSQLiteErrorが発生することを確認
        with pytest.raises(JVLinkToSQLiteError, match="予期しないエラーが発生しました"):
            manager.initialize_database(start_date="2024-01-01")


def test_initialize_database_raises_error_on_subprocess_called_process_error(
    temp_jvlinktosqlite_exe: Path, tmp_path: Path
) -> None:
    """subprocess.CalledProcessErrorでJVLinkToSQLiteErrorが発生することを確認する

    Args:
        temp_jvlinktosqlite_exe (Path): テスト用JVLinkToSQLite実行ファイル
        tmp_path (Path): pytestが提供する一時ディレクトリ
    """
    import subprocess

    db_path = tmp_path / "test_race.db"
    setting_xml = tmp_path / "test_setting.xml"

    manager = JVLinkDBManager(
        db_path=str(db_path), jvlinktosqlite_path=str(temp_jvlinktosqlite_exe)
    )
    manager.config["jvlinktosqlite"]["setting_xml"] = str(setting_xml)

    # subprocessをモック化してCalledProcessErrorを発生させる
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1,
            cmd="dummy",
            output="output",
            stderr="error",
        )

        # JVLinkToSQLiteErrorが発生することを確認
        with pytest.raises(JVLinkToSQLiteError, match="予期しないエラーが発生しました"):
            manager.initialize_database(start_date="2024-01-01")
