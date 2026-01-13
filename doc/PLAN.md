# jvlink-db-python 実装計画書

## 1. 概要

本ドキュメントは、`jvlink-db-python`ライブラリの実装計画を定義する。SPEC.mdで定義した機能仕様を、人がレビュー可能なPR単位のタスクに分割して記載する。

## 2. 開発環境

### 2.1 必須環境

- Python 3.8以上
- Windows 10/11（JV-Link・JVLinkToSQLite動作環境）
- JV-Link SDK Ver4.8.0.2インストール済み
- JVLinkToSQLite実行ファイル

### 2.2 開発ツール

- pytest: テストフレームワーク
- pytest-mock: モックライブラリ
- pandas: データ処理
- PyYAML: 設定ファイル読み込み
- black, isort, flake8, mypy: コード品質管理（既存KeibaAI設定に準拠）

### 2.3 サブモジュール

```bash
# JVLinkToSQLiteとwikiをサブモジュールとして追加
git submodule add https://github.com/urasandesu/JVLinkToSQLite.git
git submodule add https://github.com/urasandesu/JVLinkToSQLite.wiki.git
```

## 3. ディレクトリ構成

```
jvlink-db-python/
├── README.md                      # 使い方ドキュメント
├── pyproject.toml                 # パッケージ設定
├── requirements.txt               # 依存パッケージ
├── requirements-dev.txt           # 開発用パッケージ
├── setup.py                       # セットアップスクリプト
├── .gitignore
├── .gitmodules                    # サブモジュール定義
├── doc/
│   ├── INSTRUCTION.md             # プロジェクト概要
│   ├── SPEC.md                    # 機能仕様書
│   ├── PLAN.md                    # 本ファイル
├── example/                       # 使用例
│   ├── basic_usage.py
│   ├── race_data_fetch.py
│   └── update_database.py
├── jvlink_db_python/              # メインパッケージ
│   ├── __init__.py
│   ├── manager.py                 # JVLinkDBManager
│   ├── fetcher.py                 # JVLinkDataFetcher
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── id_converter.py        # ID変換ユーティリティ
│   │   ├── code_converter.py      # コード変換ユーティリティ
│   │   └── config.py              # 設定管理
│   ├── exceptions.py              # 例外クラス
│   └── models/                    # データモデル（将来用）
│       └── __init__.py
├── test/                          # テスト
│   ├── conftest.py                # pytest設定
│   ├── integration/               # 結合テスト
│   │   ├── conftest.py
│   │   ├── test_database_init_normal.py
│   │   ├── test_database_update_normal.py
│   │   ├── test_race_data_fetch_normal.py
│   │   └── test_full_workflow_normal.py
│   └── unit/                      # 単体テスト
│       ├── manager/
│       │   ├── conftest.py
│       │   ├── test_initialize_database.py
│       │   └── test_update_database.py
│       ├── fetcher/
│       │   ├── conftest.py
│       │   ├── test_get_race_info.py
│       │   ├── test_get_race_horses.py
│       │   ├── test_get_horse_info.py
│       │   ├── test_get_jockey_info.py
│       │   ├── test_get_trainer_info.py
│       │   ├── test_get_owner_info.py
│       │   ├── test_get_breeder_info.py
│       │   ├── test_get_race_schedule.py
│       │   ├── test_get_payback.py
│       │   └── test_get_odds.py
│       └── utils/
│           ├── id_converter/
│           │   ├── conftest.py
│           │   ├── test_race_id_to_jvlink.py
│           │   ├── test_date_id_to_race_id.py
│           │   └── test_jvlink_to_race_id.py
│           ├── code_converter/
│           │   ├── conftest.py
│           │   ├── test_jyo_code_to_name.py
│           │   ├── test_sex_code_to_str.py
│           │   ├── test_track_code_to_str.py
│           │   └── test_grade_code_to_str.py
│           └── config/
│               ├── conftest.py
│               └── test_config_load.py
├── config/                        # 設定ファイル
│   └── config.yml                 # デフォルト設定
├── JVLinkToSQLite/                # サブモジュール
└── JVLinkToSQLite.wiki/           # サブモジュール
```

