import sqlite3
import os

os.makedirs(
    "database",
    exist_ok=True
)

conn = sqlite3.connect(
    "database/history.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS reports (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,

        url TEXT UNIQUE,

        report_path TEXT
    )
    """
)

conn.commit()


def save_report(
    title,
    url,
    report_path
):

    cursor.execute(
        """
        INSERT OR REPLACE INTO reports
        (
            title,
            url,
            report_path
        )
        VALUES
        (
            ?,
            ?,
            ?
        )
        """,
        (
            title,
            url,
            report_path
        )
    )

    conn.commit()


def get_recent_reports(
    limit=10
):

    cursor.execute(
        """
        SELECT title
        FROM reports
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    return cursor.fetchall()


def get_report_by_url(
    url
):

    cursor.execute(
        """
        SELECT report_path
        FROM reports
        WHERE url = ?
        LIMIT 1
        """,
        (url,)
    )

    return cursor.fetchone()