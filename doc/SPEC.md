# jvlink-db-python 機能仕様書

## 1. 概要

### 1.1 目的

JRA-VANが提供するJV-Linkサービスから取得した競馬データをSQLiteデータベース経由でPythonから利用可能にする汎用的なライブラリ。netkeibaのスクレイピングに依存しない安定的なデータ取得基盤を提供する。

### 1.2 スコープ

- JVLinkToSQLiteを活用したデータベースの初期生成・更新機能
- race.dbからのデータ取得APIの提供
- KeibaAIに依存しない汎用的なライブラリとして設計
- JVLinkToSQLiteとJVLinkToSQLite.wikiをサブモジュールとして管理

### 1.3 対象外

- JV-Linkの直接操作（JVLinkToSQLiteに委譲）
- データ分析・AI機能（KeibaAI側で実装）
- WebスクレイピングAPIとの互換性維持（段階的移行を想定）

## 2. ID体系とマッピング

### 2.1 netkeiba ID（既存）

| ID名 | 形式 | 例 | 説明 |
|------|------|-----|------|
| race_id | YYYYKKNNTTRR | 202506010101 | 年+競馬場ID(2)+回(2)+日目(2)+レース番号(2) |
| date_id | YYYYMMDDKKRR | 202501050601 | 年+月+日+競馬場ID(2)+レース番号(2) |
| horse_id | YYYY1XXXXX | 202210XXXX | 生まれ年+10(日本馬)/19(外国馬)+番号 |
| keibajo_id | KK | 01～10 | 01:札幌, 02:函館, ..., 10:小倉 |
| jockey_id | XXXXX | 00666 | 騎手ID（5桁） |
| trainer_id | XXXXX | 01075 | 厩舎ID（5桁） |
| owner_id | XXXXX | 12345 | 馬主ID（5桁） |
| breeder_id | XXXXXX | 123456 | 生産者ID（6桁） |

### 2.2 JV-Link ID（JVLinkToSQLite）

| テーブル | 主キー | 形式 | netkeiba対応 |
|----------|--------|------|-------------|
| NL_RA_RACE | idYear, idMonthDay, idJyoCD, idKaiji, idNichiji, idRaceNum | 2026, 0105, 06, 01, 02, 12 | ○（変換可能） |
| NL_SE_RACE_UMA | 上記+Umaban | 上記+01～18 | ○（変換可能） |
| NL_UM_UMA | KettoNum | 202210XXXXX | △（一部対応） |
| NL_KS_KISYU | KisyuCode | 05桁 | 調査必要 |
| NL_CH_CHOKYOSI | ChokyosiCode | 05桁 | 調査必要 |
| NL_BN_BANUSI | BanusiCode | 05桁 | 調査必要 |
| NL_BR_BREEDER | BreederCode | 06桁 | 調査必要 |

### 2.3 ID変換仕様

#### 2.3.1 race_id → JV-Link

```
race_id: 202506010101 (YYYYKKNNTTRR)
↓
idYear: 2025
idMonthDay: 月日はレース開催日から取得が必要（race_idには含まれない）
idJyoCD: 06
idKaiji: 01
idNichiji: 01
idRaceNum: 01
```

**課題**: race_idには月日情報が含まれないため、date_idまたは別途開催日情報が必要

#### 2.3.2 date_id → JV-Link

```
date_id: 202501050601 (YYYYMMDDKKRR)
↓
idYear: 2025
idMonthDay: 0105
idJyoCD: 06
idRaceNum: 01
```

**課題**: idKaiji（開催回）とidNichiji（日目）の情報が欠落

#### 2.3.3 推奨アプローチ

- **race_id + date_id併用**: 最も確実
- または**date_idからNL_YS_SCHEDULEテーブル参照**: 開催回・日目を逆引き

### 2.4 馬ID（horse_id）のマッピング

JV-LinkのKettoNum（血統登録番号）はnetkeibaのhorse_idと**形式が類似**しているが、**完全一致は未検証**。

```
netkeiba horse_id: 2022103707
JV-Link KettoNum:  202210XXXXX
                   ^^^^-- 生年(西暦)4桁
                       ^-- 品種1桁（1:サラ、9:外国産）
                        XXXXX-- 数字5桁
```

**検証事項**:
- netkeibaの10/19がJV-Linkの品種コード1/9に対応するか
- 末尾5桁が一致するか

**対応方針**:
- 初期は文字列一致で検索
- 不一致の場合は馬名・生年月日での突合ロジックを追加

## 3. データベース構造

### 3.1 race.db（JVLinkToSQLiteが生成）

#### 3.1.1 主要テーブル