## 4. 実装タスク（PR単位）

### Phase 0: プロジェクトセットアップ

#### PR#0-1: 初期プロジェクト構成

**目的**: リポジトリの基本構造を構築

**作業内容**:
- ディレクトリ構造の作成
- README.md, pyproject.toml, setup.py作成
- requirements.txt, requirements-dev.txt作成
- .gitignore, .gitmodules作成
- サブモジュール追加（JVLinkToSQLite, JVLinkToSQLite.wiki）

**レビューポイント**:
- ディレクトリ構成が適切か
- 依存パッケージのバージョンが適切か
- サブモジュールが正しく追加されているか

**テスト**: なし（構成のみ）

---

### Phase 1: 基盤実装

#### PR#1-1: 例外クラスとユーティリティ基盤

**目的**: 全体で使用する基盤コードを実装

**作業内容**:
- `jvlink_db_python/exceptions.py`: 例外クラス定義
- `jvlink_db_python/utils/config.py`: 設定ファイル読み込み
- `config/config.yml`: デフォルト設定ファイル（既存ファイルを更新）
- `test/unit/utils/config/`: config.pyの単体テスト

**実装内容**:
- `JVLinkDBError`, `DatabaseNotFoundError`, `JVLinkToSQLiteError`, `DataNotFoundError`, `IDConversionError`
- YAMLファイル読み込み、デフォルト値の適用
- 設定ファイルのキー名：
  - `jvlinktosqlite.path`: JVLinkToSQLite実行ファイルパス
  - `jvlinktosqlite.setting_xml`: 設定ファイル名
  - `data_specs.default`: 取得するデータ種別リスト
  - `update.realtime`: リアルタイム系データ種別

**テスト**:
- 設定ファイル読み込み（正常系）
- 設定ファイルが存在しない場合のデフォルト値適用（正常系）
- 不正なYAML形式（準正常系）

**レビューポイント**:
- 例外クラスの階層構造が適切か
- 設定項目が網羅されているか
- docstringがGoogle Styleか
- 設定ファイルの構造が実際のconfig.ymlと一致しているか

---

#### PR#1-2: ID変換ユーティリティ

**目的**: netkeiba IDとJV-Link IDの相互変換機能

**作業内容**:
- `jvlink_db_python/utils/id_converter.py`: 変換関数実装
- `test/unit/utils/id_converter/`: 単体テスト

**実装内容**:
- `race_id_to_jvlink(race_id, date_id) -> dict`
- `date_id_to_race_id(date_id, kaiji, nichiji) -> str`
- `jvlink_to_race_id(**kwargs) -> str`
- `jvlink_to_date_id(**kwargs) -> str`

**テスト**:
- race_id + date_id → JV-Linkパラメータ（正常系）
- date_id + 開催情報 → race_id（正常系）
- JV-Linkパラメータ → race_id/date_id（正常系）
- 不正なフォーマット（準正常系）
- 必須パラメータ欠如（準正常系）

**レビューポイント**:
- ID変換ロジックが正確か
- エラーハンドリングが適切か
- エッジケース（1桁、境界値）が考慮されているか

---

#### PR#1-3: コード変換ユーティリティ

**目的**: JV-Linkのコード値を人間が読める文字列に変換

**作業内容**:
- `jvlink_db_python/utils/code_converter.py`: 変換関数実装
- `test/unit/utils/code_converter/`: 単体テスト

**実装内容**:
- `jyo_code_to_name(code: str) -> str`: 競馬場コード→名称
- `sex_code_to_str(code: str) -> str`: 性別コード→文字列
- `track_code_to_str(code: str) -> str`: トラックコード→文字列
- `grade_code_to_str(code: str) -> str`: グレードコード→文字列
- その他必要なコード変換関数

**テスト**:
- 各種コード変換（正常系）
- 未定義コード（準正常系：デフォルト値またはエラー）

**レビューポイント**:
- コードマッピングが正確か（JV-Data仕様書と一致）
- 未定義コードの扱いが適切か

