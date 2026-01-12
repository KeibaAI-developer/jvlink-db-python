"""jvlink-db-python用の例外クラス定義

このモジュールは、jvlink-db-pythonライブラリで使用される
カスタム例外クラスを定義する。
"""


class JVLinkDBError(Exception):
    """jvlink-db-python基底例外

    jvlink-db-pythonライブラリで発生する全ての例外の基底クラス。
    ライブラリ固有のエラーをキャッチする際に使用する。
    """


class DatabaseNotFoundError(JVLinkDBError):
    """データベースファイルが見つからないエラー

    指定されたデータベースファイル（race.db）が存在しない場合に発生。
    """


class JVLinkToSQLiteError(JVLinkDBError):
    """JVLinkToSQLite実行エラー

    JVLinkToSQLite.exeの実行に失敗した場合や、
    実行中にエラーが発生した場合に発生。
    """


class DataNotFoundError(JVLinkDBError):
    """指定されたデータが見つからないエラー

    データベースクエリの結果、該当するデータが存在しない場合に発生。
    例：存在しないrace_id、horse_id等を指定した場合。
    """


class IDConversionError(JVLinkDBError):
    """ID変換エラー

    netkeiba IDとJV-Link ID間の変換処理に失敗した場合に発生。
    例：不正なIDフォーマット、必須パラメータの欠如等。
    """
