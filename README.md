# ja-date-parser

A package which offers handling to Japanese date format strings.

## Installtion

```python
pip install ja-date-parser
```

## Usage

```python
>>> import jadtparser
>>> 
>>> jadtparser.to_datetime("2022年11月1日9時30分")
datetime.datetime(2022, 11, 1, 9, 30)
>>> jadtparser.to_date("2022年11月1日9時30分")
datetime.date(2022, 11, 1)
>>> # Use dateutil.parser to parse non-Japanese formats
>>> jadtparser.to_date("20221101093020")
datetime.date(2022, 11, 1)
```
