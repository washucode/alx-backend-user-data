#!/usr/bin/env python3
"""
This module contains a method called filter_datum that returns the log message
obfuscated
"""

import re


def filter_datum(fields, reda, mess, sep):
    """Returns the log message obfuscated"""
    my_regex = f'(?<={fields[0]}=).*?(?={sep})|(?<={fields[1]}=).*?(?={sep})'
    return re.sub(my_regex, reda, mess)
