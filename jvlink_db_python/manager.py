"""データベース管理モジュール

JV-LinkデータベースのCRUD操作を管理するクラスを提供する。
"""

import subprocess
import xml.etree.ElementTree as Et
from datetime import datetime
from pathlib import Path

from jvlink_db_python.exceptions import JVLinkToSQLiteError
from jvlink_db_python.utils.config import load_config


class JVLinkDBManager:
    """JV-Linkデータベース管理クラス

    JVLinkToSQLite.exeを使用してrace.dbの初期生成・更新を管理する。

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
            JVLinkToSQLiteError: JVLinkToSQLite.exeが見つからない場合
        """
        # 設定ファイルを読み込み
        self.config = load_config(config_path)

        # プロジェクトルートのパスを取得（相対パス解決用）
        self._project_root = Path(__file__).parent.parent

        # データベースパスの決定（引数 > 設定ファイル > デフォルト）
        if db_path is not None:
            self.db_path = Path(db_path)
        else:
            db_path_from_config = self.config["database"]["path"]
            # 相対パスの場合はプロジェクトルートからの相対パスとして解決
            if not Path(db_path_from_config).is_absolute():
                self.db_path = self._project_root / db_path_from_config
            else:
                self.db_path = Path(db_path_from_config)

        # JVLinkToSQLiteパスの決定（引数 > 設定ファイル > デフォルト）
        if jvlinktosqlite_path is not None:
            self.jvlinktosqlite_path = Path(jvlinktosqlite_path)
        else:
            jvlinktosqlite_path_from_config = self.config["jvlinktosqlite"]["path"]
            # 相対パスの場合はプロジェクトルートからの相対パスとして解決
            if not Path(jvlinktosqlite_path_from_config).is_absolute():
                self.jvlinktosqlite_path = self._project_root / jvlinktosqlite_path_from_config
            else:
                self.jvlinktosqlite_path = Path(jvlinktosqlite_path_from_config)

        # JVLinkToSQLite実行ファイルの存在チェック
        if not self.jvlinktosqlite_path.exists():
            error_message = (
                f"{self.jvlinktosqlite_path.name}が見つかりません: "
                f"{self.jvlinktosqlite_path.absolute()}"
            )
            raise JVLinkToSQLiteError(error_message)

        # 実行ファイル（.exe）かどうかを確認
        if not self.jvlinktosqlite_path.is_file():
            error_message = (
                f"{self.jvlinktosqlite_path.name}がファイルではありません: "
                f"{self.jvlinktosqlite_path.absolute()}"
            )
            raise JVLinkToSQLiteError(error_message)

    def initialize_database(
        self,
        start_date: str,
        data_specs: list[str] | None = None,
    ) -> None:
        """初期データベース生成

        指定日以降のrace.dbを初期生成する。
        JVLinkToSQLite.exeをサブプロセスで実行し、
        JV-Linkからデータを取得してSQLiteデータベースに格納する。

        Args:
            start_date (str): データ取得開始日（YYYY-MM-DD形式）
                この日付以降のすべてのデータを取得する。
            data_specs (list[str] | None): 取得するレコード種別のリスト。
                Noneの場合は設定ファイルのデフォルト値を使用。
                例: ["RA", "SE", "UM", "KS"]

        Raises:
            JVLinkToSQLiteError: JVLinkToSQLite.exe実行エラー
        """
        # setting.xmlを生成
        setting_xml_path = self._generate_setting_xml(start_date, data_specs)

        print(f"データベース初期化を開始します: {self.db_path}")
        print(f"期間: {start_date} 以降のすべてのデータ")
        print(f"設定ファイル: {setting_xml_path}")

        # JVLinkToSQLiteを実行
        try:
            # スロットルサイズの取得
            throttle_size = self.config["jvlinktosqlite"].get("throttle_size", 100)

            # コマンドライン引数を構築
            cmd = [
                str(self.jvlinktosqlite_path),
                "-m",
                "Exec",  # 実行モード
                "-d",
                str(self.db_path),  # データベースパス
                "-s",
                str(setting_xml_path),  # 設定ファイルパス
                "-t",
                str(throttle_size),  # スロットルサイズ
            ]

            print(f"実行コマンド: {' '.join(cmd)}")

            # サブプロセス実行
            result = subprocess.run(
                cmd,
                check=False,  # 終了コードを自分で判定するため
                text=True,
                encoding="cp932",  # Windows環境ではcp932（Shift-JIS）エンコーディングを使用
            )

            # 終了コードによって処理を分岐
            if result.returncode == 0:
                print("\nデータベース初期化が正常に完了しました")
            elif result.returncode == 4294966893:  # RC=-403（unsigned: 4294966893）
                # データファイル異常の警告だが処理は続行される
                print("\n[WARNING] JVLinkToSQLiteは警告付きで終了しました")
                print(f"[WARNING] 終了コード: {result.returncode}")
                print("[WARNING] 一部のデータファイルに異常がありましたが、処理は継続されました。")
            else:
                # その他の終了コードはエラーとして扱う
                error_message = (
                    f"JVLinkToSQLite.exeの実行に失敗しました\n" f"終了コード: {result.returncode}"
                )
                raise JVLinkToSQLiteError(error_message)

        except Exception as e:
            # subprocess実行自体の失敗などをキャッチ
            error_message = f"予期しないエラーが発生しました: {e}"
            raise JVLinkToSQLiteError(error_message) from e

    def _generate_setting_xml(self, start_date: str, data_specs: list[str] | None = None) -> Path:
        """setting.xmlを生成する

        Args:
            start_date (str): データ取得開始日（YYYY-MM-DD形式）
            data_specs (list[str] | None): 取得するレコード種別のリスト。
                Noneの場合は設定ファイルのデフォルト値を使用。

        Returns:
            Path: 生成されたsetting.xmlファイルのパス

        Raises:
            ValueError: 日付形式が不正な場合
        """
        # 日付のバリデーション
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"日付形式が不正です（YYYY-MM-DD形式で指定してください）: {e}") from e

        # データ種別の決定
        if data_specs is None:
            data_specs = self.config["data_specs"]["default"]

        # レコード種別IDからDataSpecへのマッピング
        record_spec_to_data_spec = _create_record_spec_mapping()

        # XML生成
        root = Et.Element(
            "JVLinkToSQLiteSetting",
            {
                "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                "xmlns:xsd": "http://www.w3.org/2001/XMLSchema",
            },
        )
        details = Et.SubElement(root, "Details")

        # JVSetupDataUpdateSettingを生成（初期化用）
        setup_setting = Et.SubElement(details, "JVSetupDataUpdateSetting")
        Et.SubElement(setup_setting, "IsEnabled").text = "true"

        data_spec_settings = Et.SubElement(setup_setting, "DataSpecSettings")

        # 必要なDataSpecを決定
        data_spec_set = set()
        for record_spec in data_specs:
            if record_spec in record_spec_to_data_spec:
                data_spec_set.add(record_spec_to_data_spec[record_spec])

        # 各DataSpecの設定を追加
        for data_spec in sorted(data_spec_set):
            spec_setting = Et.SubElement(data_spec_settings, "JVDataSpecSetting")
            Et.SubElement(spec_setting, "IsEnabled").text = "true"
            Et.SubElement(spec_setting, "DataSpec").text = data_spec

            # 開始日を指定（この日付以降のすべてのデータを取得）
            key = Et.SubElement(spec_setting, "JVKaisaiDateTimeKey")
            Et.SubElement(key, "KaisaiDateTime").text = f"{start_date}T00:00:00+09:00"

            Et.SubElement(spec_setting, "TimeIntervalUnit").text = "PT0S"

        Et.SubElement(setup_setting, "OpenOption").text = "SetupDataNoDialog"

        # その他の設定（通常更新とリアルタイム更新は無効化）
        normal_setting = Et.SubElement(details, "JVNormalUpdateSetting")
        Et.SubElement(normal_setting, "IsEnabled").text = "false"

        realtime_setting = Et.SubElement(details, "JVRealTimeDataUpdateSetting")
        Et.SubElement(realtime_setting, "IsEnabled").text = "false"

        # XMLファイルに書き込み
        setting_xml_path_from_config = self.config["jvlinktosqlite"]["setting_xml"]
        # 相対パスの場合はプロジェクトルートからの相対パスとして解決
        setting_xml_path: Path
        if not Path(setting_xml_path_from_config).is_absolute():
            setting_xml_path = self._project_root / setting_xml_path_from_config
        else:
            setting_xml_path = Path(setting_xml_path_from_config)

        # XMLのインデント整形
        _indent_xml(root)

        tree = Et.ElementTree(root)
        tree.write(
            setting_xml_path,
            encoding="utf-8",
            xml_declaration=True,
        )

        return setting_xml_path


