#!/usr/bin/env python3
"""filtered_logger module"""
import re
from typing import List
import logging


def filter_datum(
    fields: List[str],
    redaction: str,
    message: str,
    separator: str
) -> str:
    """returns the log message obfuscated"""
    return re.sub(
        f'({"|".join(fields)})=[^{separator}]+',
        lambda m: f'{m.group(1)}={redaction}',
        message
    )


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=None):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields or []

    def format(self, record: logging.LogRecord) -> str:
        """formats the logger"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR
        )
        return super().format(record)