| テーブル名 | 説明 | 主な用途 |
|-----------|------|----------|
| NL_RA_RACE | レース詳細（蓄積系） | レース基本情報、条件、賞金 |
| RT_RA_RACE | レース詳細（速報系） | リアルタイムレース情報 |
| NL_SE_RACE_UMA | 馬毎レース情報（蓄積系） | 出走馬、枠番、騎手、オッズ、結果 |
| RT_SE_RACE_UMA | 馬毎レース情報（速報系） | リアルタイム出走馬情報 |
| NL_UM_UMA | 競走馬マスタ | 馬の基本情報、血統、成績 |
| NL_KS_KISYU | 騎手マスタ | 騎手情報 |
| NL_CH_CHOKYOSI | 調教師マスタ | 調教師情報 |
| NL_BN_BANUSI | 馬主マスタ | 馬主情報 |
| NL_BR_BREEDER | 生産者マスタ | 生産者情報 |
| NL_YS_SCHEDULE | 年間スケジュール | 開催日程 |
| NL_HR_PAY | 払戻情報 | 配当金額 |
| RT_HR_PAY | 払戻情報（速報系） | リアルタイム配当 |
| NL_O1_ODDS_TANFUKUWAKU | 単勝・複勝・枠連オッズ | オッズ情報 |
| RT_O1_ODDS_TANFUKUWAKU | 単勝・複勝・枠連オッズ（速報系） | リアルタイムオッズ |
| RT_WH_BATAIJYU | 馬体重（速報系） | リアルタイム馬体重 |
| RT_WE_WEATHER | 天候（速報系） | リアルタイム天候情報 |
| RT_AV_INFO | 出走取消・競走除外（速報系） | 出走取消・競走除外情報 |
| RT_JC_INFO | 騎手変更（速報系） | 騎手変更情報 |
| RT_TC_INFO | 発走時刻変更（速報系） | 発走時刻変更情報 |
| RT_CC_INFO | コース変更（速報系） | コース変更情報 |
| NL_CS_COURSE | コース情報 | 芝コース使用日数等 |
| SY_PROC_FILES | 処理済みファイル管理 | 更新管理用 |

#### 3.1.2 芝コース情報の取得

**懸念事項**: race_info{yyyy}.csvには「Aコース4日目」などの情報があるが、JV-Linkでの取得方法を調査する必要がある。

**候補**:
- NL_CS_COURSEテーブル: コース情報
- NL_RA_RACEのコース区分フィールド: "A "～"E "

### 3.2 既存データとの対応

| 既存ファイル | JV-Linkテーブル | 備考 |
|-------------|----------------|------|
| Result{race_id}.csv | NL_SE_RACE_UMA | 出走馬情報 |
| race_info{yyyy}.csv | NL_RA_RACE + NL_CS_COURSE | レース基本+コース |
| Corner{race_id}.csv | NL_RA_RACEのコーナー通過順位フィールド | JSON形式で格納 |
| PayBack{race_id}.csv | NL_HR_PAY | 払戻情報 |
| Rap{race_id}.csv | NL_RA_RACEのラップタイムフィールド | カンマ区切り文字列 |
| HorseID{yyyy}.csv | NL_UM_UMA | 馬基本情報 |
| Umabashira{horse_id}.csv | NL_SE_RACE_UMA（過去出走履歴） | 馬IDで絞り込み |
| today_race{yyyymmdd}.csv | NL_YS_SCHEDULE | 開催日程 |
| RaceCalender{yyyy}.csv | NL_YS_SCHEDULE | 年間スケジュール |

## 4. 機能仕様

### 4.1 データベース管理

#### 4.1.1 初期生成機能

**機能**: 指定期間のrace.dbを初期生成する

**実装方針**:
- JVLinkToSQLite.exeをサブプロセスで実行
- 設定ファイル（setting.xml）の生成・編集機能を提供
- 進捗表示機能

**インターフェース**:
```python
from jvlink_db_python import JVLinkDBManager

manager = JVLinkDBManager(
    db_path="race.db",
    jvlinktosqlite_path="path/to/jvlinktosqlite.exe"
)

# 初期データベース生成
manager.initialize_database(
    start_date="2023-01-01",
    end_date="2024-12-31",
    data_specs=["RA", "SE", "UM", "KS", "CH", "BN", "BR", "YS", "HR", "O1"]
)
```

#### 4.1.2 更新機能

**機能**: 最新のレース結果・オッズを取得してrace.dbに反映

**更新対象**:
- 速報系データ（RT_*テーブル）
- レース結果確定
- オッズ更新
- 払戻情報

