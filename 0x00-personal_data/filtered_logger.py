#!/usr/bin/env python3
"""
This module contains a method called filter_datum that returns the log message
obfuscated
"""

import re


def filter_datum(fields, redaction, message, separator):
    """
    Returns the log message obfuscated
    """
    my_regex = f'(?<={fields[0]}=).*?(?={separator})|(?<={fields[1]}=).*?(?={separator})'
    return re.sub(my_regex, redaction, message)
