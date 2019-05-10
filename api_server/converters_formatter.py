from dateutil import parser


def string2date(value):
    return parser.parse(value).date()

def string2datetime(value):
    return parser.parse(value)
