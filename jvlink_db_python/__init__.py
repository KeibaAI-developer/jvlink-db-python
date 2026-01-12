"""jvlink-db-python: JV-Linkデータベースからのデータ取得を簡単にするPythonライブラリ

このパッケージは、JVLinkToSQLiteで生成されたrace.dbから
競馬データを簡単に取得するためのツールを提供します。

主なモジュール:
    - manager: データベース管理（JVLinkDBManager）
    - fetcher: データ取得API（JVLinkDataFetcher）
    - utils: ユーティリティ関数（ID変換、コード変換等）
    - exceptions: 例外クラス
"""

__version__ = "0.1.0"
__author__ = "Kubo-Tech"
__license__ = "MIT"
