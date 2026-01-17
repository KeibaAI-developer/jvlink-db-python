"""データベース初期化のサンプルスクリプト

JVLinkDBManagerを使用してrace.dbを初期生成するサンプルコード。
Windows環境でのみ動作します。
"""

# flake8: noqa: E402
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlite3
import sys
import time

from jvlink_db_python.manager import JVLinkDBManager


def main() -> None:
    """データベースを初期化する"""
    # JVLinkDBManagerのインスタンスを作成
    # 引数を指定しない場合はconfig.ymlの設定が使用される
    manager = JVLinkDBManager()

    # 開始時刻
    start_time = time.time()
    print(f"開始時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # データベースの初期化
    try:
        manager.initialize_database(start_date="2019-01-01")
    except Exception as e:
        print(f"データベースの初期化中にエラーが発生しました:\n{e}")
        _print_elapsed_time(start_time)
        return

    # 終了時刻
    print("\nデータベースの初期化処理が完了しました")
    _print_elapsed_time(start_time)

    # データベース確認
    _check_database(str(manager.db_path))


def _check_database(db_path: str) -> None:
    """データベースの内容を確認する

    Args:
        db_path (str): データベースファイルのパス
    """
    print("\n" + "=" * 80)
    print("データベース内容の確認")
    print("=" * 80 + "\n")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブル一覧取得
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = cursor.fetchall()

    print(f"テーブル数: {len(tables)}\n")
    print("主要テーブル:")
    for table in tables[:30]:
        # レコード数取得
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
        count = cursor.fetchone()[0]
        print(f"  - {table[0]:<30} {count:>10,} レコード")

    # NL_RA_RACE（中央競馬のみ）の年別レース数を確認
    print("\n\nNL_RA_RACE（中央競馬のみ）の年別レース数:")
    cursor.execute(
        """
        SELECT idYear, COUNT(*) as race_count
        FROM NL_RA_RACE
        WHERE idJyoCD BETWEEN '01' AND '10'
        GROUP BY idYear
        ORDER BY idYear
    """
    )
    year_counts = cursor.fetchall()
    for year, count in year_counts:
        print(f"  {year}年: {count:>6,} レース")

    # 最古と最新のレース（中央競馬のみ）を確認
    print("\n最古のレース（中央競馬のみ）:")
    cursor.execute(
        """
        SELECT idYear, idMonthDay, RaceInfoHondai
        FROM NL_RA_RACE
        WHERE idJyoCD BETWEEN '01' AND '10'
        ORDER BY idYear, idMonthDay
        LIMIT 1
    """
    )
    oldest = cursor.fetchone()
    if oldest:
        print(f"  {oldest[0]}年{oldest[1][:2]}月{oldest[1][2:]}日: {oldest[2]}")

    print("\n最新のレース（中央競馬のみ）:")
    cursor.execute(
        """
        SELECT idYear, idMonthDay, RaceInfoHondai
        FROM NL_RA_RACE
        WHERE idJyoCD BETWEEN '01' AND '10'
        ORDER BY idYear DESC, idMonthDay DESC
        LIMIT 1
    """
    )
    newest = cursor.fetchone()
    if newest:
        print(f"  {newest[0]}年{newest[1][:2]}月{newest[1][2:]}日: {newest[2]}")

    conn.close()


def _print_elapsed_time(start_time: float) -> None:
    """経過時間を表示する

    Args:
        start_time (float): 開始時刻（time.time()の戻り値）
    """
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"終了時刻: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"処理時間: {elapsed_time:.2f}秒 ({elapsed_time / 60:.2f}分)")


if __name__ == "__main__":
    main()
