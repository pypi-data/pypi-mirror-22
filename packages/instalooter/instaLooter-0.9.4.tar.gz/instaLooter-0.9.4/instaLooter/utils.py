#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import os
import hues
import sys
import functools
import datetime
import dateutil.relativedelta
import warnings

console = hues.SimpleConsole(stdout=sys.stderr)


def get_times(timeframe):
    if timeframe is None:
        timeframe = (None, None)
    else:
        assert isinstance(timeframe, tuple)
        assert isinstance(timeframe[0], datetime.date)
        assert isinstance(timeframe[1], datetime.date)

    start_time = timeframe[0] or datetime.date.today()
    end_time = timeframe[1] or datetime.date.fromtimestamp(0)

    return start_time, end_time


def get_times_from_cli(cli_token):

    today = datetime.date.today()

    if cli_token=="thisday":
        return today, today
    elif cli_token=="thisweek":
        return today, today - dateutil.relativedelta.relativedelta(days=7)
    elif cli_token=="thismonth":
        return today, today - dateutil.relativedelta.relativedelta(months=1)
    elif cli_token=="thisyear":
        return today, today - dateutil.relativedelta.relativedelta(years=1)
    else:
        try:
            start_date, stop_date = cli_token.split(':')
        except ValueError:
            raise ValueError("--time parameter must contain a colon (:)")
        if not start_date and not stop_date: # ':', no start date, no stop date
            return None
        try:
            start_date = date_from_isoformat(start_date) if start_date else datetime.date.today()
            stop_date = date_from_isoformat(stop_date) if stop_date else datetime.date.fromtimestamp(0)
        except ValueError:
            raise ValueError("--time parameter was not provided ISO formatted dates")
        return start_date, stop_date


def date_from_isoformat(isoformat_date):
    year, month, day = isoformat_date.split('-')
    return datetime.date(int(year), int(month), int(day))


def warn_with_hues(message, category, filename, lineno, file=None, line=None):
    console.warn(message)

def warn_windows(message, category, filename, lineno, file=None, line=None):
    print(("{d.hour}:{d.minute}:{d.second} - WARNING - "
          "{msg}").format(d=datetime.datetime.now(), msg=message), file=sys.stderr)

def wrap_warnings(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        showwarning = warnings.showwarning
        if os.name == 'posix':
            warnings.showwarning = warn_with_hues
        else:
            warnings.showwarning = warn_windows
        result = func(*args, **kwargs)
        warnings.showwarning = showwarning
        return result
    return new_func