**インターフェース**:
```python
# 通常更新（前回更新日時以降）
manager.update_database()

# 期間指定更新
manager.update_database(
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# 速報系のみ更新
manager.update_database(realtime_only=True)
```

### 4.2 データ取得API

#### 4.2.1 レース情報取得

**機能**: race_idまたはdate_idを指定してレース情報を取得

**インターフェース**:
```python
from jvlink_db_python import JVLinkDataFetcher

fetcher = JVLinkDataFetcher(db_path="race.db")

# race_idで取得（date_idも必要）
race_info_df = fetcher.get_race_info(
    race_id="202506010101",
    date="20250105"  # 月日情報を補完
)

# または各要素を指定
race_info_df = fetcher.get_race_info(
    year="2025",
    month_day="0105",
    jyo_cd="06",
    kaiji="01",
    nichiji="01",
    race_num="01"
)
```

**返り値**: pandas.DataFrame
```
列: レース名, 発走時間, 芝ダ, 距離, コース, 天候, 馬場状態,
    グレード, 条件, 本賞金, 登録頭数, 出走頭数, ラップタイム,
    コーナー通過順位, 芝コース, 芝コース日目 等
```

#### 4.2.2 出走馬情報取得

**機能**: 指定レースの出走馬データを取得

**インターフェース**:
```python
# 出走馬一覧
horses_df = fetcher.get_race_horses(
    race_id="202506010101",
    date="20250105"  # 月日情報を補完
)

# 結果を含む出走馬情報
horses_df = fetcher.get_race_horses(
    race_id="202506010101",
    date="20250105"  # 月日情報を補完
    include_results=True  # 着順、タイム等を含む
)
```

**返り値**: pandas.DataFrame
```
列: 枠番, 馬番, 馬名, 性齢, 斤量, 騎手, 厩舎, 馬主,
    単勝オッズ, 人気, 馬体重, 増減, 馬ID, 騎手ID, 厩舎ID,
    [確定着順, タイム, 着差, 後3F] (include_results=True時)
```

#### 4.2.3 馬情報取得

**機能**: horse_idを指定して馬の基本情報・戦績を取得

**インターフェース**:
```python
# 馬基本情報
horse_info_df = fetcher.get_horse_info(horse_id="2022103707")

# 馬の戦績（過去レース）
horse_history_df = fetcher.get_horse_race_history(
    horse_id="2022103707",
    limit=20  # 最新20レース
)
```

**返り値**:
- `get_horse_info`: 馬名, 性別, 生年月日, 毛色, 父, 母, 母父, 厩舎, 馬主, 生産者, 本賞金累計, 着回数 等
- `get_horse_race_history`: 過去レース一覧（日付, 競馬場, レース名, 着順, タイム, 騎手 等）

#### 4.2.4 騎手情報取得

**機能**: jockey_idを指定して騎手情報を取得

**インターフェース**:
```python
jockey_info_df = fetcher.get_jockey_info(jockey_id="00666")  # 武豊
```

**返り値**: 騎手名, 所属, 生年月日, 初免許年度 等

#### 4.2.5 厩舎情報取得

**機能**: trainer_idを指定して厩舎（調教師）情報を取得

**インターフェース**:
```python
trainer_info_df = fetcher.get_trainer_info(trainer_id="01075")
```

**返り値**: 調教師名, 所属, 生年月日, 初免許年度 等

#### 4.2.6 馬主情報取得

**機能**: owner_idを指定して馬主情報を取得

**インターフェース**:
```python
owner_info_df = fetcher.get_owner_info(owner_id="506800")
```

**返り値**: 馬主名, 馬主名欧字 等

#### 4.2.7 生産者情報取得

**機能**: breeder_idを指定して生産者情報を取得

**インターフェース**:
```python
breeder_info_df = fetcher.get_breeder_info(breeder_id="373126")
```

**返り値**: 生産者名, 生産者名欧字 等

#### 4.2.8 開催一覧取得

**機能**: 期間を指定して開催一覧を取得

**インターフェース**:
```python
# 期間指定
schedule_df = fetcher.get_race_schedule(
    start_date="2025-01-01",
    end_date="2025-01-31"
)

# 特定日
schedule_df = fetcher.get_race_schedule(date="2025-01-05")
```

**返り値**: pandas.DataFrame
```
列: 日付, 競馬場, 回, 日目, レース番号, レース名, 発走時刻,
    距離, トラック, グレード, 登録頭数, race_id, date_id
```

DailySchedule相当の情報とRaceCalender相当の情報をマージして返す。

#### 4.2.9 払戻情報取得

**機能**: 指定レースの払戻（配当）情報を取得

