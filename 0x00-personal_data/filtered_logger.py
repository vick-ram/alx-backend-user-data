#!/usr/bin/ env python3
"""filtered_logger module"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    return re.sub(
        f'({"|".join(fields)})=[^{separator}]+',
        lambda m: f'{m.group(1)}={redaction}',
        message
    )