---

### Phase 2: データベース管理機能

#### PR#2-1: JVLinkDBManager - 基本構造

**目的**: データベース管理クラスの基本構造を実装

**作業内容**:
- `jvlink_db_python/manager.py`: JVLinkDBManagerクラス定義
- コンストラクタ、設定読み込み
- JVLinkToSQLiteArtifact_0.1.0.0.exe存在チェック
- `test/unit/manager/conftest.py`: テスト用fixture

**実装内容**:
```python
class JVLinkDBManager:
    def __init__(
        self,
        db_path: str | None = None,
        jvlinktosqlite_path: str | None = None,
        config_path: str | None = None
    ):
        """初期化"""
```

**テスト**:
- デフォルト設定での初期化（正常系）
- カスタム設定での初期化（正常系）
- JVLinkToSQLiteArtifact_0.1.0.0.exeが存在しない（準正常系）

**レビューポイント**:
- クラス設計が適切か
- 設定の優先順位（引数 > 設定ファイル > デフォルト）が正しいか

---

#### PR#2-2: JVLinkDBManager - 初期生成機能

**目的**: データベース初期生成機能の実装

**作業内容**:
- `initialize_database()`メソッド実装
- JVLinkToSQLiteのサブプロセス実行
- setting.xml生成・編集機能
- `test/unit/manager/test_initialize_database.py`: 単体テスト

**実装内容**:
```python
def initialize_database(
    self,
    start_date: str,
    end_date: str,
    data_specs: list[str] | None = None
) -> None:
    """初期データベース生成"""
```

**テスト**:
- 正常にデータベースが生成される（正常系・モック使用）
- 期間指定が正しく反映される（正常系）
- JVLinkToSQLite実行エラー（準正常系）
- 不正な日付形式（準正常系）

**レビューポイント**:
- setting.xmlの生成ロジックが正確か
- サブプロセス実行が安全か
- エラーハンドリングが適切か

---

#### PR#2-3: JVLinkDBManager - 更新機能

**目的**: データベース更新機能の実装

**作業内容**:
- `update_database()`メソッド実装
- 前回更新日時の管理
- `test/unit/manager/test_update_database.py`: 単体テスト

**実装内容**:
```python
def update_database(
    self,
    start_date: str | None = None,
    end_date: str | None = None,
    realtime_only: bool = False
) -> None:
    """データベース更新"""
```

**テスト**:
- 通常更新（前回更新日時以降）（正常系・モック使用）
- 期間指定更新（正常系）
- 速報系のみ更新（正常系）
- 更新中のエラー（準正常系）

**レビューポイント**:
- 前回更新日時の記録・取得ロジック
- 更新範囲の決定ロジック
- エラー時のロールバック考慮

---

### Phase 3: データ取得API

#### PR#3-1: JVLinkDataFetcher - 基本構造とレース情報取得

**目的**: データ取得クラスの基本構造とレース情報取得機能

**作業内容**:
- `jvlink_db_python/fetcher.py`: JVLinkDataFetcherクラス定義
- `get_race_info()`メソッド実装
- `test/unit/fetcher/conftest.py`: テスト用fixture
- `test/unit/fetcher/test_get_race_info.py`: 単体テスト

**実装内容**:
```python
class JVLinkDataFetcher:
    def __init__(self, db_path: str | None = None):
        """初期化"""

    def get_race_info(
        self,
        race_id: str | None = None,
        date_id: str | None = None,
        year: str | None = None,
        month_day: str | None = None,
        jyo_cd: str | None = None,
        kaiji: str | None = None,
        nichiji: str | None = None,
        race_num: str | None = None
    ) -> pd.DataFrame:
        """レース情報取得"""
```

**テスト**:
- race_id + date_idで取得（正常系）
- 各要素を個別指定で取得（正常系）
- データベースが存在しない（準正常系）
- 該当レースが存在しない（準正常系）
- パラメータ不足（準正常系）

**レビューポイント**:
- SQLクエリが正確か
- pandas DataFrameの列名が適切か
- ID変換ロジックが正しく使用されているか

---

