from dateutil import parser


def string2date(value):
    return parser.parse(value).date()


def string2datetime(value):
    return parser.parse(value)


def create_pandas_query(year, month=None, day=None):
    query = 'YEAR == {}'.format(year)
    if month:
        query += ' & MONTH == {}'.format(month)
        if day:
            query += " & DAY == {}".format(day)

    return query

