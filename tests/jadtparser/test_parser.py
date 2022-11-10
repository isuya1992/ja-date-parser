import pytest
import jadtparser

from datetime import datetime, date


# ****************************
# test infer_dateformat_ja
# ****************************
def test_infer_dateformat_ja_ymd():
    input_ = "2022年10月30日"
    excepted = "%Y年%m月%d日"
    result = jadtparser.infer_dateformat_ja(input_)
    assert result == excepted

def test_infer_dateformat_ja_ymdh():
    input_ = "2022年10月30日9時"
    excepted = "%Y年%m月%d日%H時"
    result = jadtparser.infer_dateformat_ja(input_)
    assert result == excepted

def test_infer_dateformat_ja_ymdhm():
    input_ = "2022年10月30日9時30分"
    excepted = "%Y年%m月%d日%H時%M分"
    result = jadtparser.infer_dateformat_ja(input_)
    assert result == excepted

def test_infer_dateformat_ja_ymdhms():
    input_ = "2022年10月30日9時30分20秒"
    excepted = "%Y年%m月%d日%H時%M分%S秒"
    result = jadtparser.infer_dateformat_ja(input_)
    assert result == excepted

def test_infer_dateformat_ja_ymdhmf():
    input_ = "2022年10月30日9時30分20.000000秒"
    excepted = "%Y年%m月%d日%H時%M分%S.%f秒"
    result = jadtparser.infer_dateformat_ja(input_)
    assert result == excepted

def test_infer_dateformat_ja_md():
    input_ = "10月30日"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_y():
    input_ = "2022年"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ym():
    input_ = "2022年10月"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_hms():
    input_ = "9時30分20秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_y():
    input_ = "2022ねん10月30日9時30分20.000000秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_month():
    input_ = "2022年10がつ30日9時30分20.000000秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_d():
    input_ = "2022年10月30にち9時30分20.000000秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_h():
    input_ = "2022年10月30日9じ30分20.000000秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_minute():
    input_ = "2022年10月30日9時30ふん20.000000秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_s():
    input_ = "2022年10月30日9時30分20びょう"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa

def test_infer_dateformat_ja_ymdhms_invalid_microsecond():
    input_ = "2022年10月30日9時30分20秒000000ミリ秒"
    with pytest.raises(ValueError):
        result = jadtparser.infer_dateformat_ja(input_)  # noqa


# ****************************
# test to_datetime
# ****************************

def test_to_datetime_ja_ymd():
    input_ = "2022年10月30日"
    excepted = datetime(2022, 10, 30)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_ja_ymdhmf():
    input_ = "2022年10月30日9時30分20.000000秒"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_notja():
    input_ = "20221030T093020"
    excepted = datetime(2022, 10, 30, 9, 30, 20, 0)
    result = jadtparser.to_datetime(input_)
    assert result == excepted

def test_to_datetime_invalid():
    input_ = "二〇二二年十月三〇日"
    with pytest.raises(ValueError):
        result = jadtparser.to_datetime(input_)  # noqa


# ****************************
# test to_date
# ****************************

def test_to_date_ja_ymd():
    input_ = "2022年10月30日"
    excepted = date(2022, 10, 30)
    result = jadtparser.to_date(input_)
    assert result == excepted

def test_to_date_ja_ymdhmf():
    input_ = "2022年10月30日9時30分20.000000秒"
    excepted = date(2022, 10, 30)
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
        result = jadtparser.to_date(input_)  # noqa
