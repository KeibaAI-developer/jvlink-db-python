"""データベース管理モジュール

JV-LinkデータベースのCRUD操作を管理するクラスを提供する。
"""

from pathlib import Path

from jvlink_db_python.exceptions import JVLinkToSQLiteError
from jvlink_db_python.utils.config import load_config


class JVLinkDBManager:
    """JV-Linkデータベース管理クラス

    JVLinkToSQLiteArtifact_0.1.0.0.exeを使用してrace.dbの初期生成・更新を管理する。

    Attributes:
        db_path (Path): データベースファイルのパス
        jvlinktosqlite_path (Path): JVLinkToSQLite実行ファイルのパス
        config (dict): 設定情報
    """

    def __init__(
        self,
        db_path: str | None = None,
        jvlinktosqlite_path: str | None = None,
        config_path: str | None = None,
    ):
        """JVLinkDBManagerを初期化する

        Args:
            db_path (str | None): データベースファイルのパス。
                Noneの場合は設定ファイルの値を使用。
            jvlinktosqlite_path (str | None): JVLinkToSQLite実行ファイルのパス。
                Noneの場合は設定ファイルの値を使用。
            config_path (str | None): 設定ファイルのパス。
                Noneの場合はデフォルトパスを使用。

        Raises:
            JVLinkToSQLiteError: JVLinkToSQLiteArtifact_0.1.0.0.exeが見つからない場合
        """
        # 設定ファイルを読み込み
        self.config = load_config(config_path)

        # データベースパスの決定（引数 > 設定ファイル > デフォルト）
        if db_path is not None:
            self.db_path = Path(db_path)
        else:
            self.db_path = Path(self.config["database"]["path"])

        # JVLinkToSQLiteパスの決定（引数 > 設定ファイル > デフォルト）
        if jvlinktosqlite_path is not None:
            self.jvlinktosqlite_path = Path(jvlinktosqlite_path)
        else:
            self.jvlinktosqlite_path = Path(self.config["jvlinktosqlite"]["path"])

        # JVLinkToSQLite実行ファイルの存在チェック
        if not self.jvlinktosqlite_path.exists():
            error_message = (
                f"JVLinkToSQLiteArtifact_0.1.0.0.exeが見つかりません: "
                f"{self.jvlinktosqlite_path.absolute()}"
            )
            raise JVLinkToSQLiteError(error_message)

        # 実行ファイルかどうかを確認（Windowsでは.exe）
        if not self.jvlinktosqlite_path.is_file():
            error_message = (
                f"JVLinkToSQLiteArtifact_0.1.0.0.exeがファイルではありません: "
                f"{self.jvlinktosqlite_path.absolute()}"
            )
            raise JVLinkToSQLiteError(error_message)
