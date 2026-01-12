"""ID変換ユーティリティ

netkeiba IDとJV-Link ID間の相互変換機能を提供する。

ID体系:
    netkeiba:
        - race_id: YYYYKKNNTTRR (年+競馬場ID+回+日目+レース番号)
        - date_id: YYYYMMDDKKRR (年+月+日+競馬場ID+レース番号)
    JV-Link:
        - idYear: YYYY (年)
        - idMonthDay: MMDD (月日)
        - idJyoCD: KK (競馬場コード)
        - idKaiji: NN (開催回)
        - idNichiji: TT (日目)
        - idRaceNum: RR (レース番号)
"""

from jvlink_db_python.exceptions import IDConversionError


def race_id_to_jvlink(race_id: str, date_id: str) -> dict[str, str]:
    """race_idとdate_idをJV-Link形式に変換

    Args:
        race_id (str): netkeibaのrace_id (YYYYKKNNTTRR形式)
        date_id (str): netkeibaのdate_id (YYYYMMDDKKRR形式)

    Returns:
        dict[str, str]: JV-Linkパラメータの辞書
            - idYear: 年 (YYYY)
            - idMonthDay: 月日 (MMDD)
            - idJyoCD: 競馬場コード (KK)
            - idKaiji: 開催回 (NN)
            - idNichiji: 日目 (TT)
            - idRaceNum: レース番号 (RR)

    Raises:
        IDConversionError: IDフォーマットが不正な場合

    Examples:
        >>> race_id_to_jvlink("202506010101", "202501050601")
        {
            "idYear": "2025",
            "idMonthDay": "0105",
            "idJyoCD": "06",
            "idKaiji": "01",
            "idNichiji": "01",
            "idRaceNum": "01"
        }
    """
    # race_idの検証
    if not isinstance(race_id, str) or len(race_id) != 12:
        raise IDConversionError(f"race_idは12桁の文字列である必要があります: {race_id}")
    if not race_id.isdigit():
        raise IDConversionError(f"race_idは数字のみで構成される必要があります: {race_id}")

    # date_idの検証
    if not isinstance(date_id, str) or len(date_id) != 12:
        raise IDConversionError(f"date_idは12桁の文字列である必要があります: {date_id}")
    if not date_id.isdigit():
        raise IDConversionError(f"date_idは数字のみで構成される必要があります: {date_id}")

    # race_idのパース: YYYYKKNNTTRR
    year = race_id[0:4]
    jyo_cd = race_id[4:6]
    kaiji = race_id[6:8]
    nichiji = race_id[8:10]
    race_num = race_id[10:12]

    # date_idのパース: YYYYMMDDKKRR
    date_year = date_id[0:4]
    month_day = date_id[4:8]
    date_jyo_cd = date_id[8:10]
    date_race_num = date_id[10:12]

    # 整合性チェック
    if year != date_year:
        raise IDConversionError(
            f"race_idとdate_idの年が一致しません: race_id={race_id}, date_id={date_id}"
        )
    if jyo_cd != date_jyo_cd:
        raise IDConversionError(
            f"race_idとdate_idの競馬場コードが一致しません: race_id={race_id}, date_id={date_id}"
        )
    if race_num != date_race_num:
        raise IDConversionError(
            f"race_idとdate_idのレース番号が一致しません: race_id={race_id}, date_id={date_id}"
        )

    return {
        "idYear": year,
        "idMonthDay": month_day,
        "idJyoCD": jyo_cd,
        "idKaiji": kaiji,
        "idNichiji": nichiji,
        "idRaceNum": race_num,
    }


def date_id_to_race_id(date_id: str, kaiji: str | int, nichiji: str | int) -> str:
    """date_idと開催情報からrace_idを生成

    Args:
        date_id (str): netkeibaのdate_id (YYYYMMDDKKRR形式)
        kaiji (str | int): 開催回 (1-99)
        nichiji (str | int): 日目 (1-99)

    Returns:
        str: netkeibaのrace_id (YYYYKKNNTTRR形式)

    Raises:
        IDConversionError: IDフォーマットが不正な場合

    Examples:
        >>> date_id_to_race_id("202501050601", "01", "01")
        "202506010101"
        >>> date_id_to_race_id("202501050601", 1, 1)
        "202506010101"
    """
    # date_idの検証
    if not isinstance(date_id, str) or len(date_id) != 12:
        raise IDConversionError(f"date_idは12桁の文字列である必要があります: {date_id}")
    if not date_id.isdigit():
        raise IDConversionError(f"date_idは数字のみで構成される必要があります: {date_id}")

    # kaijiの検証と変換
    kaiji_str = _validate_and_convert_two_digit_number(kaiji, "kaiji", 1, 99)

    # nichijiの検証と変換
    nichiji_str = _validate_and_convert_two_digit_number(nichiji, "nichiji", 1, 99)

    # date_idのパース: YYYYMMDDKKRR
    year = date_id[0:4]
    jyo_cd = date_id[8:10]
    race_num = date_id[10:12]

    # race_idの生成: YYYYKKNNTTRR
    race_id = year + jyo_cd + kaiji_str + nichiji_str + race_num

    return race_id


