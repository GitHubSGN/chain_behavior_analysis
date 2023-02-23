from datetime import datetime
from numbers import Number

from dataStruct.constant import Constant
from tools.validator import type_validator

def datetime_to_timestamp(r_datetime):
    # transfer datetime to timestamp
    return int(datetime.timestamp( r_datetime ) * 1000)

def timestamp_output(input):
    if type_validator(input, datetime, False):
        return datetime_to_timestamp(input)
    elif type_validator(input, Number, False):
        return input
    return None

def granularity_annualized_const(granularity):
    # output the annualized constant for a given granularity, e.g.
    #   "1h" -> 24*365,
    #   "1d" -> 365
    if not type_validator(granularity, str, nullable=False):
        raise ValueError('Parameter of type str is required')

    granularity_int = int(granularity[:-1])

    annu_const = 1.0
    match granularity[-1]:
        case 'm':
            annu_const *= Constant.ONE_DAY_IN_MINUTE * Constant.ONE_YEAR_IN_DAY
        case 'h':
            annu_const *= Constant.ONE_DAY_IN_HOUR * Constant.ONE_YEAR_IN_DAY
        case 'd':
            annu_const *= Constant.ONE_YEAR_IN_DAY
        case 'w':
            annu_const *= Constant.ONE_YEAR_IN_DAY / Constant.ONE_WEEK_IN_DAY
        case _:  # Pattern not attempted
            raise ValueError('Granularity Error.')

    annu_const /= granularity_int

    return annu_const

def granularity_milliseconds(granularity):
    # output milliseconds contained in a granularity, e.g.
    #   "1h" -> 3600*1000
    annu_const = granularity_annualized_const(granularity)
    return Constant.ONE_YEAR_IN_DAY * Constant.ONE_DAY_IN_MILLI / annu_const


def generate_timestamp_sequence(starttime: int, endtime: int, granularity: str, seamless: bool = True):
    # generate timestamp sequence: starttime <= t < endtime with granularity
    # t[0] = starttime
    # t[1], t[2], ... can be divided by 15min (e.g. 9:15, 9:30, 9:45, 10:00, ...) when granularity = '15m'
    # assumption:
    # 1. granularity: m, h, d, w
    #       minutes: can be divided by 60, e.g. 10min, 15min
    #       hours: can be divided by 24, e.g. 4h, 6h

    milli_steps = int(granularity_milliseconds(granularity))
    time_sequence = list( range(starttime, endtime, milli_steps) )

    return time_sequence