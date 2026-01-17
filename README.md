# jvlink-db-python

JV-Linkデータベースからのデータ取得を簡単にするPythonライブラリ

## 概要

`jvlink-db-python`は、JRA-VANのJV-Linkサービスから取得したデータを格納したSQLiteデータベース（race.db）からデータを簡単に取得するためのPythonライブラリです。

[JVLinkToSQLite](https://github.com/urasandesu/JVLinkToSQLite)を利用してJV-LinkデータをSQLiteデータベースに変換し、Pythonから簡単に競馬データを取得できるようにします。

## 主な機能

### データベース管理（JVLinkDBManager）

- **初期データベース生成**: 指定期間のデータを取得してrace.dbを作成
- **データベース更新**: 既存のrace.dbを最新データに更新
- **JVLinkToSQLiteの自動実行**: データ取得処理を自動化

### データ取得API（JVLinkDataFetcher）

race.dbから以下のデータをpandas DataFrameとして取得できます：

- **レース情報**: レース条件、距離、馬場状態等
- **出走馬情報**: 馬番、騎手、オッズ、結果等
- **馬情報**: 馬の基本情報と過去戦績
- **マスタ情報**: 騎手、厩舎、馬主、生産者の情報
- **開催一覧**: レーススケジュール
- **払戻・オッズ情報**: 各券種の払戻とオッズ

### ユーティリティ

- **ID変換**: netkeiba IDとJV-Link IDの相互変換
- **コード変換**: JV-Linkのコード値を人間が読める文字列に変換

## 必須環境

- **OS**: Windows 10/11（JV-Link動作環境）
- **Python**: 3.12以上
- **JV-Link SDK**: Ver4.8.0.2以上
- **JVLinkToSQLite**: 実行ファイル

## インストール

### 1. 事前準備

JV-Link SDKをインストールし、JRA-VANのサービスID認証を完了させてください。

### 2. JVLinkToSQLiteのセットアップ

本プロジェクトでは、サブモジュールとして[HRSoftUsingJVLinkToSQLite](https://github.com/urasandesu/HRSoftUsingJVLinkToSQLite)を含めており、そこにある実行ファイルを使用します。

#### 2-1. サブモジュールの初期化

本リポジトリをクローンした後、サブモジュールを初期化してください：

```bash
# サブモジュールの初期化と更新
git submodule update --init --recursive
```

#### 2-2. 実行ファイルを解凍

/HRSoftUsingJVLinkToSQLite/HRSoftUsingJVLinkToSQLite/JVLinkToSQLiteArtifact_0.1.0.0.exeを実行し、同じディレクトリに`JVLinkToSQLiteArtifact/`フォルダが生成されることを確認してください。

#### 2-3. git管理について

JVLinkToSQLiteArtifact_0.1.0.0.exeの実行時に自動展開される`JVLinkToSQLiteArtifact/`フォルダは、HRSoftUsingJVLinkToSQLiteリポジトリの`.gitignore`で管理対象外に設定されています。gitの変更が気になる場合は`JVLinkToSQLiteArtifact/`を追加してください。

### 3. パッケージのインストール

```bash
pip install -e .
```

### 4. 開発環境のセットアップ（開発者向け）

```bash
pip install -e ".[dev]"
pre-commit install
```

## 使い方

### 基本的な使い方

```python
from jvlink_db_python.manager import JVLinkDBManager
from jvlink_db_python.fetcher import JVLinkDataFetcher

# データベース初期化（初回のみ）
manager = JVLinkDBManager()
manager.initialize_database(
    start_date="2024-01-01"
)

# データ取得
fetcher = JVLinkDataFetcher()

# レース情報取得
race_info = fetcher.get_race_info(
    race_id="202401010101",
    date_id="202401010101"
)

# 出走馬情報取得
horses = fetcher.get_race_horses(
    race_id="202401010101",
    date_id="202401010101",
    include_results=True
)
```

詳細な使用例は[example/](example/)ディレクトリを参照してください。

## プロジェクト構成

```
jvlink-db-python/
├── README.md                      # 本ファイル
├── pyproject.toml                 # パッケージ設定
├── requirements.txt               # 依存パッケージ
├── requirements-dev.txt           # 開発用パッケージ
├── setup.py                       # セットアップスクリプト
├── doc/                           # ドキュメント
│   ├── INSTRUCTION.md             # プロジェクト概要
│   ├── SPEC.md                    # 機能仕様書
│   └── PLAN.md                    # 実装計画書
├── example/                       # 使用例
├── jvlink_db_python/              # メインパッケージ
│   ├── manager.py                 # データベース管理
│   ├── fetcher.py                 # データ取得API
│   ├── utils/                     # ユーティリティ
│   └── exceptions.py              # 例外クラス
├── test/                          # テスト
├── config/                        # 設定ファイル
├── JVLinkToSQLite/                # サブモジュール
└── JVLinkToSQLite.wiki/           # サブモジュール
```

## 開発

### テストの実行

```bash
# 全テスト実行
pytest

# カバレッジ付き実行
pytest --cov=jvlink_db_python --cov-report=html

# 特定のテストのみ実行
pytest test/unit/utils/
```

### コード品質チェック

```bash
# フォーマット
black .
isort .

# リント
flake8

# 型チェック
mypy jvlink_db_python
```

## ライセンス

MIT License

## 関連リンク

- [JVLinkToSQLite](https://github.com/urasandesu/JVLinkToSQLite)
- [JV-Link](https://developer.jra-van.jp/t/topic/45)

## 注意事項

- 本ライブラリはWindows環境でのみ動作します（JV-Link制約）
- JRA-VANサービスへの加入とJV-Linkの契約が必要です
- データ取得には時間がかかる場合があります
- race.dbのサイズは数GB〜数十GBになる可能性があります

## サポート

問題や質問がある場合は、[Issues](https://github.com/KeibaAI-developer/jvlink-db-python/issues)で報告してください。