#### PR#3-2: JVLinkDataFetcher - 出走馬情報取得

**目的**: 出走馬情報取得機能の実装

**作業内容**:
- `get_race_horses()`メソッド実装
- `test/unit/fetcher/test_get_race_horses.py`: 単体テスト

**実装内容**:
```python
def get_race_horses(
    self,
    race_id: str | None = None,
    date_id: str | None = None,
    year: str | None = None,
    month_day: str | None = None,
    jyo_cd: str | None = None,
    kaiji: str | None = None,
    nichiji: str | None = None,
    race_num: str | None = None,
    include_results: bool = False
) -> pd.DataFrame:
    """出走馬情報取得"""
```

**テスト**:
- 基本情報のみ取得（正常系）
- 結果を含めて取得（正常系）
- 該当データなし（準正常系）

**レビューポイント**:
- NL_SE_RACE_UMAテーブルの適切な列選択
- 結果データ（確定着順、タイム等）の条件分岐

---

#### PR#3-3: JVLinkDataFetcher - 馬情報取得

**目的**: 馬の基本情報と戦績取得機能

**作業内容**:
- `get_horse_info()`メソッド実装
- `get_horse_race_history()`メソッド実装
- `test/unit/fetcher/test_get_horse_info.py`: 単体テスト

**実装内容**:
```python
def get_horse_info(self, horse_id: str) -> pd.DataFrame:
    """馬基本情報取得"""

def get_horse_race_history(
    self,
    horse_id: str,
    limit: int | None = None
) -> pd.DataFrame:
    """馬の戦績（過去レース）取得"""
```

**テスト**:
- 馬基本情報取得（正常系）
- 過去レース取得（正常系）
- 件数制限（正常系）
- 存在しないhorse_id（準正常系）

**レビューポイント**:
- NL_UM_UMAテーブルとの結合ロジック
- horse_id（netkeiba）とKettoNum（JV-Link）のマッピング
- 過去レースのソート順（新しい順）

---

#### PR#3-4: JVLinkDataFetcher - マスタ情報取得

**目的**: 騎手、厩舎、馬主、生産者の情報取得

**作業内容**:
- `get_jockey_info()`メソッド実装
- `get_trainer_info()`メソッド実装
- `get_owner_info()`メソッド実装
- `get_breeder_info()`メソッド実装
- 各テストファイル作成

**実装内容**:
```python
def get_jockey_info(self, jockey_id: str) -> pd.DataFrame:
    """騎手情報取得"""

def get_trainer_info(self, trainer_id: str) -> pd.DataFrame:
    """厩舎情報取得"""

def get_owner_info(self, owner_id: str) -> pd.DataFrame:
    """馬主情報取得"""

def get_breeder_info(self, breeder_id: str) -> pd.DataFrame:
    """生産者情報取得"""
```

**テスト**:
- 各マスタ情報の取得（正常系）
- 存在しないID（準正常系）

**レビューポイント**:
- 各マスタテーブル（NL_KS_KISYU, NL_CH_CHOKYOSI等）の正しい参照
- ID形式の検証

---

#### PR#3-5: JVLinkDataFetcher - 開催一覧取得

**目的**: レーススケジュール取得機能

**作業内容**:
- `get_race_schedule()`メソッド実装
- `test/unit/fetcher/test_get_race_schedule.py`: 単体テスト

**実装内容**:
```python
def get_race_schedule(
    self,
    start_date: str | None = None,
    end_date: str | None = None,
    date: str | None = None
) -> pd.DataFrame:
    """開催一覧取得"""
```

**テスト**:
- 期間指定取得（正常系）
- 特定日取得（正常系）
- 不正な日付形式（準正常系）

**レビューポイント**:
- NL_YS_SCHEDULEとNL_RA_RACEの結合ロジック
- race_idとdate_idの生成ロジック

---

#### PR#3-6: JVLinkDataFetcher - 払戻・オッズ取得

**目的**: 払戻情報とオッズ情報の取得機能

