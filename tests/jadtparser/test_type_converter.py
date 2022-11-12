import pytest
import jadtparser

from datetime import datetime, date, time
import dateutil.tz


# ****************************
# test to_datetime
# ****************************

def test_to_datetime_ja_ymd():
    input_ = "2022年10月30日"
    excepted = datetime(2022, 10, 30)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_ja_ymdhmsf():
    input_ = "2022年10月30日9時30分20.000000秒"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_ja_ymdhms_withtz():
    input_ = "2022年10月30日9時30分20秒"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0, dateutil.tz.gettz("Asia/Tokyo"))
    result = jadtparser.to_datetime(input_, with_tz=True)
    assert result == excepted

def test_to_datetime_ja_ymdhms_withtz_utc():
    input_ = "2022年10月30日9時30分20秒"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0, dateutil.tz.gettz("UTC"))
    result = jadtparser.to_datetime(input_, with_tz=True, tz_name="UTC")
    assert result == excepted

def test_to_datetime_notja():
    input_ = "20221030T093020"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_ja_ymdhms_list():
    input_ = [
        "2022年10月30日9時30分20秒",
        "2022年11月30日9時30分20秒"
    ]
    excepted = [
        datetime(2022, 10, 30, 9, 30, 20, 0),
        datetime(2022, 11, 30, 9, 30, 20, 0),
    ]
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_notja_ymdhms_list():
    input_ = [
        "20221030T093020",
        "20221130T093020"
    ]
    excepted = [
        datetime(2022, 10, 30, 9, 30, 20, 0),
        datetime(2022, 11, 30, 9, 30, 20, 0),
    ]
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_ja_ymdhms_list_multifmts():
    input_ = [
        "2022年10月30日9時30分20秒",
        "2022年11月30日9:30:20"
    ]
    with pytest.raises(ValueError):
        jadtparser.to_datetime(input_)

def test_to_datetime_invalid():
    input_ = "二〇二二年十月三〇日"
    with pytest.raises(ValueError):
        jadtparser.to_datetime(input_)


# ****************************
# test to_date
# ****************************

def test_to_date_ja_ymd():
    input_ = "2022年10月30日"
    excepted = date(2022, 10, 30)
    result = jadtparser.to_date(input_)
    assert result == excepted

def test_to_date_ja_ymdhms_list():
    input_ = [
        "2022年10月30日9時30分20秒",
        "2022年11月30日9時30分20秒"
    ]
    excepted = [
        date(2022, 10, 30),
        date(2022, 11, 30),
    ]
    result = jadtparser.to_date(input_)
    assert result == excepted

def test_to_date_notja():
    input_ = "20221030T093020"
    excepted = date(2022, 10, 30)
    result = jadtparser.to_date(input_)
    assert result == excepted

def test_to_date_invalid():
    input_ = "二〇二二年十月三〇日"
    with pytest.raises(ValueError):
        jadtparser.to_date(input_)


# ****************************
# test to_time
# ****************************

def test_to_time_ja_ymd():
    input_ = "2022年10月30日"
    excepted = time(0, 0, 0)
    result = jadtparser.to_time(input_)
    assert result == excepted

def test_to_time_ja_ymdhms_list():
    input_ = [
        "2022年10月30日9時30分20秒",
        "2022年11月30日10時30分20秒"
    ]
    excepted = [
        time(9, 30, 20),
        time(10, 30, 20),
    ]
    result = jadtparser.to_time(input_)
    assert result == excepted

def test_to_time_notja():
    input_ = "20221030T093020"
    excepted = time(9, 30, 20)
    result = jadtparser.to_time(input_)
    assert result == excepted

def test_to_time_invalid():
    input_ = "二〇二二年十月三〇日六時三〇分"
    with pytest.raises(ValueError):
        jadtparser.to_time(input_)
