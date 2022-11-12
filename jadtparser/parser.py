""" This module which offers a parser for date format strings in Japanese.

"""

from abc import ABCMeta, abstractmethod
from collections import OrderedDict
from collections.abc import Iterable
from datetime import datetime, date
import dateutil.parser
import dateutil.tz
import re

# ********************
# constants
# ********************
_YEAR_PARTITIONS = ["年", "/", "／", "-", "－", "―"]
_MONTH_PARTITIONS = ["月", "/", "／", "-", "－", "―"]
_DAY_PARTITIONS = ["日", " "]
_HOUR_PARTITIONS = ["時", ":", "："]
_MINUTE_PARTITIONS = ["分", ":", "："]
_SECOND_PARTITIONS = ["秒", ":", "：", "."]
_MICROSECOND_PARTITIONS = ["秒", "マイクロ秒", ""]

# ********************
# private classes
# ********************
class _PatterntailSplitter(metaclass=ABCMeta):
    _PARSE_ERROR_MESSAGE = ""  # define in its subclass

    @classmethod
    @abstractmethod
    def split(cls, text: str) -> tuple[str, str]:
        raise NotImplementedError

    @classmethod
    def _split_pattern_and_tail(cls, text: str, pattern: str) -> tuple[str, str]:
        m = re.search(pattern, text)

        if m is None:
            raise ValueError(cls._PARSE_ERROR_MESSAGE.format(text=text))
        searched = m.group(0)
        tail = text[m.end():]

        return searched, tail


class _DigittailSplitter(_PatterntailSplitter):
    _PARSE_ERROR_MESSAGE = "Cannot split text: {text} into a digit and tail."

    @classmethod
    def split(cls, text: str) -> tuple[str, str]:
        pattern = r"[0-9]+"
        return cls._split_pattern_and_tail(text, pattern)


class _NondigittailSplitter(_PatterntailSplitter):
    _PARSE_ERROR_MESSAGE = "Cannot split text: {text} into a non-digit and tail."

    @classmethod
    def split(cls, text: str) -> tuple[str, str]:
        pattern = r"[^0-9]+"
        return cls._split_pattern_and_tail(text, pattern)


# ********************
# private functions
# ********************


def _parse(text: str) -> tuple[dict[str, str], dict[str, str]]:
    parsed_result = dict()
    partitions = dict()

    tail = text
    keys = [
        "year", "month", "day",
        "hour", "minute", "second", "microsecond"
    ]
    i = 0  # increment by splitting text
    while len(tail) > 0:
        digit, tail = _DigittailSplitter.split(tail)
        pt, tail = _NondigittailSplitter.split(tail)

        k = keys[i]
        if k not in parsed_result:
            parsed_result[k] = digit
            partitions[k] = pt

        i += 1

    # set empty value for remainder keys
    for k in keys:
        if k not in parsed_result:
            parsed_result[k] = ""
            partitions[k] = ""

    return parsed_result, partitions


def _infer_dateformat_ja_all(texts: Iterable[str]) -> list[str]:
    """Infer a date format for list-like object of date-format texts in Japanese style

    This method parse texts which start year.

    Args:
        texts (Iterable[str]): A date format text in Japanese style

    Returns:
        list[str]: A list of appeared date-formats

    Raises:
        ValueError: if invalid any date separators are given.

    """

    inferred_formats = list()
    for t in texts:
        fmt = infer_dateformat_ja(t)
        if fmt not in inferred_formats:
            inferred_formats.append(fmt)

    return inferred_formats


# ********************
# public functions
# ********************


