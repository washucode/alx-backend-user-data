#!/usr/bin/env python3
"""
This module contains a method called filter_datum that returns the log message
obfuscated
"""

import re
from typing import List
import logging
import mysql.connector
from os import getenv


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """Returns the log message obfuscated"""
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """Returns a logging object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PIL_FIELDS))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to a database"""
    return mysql.connector.connect(
        user=getenv('PERSONAL_DATA_DB_USERNAME'),
        password=getenv('PERSONAL_DATA_DB_PASSWORD'),
        host=getenv('PERSONAL_DATA_DB_HOST'),
        database=getenv('PERSONAL_DATA_DB_NAME')

    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    Args:
        fields: a list of strings
                representing all fields to obfuscate
                """

    # redaction string
    REDACTION = "***"
    # log message format
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    # separator
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values from the log records"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

# if __name__ == '__main__':
#     # Create a logger
#     logger = logging.getLogger('user_data')
#     # Set the log level
#     logger.setLevel(logging.INFO)
#     # Create a stream handler
#     stream_handler = logging.StreamHandler()
#     # Create a RedactingFormatter
#     formatter = RedactingFormatter(fields=("name", "email", "phone"))
#     # Set the formatter
#     stream_handler.setFormatter(formatter)
#     # Add the stream handler to the logger
#     logger.addHandler(stream_handler)
#     # Create a filter
#     logger.info("
