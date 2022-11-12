""" The module which offers datetime operators with preserving date-format

"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from .parser import infer_dateformat_ja
from .type_converter import to_datetime

# ********************
# private functions
# ********************


def _make_tdelta(interval: int, unit: str) -> relativedelta:
    if unit == "day":
        tdelta = relativedelta(days=interval)
    elif unit == "week":
        tdelta = relativedelta(weeks=interval)
    elif unit == "month":
        tdelta = relativedelta(months=interval)
    elif unit == "year":
        tdelta = relativedelta(years=interval)
    else:
        raise ValueError(f"An invalid unit: {unit}")

    return tdelta


# ********************
# public functions
# ********************


def date_add(date: str, interval: int, unit: str = "day", convert_dt: bool = False) -> str | datetime:
    """Parse a text and add a timedelta

    * Return the result with preserving the given date-format if `convert_dt` is set to False.

    Args:
        date (str): A date-format text in Japanese style
        interval (int): A additional interval
        unit ("day" or "week" or "month" or "year"): A additional unit
        convert_dt (bool): Whether or not convert the datetime object

    Returns:
        str or datetime.datetime: The operation result

    Raises:
        ValueError: If given an non-Japanese date-format text, or invalid unit

    """

    try:
        inferred_format = infer_dateformat_ja(date)
    except ValueError:
        raise ValueError(f"Cannot parse the given text: {date} as Japanese date-format.")

    dt = datetime.strptime(date, inferred_format)
    tdelta = _make_tdelta(interval, unit)
    result = dt + tdelta

    output: str | datetime
    if convert_dt:
        output = result
    else:
        output = result.strftime(inferred_format)

    return output


def date_sub(date: str, interval: int, unit: str = "day", convert_dt: bool = False) -> str | datetime:
    """Parse a text and subtract a timedelta

    * Return the result with preserving the given date-format if `convert_dt` is set to False.

    Args:
        date (str): A date-format text in Japanese style
        interval (int): A subtraction interval
        unit ("day" or "week" or "month" or "year"): A subtraction unit
        convert_dt (bool): Whether or not convert the datetime object

    Returns:
        str or datetime.datetime: The operation result

    Raises:
        ValueError: If given an non-Japanese date-format text, or invalid unit

    """

    try:
        inferred_format = infer_dateformat_ja(date)
    except ValueError:
        raise ValueError(f"Cannot parse the given text: {date} as Japanese date-format.")

    dt = datetime.strptime(date, inferred_format)
    tdelta = _make_tdelta(interval, unit)
    result = dt - tdelta

    output: str | datetime
    if convert_dt:
        output = result
    else:
        output = result.strftime(inferred_format)

    return output


def date_diff(date1: str, date2: str, relative: bool = False) -> timedelta | relativedelta:
    """Caluculate the interval of two date

    Args:
        date1 (str): A date-format text in Japanese style
        date2 (str): Same as above
        relative (bool): If True, then this function returns a dateutil.relativedelta.relativedelta instance.
                         If False, then this function returns a datetime.timedelta instance.
                         See: https://dateutil.readthedocs.io/en/stable/relativedelta.html

    Returns:
        datetime.timedelta or dateutil.relativedelta.relativedelta: The interval

    """
    parsed_date1, parsed_date2 = to_datetime([date1, date2])  # type: ignore

    tdelta: timedelta | relativedelta
    if relative:
        tdelta = relativedelta(parsed_date1, parsed_date2)
    else:
        tdelta = parsed_date1 - parsed_date2

    return tdelta