def infer_dateformat_ja(text: str) -> str:
    """Infer a date format of a given text in Japanese style

    This method parse texts which start year.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        str: A Inferred Python date format

    Raises:
        ValueError: If invalid any date separators are given

    """

    parsed_result, partitions = _parse(text)

    allowance_partitions_map = OrderedDict({
        "year": _YEAR_PARTITIONS,
        "month": _MONTH_PARTITIONS,
        "day": _DAY_PARTITIONS,
        "hour": _HOUR_PARTITIONS,
        "minute": _MINUTE_PARTITIONS,
        "second": _SECOND_PARTITIONS,
        "microsecond": _MICROSECOND_PARTITIONS
    })

    # validate partitions
    num_invalid_partitions = 0
    for key, allowance_partitions in allowance_partitions_map.items():
        digit = parsed_result[key]
        pt = partitions[key]
        if digit:
            if not pt:
                num_invalid_partitions += 1
            elif pt not in allowance_partitions:
                num_invalid_partitions += 1

    if num_invalid_partitions > 0:
        raise ValueError(f"Cannot infer a format from the given text: {text}")

    # make format string
    inferred_format = ""
    if partitions["year"]:
        inferred_format += r"%Y" + partitions["year"]
    if partitions["month"]:
        inferred_format += r"%m" + partitions["month"]
    if partitions["day"]:
        inferred_format += r"%d" + partitions["day"]
    if partitions["hour"]:
        inferred_format += r"%H" + partitions["hour"]
    if partitions["minute"]:
        inferred_format += r"%M" + partitions["minute"]
    if partitions["second"]:
        inferred_format += r"%S" + partitions["second"]
    if partitions["microsecond"]:
        inferred_format += r"%f" + partitions["microsecond"]

    return inferred_format


def to_datetime(
    text: str | Iterable[str],
    with_tz: bool = False,
    tz_name: str = "Asia/Tokyo"
) -> datetime | list[datetime]:
    """Parse and convert a given text to a datetime object.

    * If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.
    * If missing month or day digits in a text, then assign 1 as thier value.

    Args:
        text (str): A date format text in Japanese style
        with_tz (bool): Whether or not append timezone from `tz_name` to datetime
        tz_name (str): Time zone name. This is valid if `with_tz` = True.

    Returns:
        datetime.datetime | list[datetime.datetime]: Parsed datetime objects

    Raises:
        ValueError: If extsts multi formats in given texts
        TypeError: If an invalid type arg is given

    """

    tz_obj = dateutil.tz.gettz(tz_name)
    out_obj: datetime | list[datetime]

    if isinstance(text, str):
        try:
            inferred_format = infer_dateformat_ja(text)
        except ValueError:
            inferred_format = None  # Imply not Japanese or invalid format

        if inferred_format is not None:
            dt_obj = datetime.strptime(text, inferred_format)
        else:
            dt_obj = dateutil.parser.parse(text)

        if with_tz:
            dt_obj = dt_obj.replace(tzinfo=tz_obj)

        out_obj = dt_obj

    elif isinstance(text, Iterable):
        inferred_format_list = list()
        try:
            inferred_format_list += _infer_dateformat_ja_all(text)
            if len(inferred_format_list) != 1:
                raise ValueError("Cannot infer ONE date-format")
            inferred_format = inferred_format_list[0]
        except ValueError:
            inferred_format = None   # Imply not Japanese or invalid forma

        out_obj = list()
        for t in text:
            if inferred_format is not None:
                dt_obj = datetime.strptime(t, inferred_format)
            else:
                dt_obj = dateutil.parser.parse(t)

            if with_tz:
                dt_obj = dt_obj.replace(tzinfo=tz_obj)

            out_obj.append(dt_obj)
    else:
        raise TypeError("Invalid type")

    return out_obj


def to_date(text: str) -> date:
    """Parse and convert a given text to a date object.

    * If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.
    * If missing month or day digits in a text, then assign 1 as thier value.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        datetime.date: A parsed date object

    """

    dt_obj = to_datetime(text)
    out_obj: datetime | list[datetime]

    if isinstance(dt_obj, datetime):
        out_obj = dt_obj.date()
    else:
        out_obj = list()
        for dt in dt_obj:
            out_obj.append(dt.date())

    return out_obj
