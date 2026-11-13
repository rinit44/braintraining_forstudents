import mysql.connector

"""
database.py - All interactions with the Braintraining database
Author: Rinit
"""

import mysql.connector

try:
    from db_config import DB_CONFIG  # local file, not committed (see db_config_example.py)
except ImportError:
    raise SystemExit("Missing db_config.py: copy db_config_example.py to db_config.py and fill it in.")


def open_connection():
    return mysql.connector.connect(**DB_CONFIG)


def get_or_create_user(cursor, username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    row = cursor.fetchone()
    if row:
        return row[0]
    cursor.execute("INSERT INTO users (username) VALUES (%s)", (username,))
    return cursor.lastrowid


def get_exercise_id(cursor, exercise_code):
    """Return the id of the exercise from its code (ex: 'GEO01')."""
    cursor.execute("SELECT id FROM exercises WHERE code = %s", (exercise_code,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError(f"Unknown exercise: {exercise_code}")
    return row[0]


def insert_result(username, exercise_code, duration_s, nb_trials, nb_ok):
    connection = open_connection()
    try:
        cursor = connection.cursor()
        user_id = get_or_create_user(cursor, username)
        exercise_id = get_exercise_id(cursor, exercise_code)
        cursor.execute(
            "INSERT INTO results (duration, nb_trials, nb_ok, user_id, exercise_id) "
            "VALUES (%s, %s, %s, %s, %s)",
            (duration_s, nb_trials, nb_ok, user_id, exercise_id),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_results(username=None, exercise_code=None):
    query = (
        "SELECT u.username, e.code AS exercise, r.date_hour, r.duration, r.nb_trials, r.nb_ok "
        "FROM results r "
        "JOIN users u ON u.id = r.user_id "
        "JOIN exercises e ON e.id = r.exercise_id "
        "WHERE 1 = 1"
    )
    params = []
    if username:
        query += " AND u.username = %s"
        params.append(username)
    if exercise_code:
        query += " AND e.code = %s"
        params.append(exercise_code)
    query += " ORDER BY r.date_hour DESC"

    connection = open_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        connection.close()


def get_usernames():
    """Return the list of all usernames (for the filter)."""
    connection = open_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT username FROM users ORDER BY username")
        return [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()


def get_exercise_codes():
    """Return the list of all exercise codes (for the filter)."""
    connection = open_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT code FROM exercises ORDER BY code")
        return [row[0] for row in cursor.fetchall()]
    finally:
        connection.close()


def format_duration(duration_s):
    """Convert seconds to 'm:ss' for display (ex: 127 -> '2:07')."""
    return f"{duration_s // 60}:{duration_s % 60:02d}"