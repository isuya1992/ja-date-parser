""" This module which offers a parser for date format strings in Japanese.

"""

from abc import ABCMeta, abstractmethod
from datetime import datetime, date
import dateutil.parser
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


# ********************
# public functions
# ********************


def infer_dateformat_ja(text: str) -> str:
    """Infer the date format of a given text in Japanese style.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        str: A Inferred Python date format

    """

    _, partitions = _parse(text)

    # validate partitions
    num_invalid_partitions = 0
    if (not partitions["year"]) or (partitions["year"] not in _YEAR_PARTITIONS):
        num_invalid_partitions += 1
    if (not partitions["month"]) or (partitions["month"] not in _MONTH_PARTITIONS):
        num_invalid_partitions += 1
    if (not partitions["day"]) or (partitions["day"] not in _DAY_PARTITIONS):
        num_invalid_partitions += 1
    if partitions["hour"] and (partitions["hour"] not in _HOUR_PARTITIONS):
        num_invalid_partitions += 1
    if partitions["minute"] and (partitions["minute"] not in _MINUTE_PARTITIONS):
        num_invalid_partitions += 1
    if partitions["second"] and (partitions["second"] not in _SECOND_PARTITIONS):
        num_invalid_partitions += 1
    if partitions["microsecond"] and (partitions["microsecond"] not in _MICROSECOND_PARTITIONS):
        num_invalid_partitions += 1

    if num_invalid_partitions > 0:
        raise ValueError(f"Cannot infer a format from the given text: {text}")

    # make format string
    inferred_format = ""
    inferred_format += r"%Y" + partitions["year"]
    inferred_format += r"%m" + partitions["month"]
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


def to_datetime(text: str) -> datetime:
    """Parse and convert a given text to a datetime object.

    If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        datetime.datetime: A parsed datetime object.

    """

    try:
        inferred_format = infer_dateformat_ja(text)
    except ValueError:
        inferred_format = None

    if inferred_format is not None:
        dt_obj = datetime.strptime(text, inferred_format)
    else:
        dt_obj = dateutil.parser.parse(text)

    return dt_obj


def to_date(text: str) -> date:
    """Parse and convert a given text to a date object.

    If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        datetime.date: A parsed date object.

    """

    dt_obj = to_datetime(text)

    return dt_obj.date()