**作業内容**:
- `get_payback()`メソッド実装
- `get_odds_tanfuku()`メソッド実装
- その他オッズ取得メソッド（umaren, umatan, wide等）実装
- 各テストファイル作成

**実装内容**:
```python
def get_payback(
    self,
    race_id: str | None = None,
    date_id: str | None = None,
    **kwargs
) -> pd.DataFrame:
    """払戻情報取得"""

def get_odds_tanfuku(
    self,
    race_id: str | None = None,
    date_id: str | None = None,
    **kwargs
) -> pd.DataFrame:
    """単勝・複勝オッズ取得"""

# その他のオッズ取得メソッド
```

**テスト**:
- 払戻情報取得（正常系）
- 各券種のオッズ取得（正常系）
- レース前（オッズなし）（準正常系）

**レビューポイント**:
- NL_HR_PAY, NL_O1_ODDS_TANFUKUWAKU等の正しい参照
- オッズデータのフォーマット

---

### Phase 4: 結合テストとドキュメント

#### PR#4-1: 結合テスト - データベース初期化と更新

**目的**: データベース初期化・更新の結合テスト

**作業内容**:
- `test/integration/test_database_init_normal.py`: 初期化テスト
- `test/integration/test_database_update_normal.py`: 更新テスト

**テスト内容**:
- 実際のJVLinkToSQLiteを使用したデータベース生成（正常系）
- データベース更新の動作確認（正常系）
- 生成されたデータの検証

**レビューポイント**:
- 実データでの動作確認
- テストデータの準備方法
- テスト時間（長時間テストの扱い）

---

#### PR#4-2: 結合テスト - データ取得ワークフロー

**目的**: データ取得APIの結合テスト

**作業内容**:
- `test/integration/test_race_data_fetch_normal.py`: データ取得テスト
- `test/integration/test_full_workflow_normal.py`: 全体ワークフローテスト

**テスト内容**:
- 実際のrace.dbを使用した各種データ取得（正常系）
- 複数のAPIを組み合わせた実際のユースケース（正常系）

**レビューポイント**:
- 実データでの動作確認
- APIの組み合わせ時の整合性

---

#### PR#4-3: ドキュメントと使用例

**目的**: ユーザー向けドキュメントの整備

**作業内容**:
- README.mdの充実
- `doc/examples/`に使用例を作成
  - `basic_usage.py`: 基本的な使い方
  - `race_data_fetch.py`: レースデータ取得例
  - `update_database.py`: データベース更新例
- インストール手順の記載

**レビューポイント**:
- ドキュメントが初心者にもわかりやすいか
- 使用例が実用的か
- トラブルシューティング情報の有無

---

### Phase 5: 追加機能・最適化（オプション）

#### PR#5-1: キャッシュ機構

**目的**: 頻繁にアクセスされるマスタデータのキャッシュ

**作業内容**:
- メモリキャッシュの実装（lru_cache等）
- キャッシュクリア機能
- テスト

---

#### PR#5-2: 非同期API

**目的**: async/await対応

**作業内容**:
- 非同期版のデータ取得API実装
- テスト

---

#### PR#5-3: データ検証機能

**目的**: 取得データの整合性チェック

**作業内容**:
- データバリデーション機能
- テスト

---

## 5. テスト戦略

### 5.1 単体テスト

**ルール**:
- `KeibaAI/.github/skills/pytest-coding-rule/SKILL.md`に従う
- 各関数・メソッドごとにテストファイルを分割
- 正常系、準正常系、異常系に分けて記述
- カバレッジ80%以上を目標

**テストケース設計**:
- **正常系**: 想定内の入力で正しい出力が得られることを確認
- **準正常系**: 不正な入力に対して適切な例外が発生することを確認
- **異常系**: 想定外の状況でも安定動作することを確認

**モックの使用**:
- JVLinkToSQLiteの実行は原則モック化
- SQLiteデータベースはテスト用のインメモリDBまたはテンポラリファイルを使用
- 外部ファイルアクセスは可能な限りモック化

### 5.2 結合テスト

**ルール**:
- 実際のrace.dbを使用（テスト用のサンプルDBを準備）
- JVLinkToSQLiteの実行を含む（CIでは条件付きスキップ可）
- エンドツーエンドのワークフローを確認