def jvlink_to_race_id(
    year: str | int,
    jyo_cd: str,
    kaiji: str | int,
    nichiji: str | int,
    race_num: str | int,
) -> str:
    """JV-Linkパラメータからrace_idを生成

    Args:
        year (str | int): 年 (1000-9999)
        jyo_cd (str): 競馬場コード (KK形式、2桁)
        kaiji (str | int): 開催回 (1-99)
        nichiji (str | int): 日目 (1-99)
        race_num (str | int): レース番号 (1-12)

    Returns:
        str: netkeibaのrace_id (YYYYKKNNTTRR形式)

    Examples:
        >>> jvlink_to_race_id("2025", "06", "01", "01", "01")
        "202506010101"
        >>> jvlink_to_race_id(2025, "06", 1, 1, 1)
        "202506010101"
    """
    # yearの検証と変換
    year_str = _validate_and_convert_year(year)

    # jyo_cdの検証
    _validate_jyo_cd(jyo_cd)

    # kaijiの検証と変換
    kaiji_str = _validate_and_convert_two_digit_number(kaiji, "kaiji", 1, 99)

    # nichijiの検証と変換
    nichiji_str = _validate_and_convert_two_digit_number(nichiji, "nichiji", 1, 99)

    # race_numの検証と変換
    race_num_str = _validate_and_convert_two_digit_number(race_num, "race_num", 1, 12)

    # race_idの生成: YYYYKKNNTTRR
    race_id = year_str + jyo_cd + kaiji_str + nichiji_str + race_num_str

    return race_id


def jvlink_to_date_id(
    year: str | int,
    month: str | int,
    day: str | int,
    jyo_cd: str,
    race_num: str | int,
) -> str:
    """JV-Linkパラメータからdate_idを生成

    Args:
        year (str | int): 年 (1000-9999)
        month (str | int): 月 (1-12)
        day (str | int): 日 (1-31)
        jyo_cd (str): 競馬場コード (KK形式、2桁)
        race_num (str | int): レース番号 (1-12)

    Returns:
        str: netkeibaのdate_id (YYYYMMDDKKRR形式)

    Examples:
        >>> jvlink_to_date_id("2025", "01", "05", "06", "01")
        "202501050601"
        >>> jvlink_to_date_id(2025, 1, 5, "06", 1)
        "202501050601"
    """
    # yearの検証と変換
    year_str = _validate_and_convert_year(year)

    # monthの検証と変換
    month_str = _validate_and_convert_two_digit_number(month, "month", 1, 12)

    # dayの検証と変換
    day_str = _validate_and_convert_two_digit_number(day, "day", 1, 31)

    # jyo_cdの検証
    _validate_jyo_cd(jyo_cd)

    # race_numの検証と変換
    race_num_str = _validate_and_convert_two_digit_number(race_num, "race_num", 1, 12)

    # date_idの生成: YYYYMMDDKKRR
    date_id = year_str + month_str + day_str + jyo_cd + race_num_str

    return date_id


def _validate_and_convert_year(year: str | int) -> str:
    """年を検証して文字列に変換

    Args:
        year (str | int): 年 (1000-9999)

    Returns:
        str: 4桁の年文字列

    Raises:
        IDConversionError: yearが不正な場合
    """
    if year is None:
        raise IDConversionError("yearがNoneです")
    if isinstance(year, int):
        if not 1000 <= year <= 9999:
            raise IDConversionError(f"yearは1000-9999の範囲である必要があります: {year}")
        return str(year)
    else:
        if not isinstance(year, str) or len(year) != 4 or not year.isdigit():
            raise IDConversionError(f"yearは4桁の数字文字列である必要があります: {year}")
        return year


def _validate_and_convert_two_digit_number(
    value: str | int, name: str, min_val: int, max_val: int
) -> str:
    """2桁の数値を検証して文字列に変換

    Args:
        value (str | int): 検証する値
        name (str): パラメータ名（エラーメッセージ用）
        min_val (int): 最小値
        max_val (int): 最大値

    Returns:
        str: 2桁の数字文字列（ゼロパディング済み）

    Raises:
        IDConversionError: 値が不正な場合
    """
    if value is None:
        raise IDConversionError(f"{name}がNoneです")
    if isinstance(value, int):
        if not min_val <= value <= max_val:
            raise IDConversionError(
                f"{name}は{min_val}-{max_val}の範囲である必要があります: {value}"
            )
        return str(value).zfill(2)
    else:
        if not isinstance(value, str) or len(value) != 2 or not value.isdigit():
            raise IDConversionError(f"{name}は2桁の数字文字列である必要があります: {value}")
        return value


def _validate_jyo_cd(jyo_cd: str) -> None:
    """競馬場コードを検証

    Args:
        jyo_cd (str): 競馬場コード (KK形式、2桁)

    Raises:
        IDConversionError: jyo_cdが不正な場合
    """
    if not isinstance(jyo_cd, str) or len(jyo_cd) != 2:
        raise IDConversionError(f"jyo_cdは2桁の文字列である必要があります: {jyo_cd}")
    if not jyo_cd.isdigit():
        raise IDConversionError(f"jyo_cdは数字のみで構成される必要があります: {jyo_cd}")
