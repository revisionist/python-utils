import logging
import sqlite3

from .. import _persistent

logger = logging.getLogger(__name__)


PROPNAME_SQLITE_DB_FILE = "sqlite_db_file"


def configure_db(db_file_path):

    logger.debug(f"Configuring {PROPNAME_SQLITE_DB_FILE}: {db_file_path}")
    _persistent.set_value(PROPNAME_SQLITE_DB_FILE, db_file_path)


def get_db_conn():

    if not _persistent.has_value(PROPNAME_SQLITE_DB_FILE):
        raise ValueError("Database file path is not configured")

    conn = sqlite3.connect(_persistent.get_value(PROPNAME_SQLITE_DB_FILE))

    # To enable using column names to address result items
    conn.row_factory = sqlite3.Row

    #logger.debug(f"Method get_db_conn returning {repr(conn)}")

    return conn