**テストケース**:
- データベース初期化 → データ取得の一連の流れ
- データベース更新 → 更新されたデータの取得
- 複数のAPI呼び出しを組み合わせた実用的なシナリオ

### 5.3 テストデータ

**準備**:
- 最小限のrace.db（数レース分）をテスト用に作成
- `test/fixtures/`ディレクトリに配置
- 機密情報を含まないダミーデータを使用

### 5.4 CI/CD

**GitHub Actions設定**:
- 単体テスト: 全PR・コミットで実行
- 結合テスト: mainブランチへのマージ時に実行（JVLinkToSQLite実行は条件付きスキップ）
- カバレッジレポート生成

## 6. コード品質管理

### 6.1 コーディング規約

- PEP8準拠
- `KeibaAI/doc/コーディング規約.md`に従う
- docstring: Google Style
- 型アノテーション必須
- 不必要にclassを使用しないこと
  - メンバ変数を持たないclassはclassである意味がないので、通常の関数にするかメンバ変数を持たせる設計に変更すること。
  - コンストラクタで何も処理しないclassも意味がないので設計変更すること。

### 6.2 ツール

- black: フォーマッタ
- isort: import整形
- flake8: リンタ
- mypy: 静的型チェック

### 6.3 pre-commitフック

`.pre-commit-config.yaml`を設定し、コミット前に自動チェック

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        args: [--line-length=100]
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: [--profile=black, --line-length=100]
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
        args: [--max-line-length=100, --ignore=E203,W503,...]
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

## 7. レビュー基準

### 7.1 必須チェック項目

- [ ] docstringが全ての関数・クラス・モジュールに記載されているか
- [ ] 型アノテーションが全ての関数引数・返り値に記載されているか
- [ ] テストカバレッジが80%以上か
- [ ] 全テストがパスしているか
- [ ] コード品質チェック（black, isort, flake8, mypy）をパスしているか
- [ ] 機能が仕様書通りに実装されているか

### 7.2 推奨チェック項目

- [ ] エラーハンドリングが適切か
- [ ] パフォーマンスが許容範囲か
- [ ] セキュリティ上の問題がないか
- [ ] 可読性・保守性が高いか

## 8. リスクと対応

### 8.1 ID不一致リスク

**リスク**: netkeibaのhorse_id等とJV-LinkのKettoNum等が完全に一致しない可能性

**対応**:
- 初期は文字列一致で実装
- 不一致が判明した場合は馬名・生年月日での突合ロジックを追加

### 8.2 芝コース情報不足

**リスク**: 「Aコース4日目」等の情報がJV-Linkから取得できない可能性

**対応**:
- NL_CS_COURSEテーブルを調査
- 取得不可の場合は独自計算ロジックを実装

### 8.3 JVLinkToSQLite依存

**リスク**: JVLinkToSQLiteのバージョンアップや仕様変更で動作しなくなる可能性

**対応**:
- サブモジュールのバージョンを固定
- テストで動作確認を徹底
- 将来的にはJV-Link直接操作も検討

### 8.4 Windows環境依存

**リスク**: WindowsのみでしかJV-Linkが動作しない

**対応**:
- 現時点ではWindows専用として設計
- 将来的にはLinux/MacでのDB操作のみ対応を検討

## 10. 完了定義

各PRは以下の条件を満たした場合に完了とする:

- [ ] 実装が完了している
- [ ] 単体テストが全てパスしている
- [ ] テストカバレッジが80%以上である
- [ ] コード品質チェック（black, isort, flake8, mypy）をパスしている
- [ ] docstringとコメントが適切に記載されている
- [ ] レビューが完了している
- [ ] mainブランチにマージされている

プロジェクト全体は以下の条件を満たした場合に完了とする:

- [ ] 全てのPRが完了している
- [ ] 結合テストが全てパスしている
- [ ] README.mdとドキュメントが整備されている
- [ ] 使用例が動作確認されている
- [ ] 既知の問題がIssueとして記録されている
