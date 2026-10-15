import os
from decimal import Decimal
from typing import Any, cast

import mysql.connector
import pandas as pd
from mysql.connector import Error

DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", ""),
}
DB_NAME = "lms_db"


def get_connection(use_database=True):
    config = dict(DB_CONFIG)
    if use_database:
        config["database"] = DB_NAME
    return mysql.connector.connect(**config)


def run_query(sql, params=None):
    connection = get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql, params or ())
        rows = cast(list[dict[str, Any]], cursor.fetchall())
        columns = [column[0] for column in cursor.description] if cursor.description else []
    finally:
        connection.close()
    rows = [
        {
            key: float(value) if isinstance(value, Decimal) else value
            for key, value in row.items()
        }
        for row in rows
    ]
    return pd.DataFrame(rows, columns=columns)


def run_command(sql, params=None):
    connection = get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(sql, params or ())
        connection.commit()
        if sql.lstrip().upper().startswith("INSERT"):
            return cursor.lastrowid
        return cursor.rowcount
    finally:
        connection.close()


def run_script(filename):
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    with open(path, encoding="utf-8") as file:
        statements = [part.strip() for part in file.read().split(";") if part.strip()]
    connection = get_connection(use_database=False)
    try:
        cursor = connection.cursor()
        for statement in statements:
            cursor.execute(statement)
        connection.commit()
    finally:
        connection.close()


def friendly_error(error):
    messages = {
        1062: "This record already exists (duplicate email, name or enrollment).",
        1451: "This record cannot be deleted because other records depend on it.",
        1452: "The selected related record does not exist.",
        3819: "One of the values is outside the allowed range.",
        4025: "One of the values is outside the allowed range.",
        1048: "A required field is empty.",
        1045: "Wrong MySQL username or password. Check the settings in db.py.",
        1049: "The lms_db database does not exist yet. Run 01_setup_and_connection.ipynb first.",
        2003: "Cannot reach the MySQL server. Make sure MySQL is running.",
    }
    return messages.get(error.errno, f"Database error: {error.msg}")
