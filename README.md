# alfred-datetime

[![Latest Travis CI build status](https://travis-ci.org/kdeal/alfred-datetime.png)](https://travis-ci.org/kdeal/alfred-datetime)

Handle datetime formatting and math with alfred

## Install

Download the latest [release](https://github.com/kdeal/alfred-datetime/releases) and double click to add to alfred.

## Usage

### `dt`
- Specify a formatted time to switch to another format
- Use `now`, `today`, `tomorrow`, `yesterday`
- `+/- <amount> <unit>` to add or subtract time
    - units: microseconds(ms), seconds(s), minutes(min), hours(hr), days(dy), weeks(wk), months(mn), years(yr)
- `next|prev <day of the week>`
- `start|end <unit>`
    - units: day, week, month, year, decade, century
- `to <timezone>`
    - accepts local, utc, or a timezone
    - partial match timezone if it matches a single timezone (i.e. `york` matches
    `America/New_York`)
- Use a combination of the commands above
    - `dt now + 2 weeks 2 days`
    - `dt next monday + 2 days`
    - `dt 2017-09-10 22:10:44 start week`

## Todo
- Handle time zone better
- Improve docs
- Allow users to define formats
- Add some tests to make sure things work