**インターフェース**:
```python
payback_df = fetcher.get_payback(
    race_id="202506010101",
    date="20250105"  # 月日情報を補完
)
```

**返り値**: pandas.DataFrame
```
列: 券種, 馬番組み合わせ, 配当金額, 人気
```

#### 4.2.10 オッズ情報取得

**機能**: 指定レースのオッズ情報を取得

**インターフェース**:
```python
# 単勝・複勝オッズ
odds_df = fetcher.get_odds_tanfuku(
    race_id="202506010101",
    date="20250105"
)

# 馬連オッズ
odds_df = fetcher.get_odds_umaren(
    race_id="202506010101",
    date="20250105"
)

# その他の券種も同様
```

### 4.3 ユーティリティ機能

#### 4.3.1 ID変換ユーティリティ

**機能**: 各種IDフォーマット間の変換

**インターフェース**:
```python
from jvlink_db_python.utils import race_id_to_jvlink, date_id_to_race_id, jvlink_to_race_id

# race_id → JV-Link形式
jvlink_params = race_id_to_jvlink("202506010101", "20250105")
# → {"year": "2025", "month_day": "0105", "jyo_cd": "06", ...}

# date_id → race_id
race_id = date_id_to_race_id("202501050601", kaiji="01", nichiji="01")
# → "202506010101"

# JV-Link形式 → race_id
race_id = jvlink_to_race_id(year="2025", jyo_cd="06", kaiji="01", ...)
```

#### 4.3.2 コード変換ユーティリティ

**機能**: JV-Linkのコード値を人間が読める文字列に変換

**インターフェース**:
```python
from jvlink_db_python.utils import jyo_code_to_name, sex_code_to_str, track_code_to_str, grade_code_to_str

# 競馬場コード
jyo_name = jyo_code_to_name("06")  # → "中山"

# 性別コード
sex = sex_code_to_str("1")  # → "牡"

# トラックコード
track = track_code_to_str("10")  # → "芝"

# グレードコード
grade = grade_code_to_str("A")  # → "G1"
```

## 5. エラーハンドリング

### 5.1 例外クラス

```python
class JVLinkDBError(Exception):
    """jvlink-db-python基底例外"""

class DatabaseNotFoundError(JVLinkDBError):
    """データベースファイルが見つからない"""

class JVLinkToSQLiteError(JVLinkDBError):
    """JVLinkToSQLite実行エラー"""

class DataNotFoundError(JVLinkDBError):
    """指定されたデータが見つからない"""

class IDConversionError(JVLinkDBError):
    """ID変換エラー"""
```

## 6. 設定ファイル

### 6.1 設定項目

