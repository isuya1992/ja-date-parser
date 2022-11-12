import pytest
import jadtparser

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# ****************************
# test add
# ****************************

def test_date_add_ja_ymd():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2022年11月02日"
    result = jadtparser.date_add(input_dt, input_interval)
    assert result == excepted

def test_date_add_ja_ymd_unit_week():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2022年11月20日"
    result = jadtparser.date_add(input_dt, input_interval, unit="week")
    assert result == excepted

def test_date_add_ja_ymd_unit_month():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2023年01月30日"
    result = jadtparser.date_add(input_dt, input_interval, unit="month")
    assert result == excepted

def test_date_add_ja_ymd_unit_year():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2025年10月30日"
    result = jadtparser.date_add(input_dt, input_interval, unit="year")
    assert result == excepted

def test_date_add_ja_ymd_unit_invalid():
    input_dt = "2022年10月30日"
    input_interval = 3
    with pytest.raises(ValueError):
        jadtparser.date_add(input_dt, input_interval, unit="hour")

def test_date_add_ja_ymd_convert():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = datetime(2022, 11, 2)
    result = jadtparser.date_add(input_dt, input_interval, convert_dt=True)
    assert result == excepted

def test_date_add_notja_ymd():
    input_dt = "20221030"
    input_interval = 3
    with pytest.raises(ValueError):
        jadtparser.date_add(input_dt, input_interval, unit="hour")


# ****************************
# test sub
# ****************************


def test_date_sub_ja_ymd():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2022年10月27日"
    result = jadtparser.date_sub(input_dt, input_interval)
    assert result == excepted

def test_date_sub_ja_ymd_unit_week():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2022年10月09日"
    result = jadtparser.date_sub(input_dt, input_interval, unit="week")
    assert result == excepted

def test_date_sub_ja_ymd_unit_month():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2022年07月30日"
    result = jadtparser.date_sub(input_dt, input_interval, unit="month")
    assert result == excepted

def test_date_sub_ja_ymd_unit_year():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = "2019年10月30日"
    result = jadtparser.date_sub(input_dt, input_interval, unit="year")
    assert result == excepted

def test_date_sub_ja_ymd_unit_invalid():
    input_dt = "2022年10月30日"
    input_interval = 3
    with pytest.raises(ValueError):
        jadtparser.date_sub(input_dt, input_interval, unit="hour")

def test_date_sub_ja_ymd_convert():
    input_dt = "2022年10月30日"
    input_interval = 3
    excepted = datetime(2022, 10, 27)
    result = jadtparser.date_sub(input_dt, input_interval, convert_dt=True)
    assert result == excepted

def test_date_sub_notja_ymd():
    input_dt = "20221030"
    input_interval = 3
    with pytest.raises(ValueError):
        jadtparser.date_sub(input_dt, input_interval, unit="hour")


# ****************************
# test date_diff
# ****************************

def test_date_diff():
    input_date1 = "2022年10月30日"
    input_date2 = "2022年10月27日"
    excepted = timedelta(days=3)
    result = jadtparser.date_diff(input_date1, input_date2)
    assert result == excepted

def test_date_diff_relative():
    input_date1 = "2022年10月30日"
    input_date2 = "2022年10月27日"
    excepted = relativedelta(days=3)
    result = jadtparser.date_diff(input_date1, input_date2, relative=True)
    assert result == excepted
