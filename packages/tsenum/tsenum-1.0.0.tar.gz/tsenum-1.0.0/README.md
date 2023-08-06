# tsenum

A timestamp generator.

## commands

```
usage: tsenum.py [-h] [--utc] --offset OFFSET --count COUNT --step
                 {day,week,hour,minute} --pattern PATTERN

Enumerate timestamps from now with offset in different units.

optional arguments:
  -h, --help            show this help message and exit
  --utc, -u             Current time is in UTC
  --offset OFFSET, -o OFFSET
                        Offset to enumerate from
  --count COUNT, -c COUNT
                        Count to enumerate
  --step {day,week,hour,minute}, -s {day,week,hour,minute}
                        Step width
  --pattern PATTERN, -p PATTERN
                        Date pattern to use (see Python's strftime in
                        datetime)
```
## Usage (Module)

Count 7 days back from yesterday.

```
from tsenum import enumerate_times
from datetime import datetime

enumerate_times(datetime.now(), -1, -7, 'day', '%Y-%m-%d')
```

## Usage (CLI)

Count 7 days back from yesterday.

```
tsenum --offset -1 --count -7 --step day --pattern "%Y-%m-%d: Hello world!"
2016-05-27: Hello world!
2016-05-28: Hello world!
2016-05-29: Hello world!
2016-05-30: Hello world!
2016-05-31: Hello world!
2016-06-01: Hello world!
2016-06-02: Hello world!
```

Count 3 weeks into future starting from now.

```
tsenum --offset 0 --count 3 --step day --pattern "Week %V"
Week 22
Week 22
Week 23
```
