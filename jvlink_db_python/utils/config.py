"""設定ファイル管理モジュール

YAMLファイルから設定を読み込み、デフォルト値を適用する機能を提供する。
"""

from pathlib import Path
from typing import Any

import yaml

from jvlink_db_python.exceptions import JVLinkDBError


def load_config(config_path: str | None = None) -> dict[str, Any]:
    """設定ファイルを読み込む

    YAMLファイルから設定を読み込み、辞書形式で返す。
    設定ファイルが存在しない場合はデフォルト値を返す。

    Args:
        config_path (str | None): 設定ファイルのパス。Noneの場合はデフォルトパスを使用。

    Returns:
        dict[str, Any]: 設定内容を格納した辞書

    Raises:
        JVLinkDBError: 設定ファイルの読み込みに失敗した場合
    """
    # デフォルト設定
    default_config = _get_default_config()

    # 設定ファイルパスの決定
    if config_path is None:
        # デフォルトパス: プロジェクトルート/config/config.yml
        project_root = Path(__file__).parent.parent.parent
        config_path_obj = project_root / "config" / "config.yml"
    else:
        config_path_obj = Path(config_path)

    # 設定ファイルが存在しない場合はデフォルト設定を返す
    if not config_path_obj.exists():
        return default_config

    # 設定ファイルの読み込み
    try:
        with open(config_path_obj, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f)

        # user_configがNoneまたは空の場合はデフォルト設定を返す
        if user_config is None or (isinstance(user_config, dict) and not user_config):
            return default_config

        # user_configがdictでない場合はエラー
        if not isinstance(user_config, dict):
            error_message = (
                f"設定ファイルの形式が不正です: "
                f"辞書形式のYAMLが期待されますが、{type(user_config).__name__}型が読み込まれました"
            )
            raise JVLinkDBError(error_message)

        # デフォルト設定にユーザー設定をマージ
        merged_config = _merge_config(default_config, user_config)
        return merged_config

    except yaml.YAMLError as e:
        error_message = f"設定ファイルの読み込みに失敗しました: {e}"
        raise JVLinkDBError(error_message) from e
    except OSError as e:
        error_message = f"設定ファイルのアクセスに失敗しました: {e}"
        raise JVLinkDBError(error_message) from e


def _get_default_config() -> dict[str, Any]:
    """デフォルト設定を返す

    Returns:
        dict[str, Any]: デフォルト設定
    """
    return {
        "database": {
            "path": "./race.db",
            "backup_dir": "./backup/",
        },
        "jvlinktosqlite": {
            "path": "./JVLinkToSQLiteArtifact_0.1.0.0.exe",
            "setting_xml": "./setting.xml",
            "throttle_size": 100,
            "log_level": "Info",
        },
        "data_specs": {
            "default": [
                # コース情報
                "CS",
                # レース情報
                "YS",
                "RA",
                # 馬情報
                "TK",
                "SE",
                "HS",
                "HY",
                "HN",
                "SK",
                "BT",
                # オッズ情報
                "HR",
                "H1",
                "H6",
                "O1",
                "O2",
                "O3",
                "O4",
                "O5",
                "O6",
                "WF",
                # マスタ情報
                "JG",
                "UM",
                "KS",
                "CH",
                "BR",
                "BN",
                "RC",
                "CK",
                # 調教情報
                "HC",
                "WC",
                # TARGET独自指数
                "DM",
                "TM",
            ],
        },
        "update": {
            "auto_update": False,
            "update_interval_minutes": 15,
            "realtime": [
                # レース情報
                "RA",
                "SE",
                # オッズ
                "HR",
                "O1",
                "O2",
                "O3",
                "O4",
                "O5",
                "O6",
                "H1",
                "H6",
                "WF",
                # レース変更情報
                "WH",
                "WE",
                "AV",
                "JC",
                "TC",
                "CC",
                # TARGET独自指数
                "DM",
                "TM",
            ],
        },
    }


def _merge_config(default: dict[str, Any], user: dict[str, Any]) -> dict[str, Any]:
    """デフォルト設定とユーザー設定をマージする

    ユーザー設定で指定された項目のみを上書きし、
    指定されていない項目はデフォルト値を使用する。
    ネストされた辞書も再帰的にマージする。

    Args:
        default (dict[str, Any]): デフォルト設定
        user (dict[str, Any]): ユーザー設定

    Returns:
        dict[str, Any]: マージされた設定
    """
    merged = default.copy()

    for key, value in user.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            # ネストされた辞書の場合は再帰的にマージ
            merged[key] = _merge_config(merged[key], value)
        else:
            # それ以外の場合はユーザー設定で上書き
            merged[key] = value

    return merged