```yaml
# config.yml
database:
  path: "./race.db"
  backup_dir: "./backup/"  # オプション

jvlinktosqlite:
  path: "./JVLinkToSQLiteArtifact_0.1.0.0.exe"
  setting_xml: "./setting.xml"
  throttle_size: 100  # オプション
  log_level: "Info"  # オプション（Trace, Debug, Info, Warn, Error, Fatal）

data_specs:
  # 取得するデータ種別（JVLinkToSQLite Data Spec記号）
  # 詳細はJVLinkToSQLite.wiki/Table-Spec.md
  # 対応テーブル: NL_{レコード種別ID}_* (例: RA → NL_RA_{サフィックス})
  # 注意: 1つのレコード種別IDが複数テーブルを生成する場合があります
  default:
    # コース情報
    - CS    # コース情報（NL_CS_COURSE）

    # レース情報
    - YS    # 年間スケジュール（NL_YS_SCHEDULE）
    - RA    # レース詳細（NL_RA_RACE）

    # 馬情報
    - TK    # 特別登録馬（NL_TK_TOKUUMA + NL_TK_TokuUmaInfo）
    - SE    # 馬毎レース情報（NL_SE_RACE_UMA）
    - HS    # 競走馬市場取引価格（NL_HS_SALE）
    - HY    # 馬名の意味由来（NL_HY_BAMEIORIGIN）
    - HN    # 繁殖馬マスタ（NL_HN_HANSYOKU）
    - SK    # 産駒マスタ（NL_SK_SANKU）
    - BT    # 系統情報（NL_BT_KEITO）

    # オッズ情報
    - HR    # 払戻情報（NL_HR_PAY）
    - H1    # 票数全掛（NL_H1_HYOSU_ZENKAKE + NL_H1_Hyo*系列）
    - H6    # 票数三連単（NL_H6_HYOSU_SANRENTAN + NL_H6_HyoSanrentan）
    - O1    # 単勝・複勝・枠連オッズ（NL_O1_ODDS_TANFUKUWAKU）
    - O2    # 馬連オッズ（NL_O2_ODDS_UMAREN）
    - O3    # ワイドオッズ（NL_O3_ODDS_WIDE）
    - O4    # 馬単オッズ（NL_O4_ODDS_UMATAN）
    - O5    # 三連複オッズ（NL_O5_ODDS_SANREN + NL_O5_OddsSanrenInfo）
    - O6    # 三連単オッズ（NL_O6_ODDS_SANRENTAN + NL_O6_OddsSanrentanInfo）
    - WF    # 重勝式(WIN5)（NL_WF_INFO）

    # マスタ情報
    - JG    # 競走馬除外情報（NL_JG_JOGAIBA）
    - UM    # 競走馬マスタ（NL_UM_UMA）
    - KS    # 騎手マスタ（NL_KS_KISYU）
    - CH    # 調教師マスタ（NL_CH_CHOKYOSI）
    - BR    # 生産者マスタ（NL_BR_BREEDER）
    - BN    # 馬主マスタ（NL_BN_BANUSI）
    - RC    # レコードマスタ（NL_RC_RECORD）
    - CK    # 出走別着度数（NL_CK_CHAKU + NL_CK_*Chaku系列）

    # 調教情報
    - HC    # 坂路調教（NL_HC_HANRO）
    - WC    # ウッドチップ調教（NL_WC_WOOD）

    # TARGET独自指数
    - DM    # タイム型データマイニング予想（NL_DM_INFO）
    - TM    # 対戦型データマイニング予想（NL_TM_INFO）

update:
  auto_update: false  # オプション
  update_interval_minutes: 15  # オプション
  # 速報系データ種別（RT_プレフィックス）
  # 詳細はJVLinkToSQLite.wiki/Table-Spec.md
  # 対応テーブル: RT_{レコード種別ID}_* (例: RA → RT_RA_{サフィックス})
  realtime:
    # レース情報
    - RA  # 速報レース詳細（RT_RA_RACE）
    - SE  # 速報馬毎レース情報（出馬表）（RT_SE_RACE_UMA）

    # オッズ
    - HR  # 速報払戻（RT_HR_PAY）
    - O1  # 速報単勝・複勝・枠連オッズ（RT_O1_ODDS_TANFUKUWAKU）
    - O2  # 速報馬連オッズ（RT_O2_ODDS_UMAREN）
    - O3  # 速報ワイドオッズ（RT_O3_ODDS_WIDE）
    - O4  # 速報馬単オッズ（RT_O4_ODDS_UMATAN）
    - O5  # 速報三連複オッズ（RT_O5_ODDS_SANREN + RT_O5_OddsSanrenInfo）
    - O6  # 速報三連単オッズ（RT_O6_ODDS_SANRENTAN + RT_O6_OddsSanrentanInfo）
    - H1  # 速報票数全掛（RT_H1_HYOSU_ZENKAKE + RT_H1_Hyo*系列）
    - H6  # 速報票数三連単（RT_H6_HYOSU_SANRENTAN + RT_H6_HyoSanrentan）
    - WF  # 速報重勝式(WIN5)（RT_WF_INFO）

    # レース変更情報
    - WH  # 速報馬体重（RT_WH_BATAIJYU）
    - WE  # 天候馬場状態（RT_WE_WEATHER）
    - AV  # 速報出走取消・競走除外（RT_AV_INFO）
    - JC  # 速報騎手変更（RT_JC_INFO）
    - TC  # 速報発走時刻変更（RT_TC_INFO）
    - CC  # 速報コース変更（RT_CC_INFO）

    # TARGET独自指数
    - DM  # 速報タイム型データマイニング予想（RT_DM_INFO）
    - TM  # 速報対戦型データマイニング予想（RT_TM_INFO）
```

## 7. パフォーマンス要件

- レース情報取得: 100ms以内（1レース）
- 出走馬情報取得: 200ms以内（1レース18頭）
- 馬戦績取得: 300ms以内（過去20レース）
- 開催一覧取得: 500ms以内（1ヶ月分）

## 8. 今後の拡張

### 8.1 キャッシュ機構

頻繁にアクセスされるマスタデータ（馬、騎手、調教師等）をメモリキャッシュする。

### 8.2 非同期API

async/awaitによる非同期データ取得APIの提供。

### 8.3 データ検証

取得データの整合性チェック機能。

### 8.4 差分更新の最適化

変更があったレコードのみを更新する効率的な更新機構。

## 9. テスト要件

- 単体テスト: カバレッジ80%以上
- 結合テスト: 主要なユースケースを網羅
- 実データを使った動作確認テスト

詳細は実装計画（PLAN.md）を参照。
