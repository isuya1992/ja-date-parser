""" The module which offers type converters from date-format strings to datetime objects.

"""

from datetime import datetime
import dateutil.parser
import dateutil.tz
from collections.abc import Iterable

from .alias import StrOrIterable, DatetimeOrList, DateOrList, TimeOrList
from .parser import infer_dateformat_ja, infer_dateformat_ja_all


# ********************
# public functions
# ********************


def to_datetime(date: StrOrIterable, with_tz: bool = False, tz_name: str = "Asia/Tokyo") -> DatetimeOrList:
    """Parse and convert a given text to a datetime object.

    * If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.
    * If missing month or day digits in a text, then assign 1 as thier value.

    Args:
        date (str): A date format text in Japanese style
        with_tz (bool): Whether or not append timezone from `tz_name` to datetime
        tz_name (str): Time zone name. This is valid if `with_tz` = True.

    Returns:
        datetime.datetime or list[datetime.datetime]: Parsed datetime objects

    Raises:
        ValueError: If extsts multi formats in given texts
        TypeError: If an invalid type arg is given

    """

    tz_obj = dateutil.tz.gettz(tz_name)
    out_obj: DatetimeOrList

    if isinstance(date, str):
        try:
            inferred_format = infer_dateformat_ja(date)
        except ValueError:
            inferred_format = None  # Imply not Japanese or invalid format

        if inferred_format is not None:
            dt_obj = datetime.strptime(date, inferred_format)
        else:
            dt_obj = dateutil.parser.parse(date)

        if with_tz:
            dt_obj = dt_obj.replace(tzinfo=tz_obj)

        out_obj = dt_obj

    elif isinstance(date, Iterable):
        inferred_format_list = list()
        try:
            inferred_format_list += infer_dateformat_ja_all(date)
            if len(inferred_format_list) != 1:
                raise ValueError("Cannot infer ONE date-format")
            inferred_format = inferred_format_list[0]
        except ValueError:
            inferred_format = None   # Imply not Japanese or invalid forma

        out_obj = list()
        for dtstr in date:
            if inferred_format is not None:
                dt_obj = datetime.strptime(dtstr, inferred_format)
            else:
                dt_obj = dateutil.parser.parse(dtstr)

            if with_tz:
                dt_obj = dt_obj.replace(tzinfo=tz_obj)

            out_obj.append(dt_obj)
    else:
        raise TypeError("Invalid type")

    return out_obj


def to_date(date: StrOrIterable) -> DateOrList:
    """Parse and convert a given text to a date object.

    * If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.
    * If missing month or day digits in a text, then assign 1 as thier value.

    Args:
        date (str): A date format text in Japanese style

    Returns:
        datetime.date or list[datetime.date]: A parsed date object

    """

    dt_obj = to_datetime(date)
    out_obj: DateOrList

    if isinstance(dt_obj, datetime):
        out_obj = dt_obj.date()
    else:
        out_obj = list()
        for dt in dt_obj:
            out_obj.append(dt.date())

    return out_obj

def to_time(date: StrOrIterable) -> TimeOrList:
    """Parse and convert a given text to a time object.

    * If it is failure to inffer a format in Japanese meaning, then parse text by dateutil.parser.
    * If missing month or day digits in a text, then assign 1 as thier value.

    Args:
        text (str): A date format text in Japanese style

    Returns:
        datetime.time or list[datetime.time]: A parsed date object

    """

    dt_obj = to_datetime(date)
    out_obj: TimeOrList

    if isinstance(dt_obj, datetime):
        out_obj = dt_obj.time()
    else:
        out_obj = list()
        for dt in dt_obj:
            out_obj.append(dt.time())

    return out_obj
