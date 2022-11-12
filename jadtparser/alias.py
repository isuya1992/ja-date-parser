""" The module which offers aliases to improve usability.

"""

from datetime import datetime, date
from typing import Iterable


# ********************
# typing
# ********************

StrOrIterable = str | Iterable[str]
DatetimeOrList = datetime | list[datetime]
DateOrList = date | list[date]
