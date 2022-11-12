# ja-date-parser

A package which offers handling to Japanese date format strings.

## Installtion

```python
pip install ja-date-parser
```

## Usage

### Functions

#### to_datetime

* Convert a Japanese date-format text into the corresponding datetime.datetime object.
* For a text with no Japanese date-format, this function try to parse it by dateutil.parser.
  * See: [https://dateutil.readthedocs.io/en/stable/parser.html]
* It is enable to append timezone.

```python
>>> import jadtparser
>>> 
>>> jadtparser.to_datetime("2022年11月1日9時30分")
datetime.datetime(2022, 11, 1, 9, 30)
>>> jadtparser.to_datetime("2022/11/1 9:30")
datetime.datetime(2022, 11, 1, 9, 30)
>>> Append timezone
>>> jadtparser.to_datetime("2022年11月1日9時30分", with_tz=True)
datetime.datetime(2022, 11, 1, 9, 30, tzinfo=tzfile('/usr/share/zoneinfo/Asia/Tokyo'))
>>> jadtparser.to_datetime("2022年11月1日9時30分", with_tz=True, tz_name="UTC")
datetime.datetime(2022, 11, 1, 9, 30, tzinfo=tzfile('/usr/share/zoneinfo/UTC'))
>>> For a text with no Japanese date-format
>>> jadtparser.to_datetime("20221101093020")
datetime.datetime(2022, 11, 1, 9, 30, 20)
```

#### to_date/to_time

* Convert a Japanese date-format text into the corresponding datetime.date (or datetime.time) instance.

```python
>>> import jadtparser
>>> 
>>> jadtparser.to_date("2022年11月1日9時30分")
datetime.date(2022, 11, 1)
>>> jadtparser.to_time("2022年11月1日9時30分")
datetime.time(9, 30)
```

#### infer_dateformat_ja

* Infer a data-format in Japanese style

```python
>>> import jadtparser
>>> 
>>> jadtparser.infer_dateformat_ja("2022年11月1日9時30分")
'%Y年%m月%d日%H時%M分'
```

#### date_add/date_sub

* Add (or Subtract) a date by an interval with preserving its data-format.
* It is enable to return a datetime.datetime instance.

```python
>>> import jadtparser
>>> 
>>> # Add 3days
>>> jadtparser.date_add("2022年11月1日9時30分", 3)
'2022年11月04日09時30分'
>>> # Add 3 months
>>> jadtparser.date_add("2022年11月1日9時30分", 3, unit="month")
'2023年02月01日09時30分'
>>> # Subtract 3 years
>>> jadtparser.date_sub("2022年11月1日9時30分", 3, unit="year")
'2022年10月29日09時30分'
>>> # Return a datetime.datetime instance
>>> jadtparser.date_add("2022年11月1日9時30分", 3, convert_dt=True)
datetime.datetime(2022, 11, 4, 9, 30)
```

#### date_diff

* Calculate the date interval.

```python
>>> import jadtparser
>>> 
>>> jadtparser.date_diff("2022年11月1日9時30分", "2022年10月30日21時30分")
datetime.timedelta(days=1, seconds=43200)
```
