#!/usr/bin/env python3
"""filtered_logger module"""
from datetime import datetime
import logging
import mysql.connector
from mysql.connector import connection
import os
import re
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format='[HOLBERTON] %(name)s %(levelname)s %(asctime)s: %(message)s'
)

PII_FIELDS = ("name", "email", "phone", "ssn", "password")
FILTERED_FIELDS = ["name", "email", "phone", "ssn", "password"]


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

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats the logger"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.msg,
            self.SEPARATOR
        )
        return super().format(record)


def get_logger() -> logging.Logger:
    """Creates and returns a logger named 'user_data'."""
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    """Create a StreamHandler and set the RedactingFormatter"""
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    """Add the handler to the logger"""
    logger.addHandler(stream_handler)

    return logger


def get_db() -> connection.MySQLConnection:
    """Returns a MySQL database connection."""
    username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')

    return mysql.connector.connect(
        user=username,
        password=password,
        host=host,
        database=database
    )


def filter_data(data: dict) -> dict:
    """Filters out sensitive data."""
    return {
        key: '***' if key in FILTERED_FIELDS else value for key,
        value in data.items()}


def main() -> None:
    """Main function that retrieves and displays users'
    data in a filtered format."""
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()

    for row in rows:
        filtered_row = filter_data(row)
        log_msg = "; ".join(
            [f"{key}={value}" for key, value in filtered_row.items()])
        logging.info(log_msg)

    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
