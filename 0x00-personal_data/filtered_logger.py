#!/usr/bin/env python3
"""filtered_logger module"""
import re
from typing import List


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
