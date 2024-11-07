#!/usr/bin/env python3
"""
Module for handling personal data and database operations
"""
import logging
import mysql.connector
import os
from typing import List

# PII fields to be redacted
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def filter_datum(fields: List[str], redaction: str,
                message: str, separator: str) -> str:
    """
    Returns the log message obfuscated
    """
    import re
    for field in fields:
        pattern = f'{field}=.*?{separator}'
        repl = f'{field}={redaction}{separator}'
        message = re.sub(pattern, repl, message)
    return message

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Filters values in incoming log records using filter_datum
        """
        log_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                          log_message, self.SEPARATOR)

def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the MySQL database
    """
    return mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

def main():
    """
    Retrieve all rows in the users table and display each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users;")
    
    for row in cursor:
        filtered_row = '; '.join(f"{k}={v}" for k, v in row.items())
        logger.info(filtered_row)

    cursor.close()
    db.close()

if __name__ == "__main__":
    main()