def _create_record_spec_mapping() -> dict[str, str]:
    """レコード種別IDからDataSpecへのマッピングを作成する

    Returns:
        dict[str, str]: レコード種別ID→DataSpecのマッピング辞書
    """
    # SPEC.mdのdata_specsコメントとSettingXml-Spec.mdを参照
    mapping = {
        # コース情報
        "CS": "YSCH",
        # レース情報
        "YS": "YSCH",
        "RA": "RACE",
        # 馬情報
        "TK": "TOKU",
        "SE": "RACE",
        "HS": "HOSE",
        "HY": "HOYU",
        "HN": "BLOD",
        "SK": "BLOD",
        "BT": "BLOD",
        # オッズ情報
        "HR": "RACE",
        "H1": "RACE",
        "H6": "RACE",
        "O1": "RACE",
        "O2": "RACE",
        "O3": "RACE",
        "O4": "RACE",
        "O5": "RACE",
        "O6": "RACE",
        "WF": "RACE",
        # マスタ情報
        "JG": "DIFF",
        "UM": "DIFF",
        "KS": "DIFF",
        "CH": "DIFF",
        "BR": "BLOD",
        "BN": "COMM",
        "RC": "COMM",
        "CK": "COMM",
        # 調教情報
        "HC": "SLOP",
        "WC": "WOOD",
        # TARGET独自指数
        "DM": "MING",
        "TM": "MING",
    }
    return mapping


def _indent_xml(elem: Et.Element, level: int = 0) -> None:
    """XMLを整形する（インデント追加）

    Args:
        elem (Et.Element): 整形するXML要素
        level (int): 現在のインデントレベル
    """
    indent = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent
        for child in elem:
            _indent_xml(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent
