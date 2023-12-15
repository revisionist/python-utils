import logging

from .. import _persistent


logger = logging.getLogger(__name__)


def conn_rollback(conn):

    if conn:
        try:
            #logger.debug("Doing conn.rollback()")
            conn.rollback()
        except Exception as e:
            logger.exception(f"Error during conn.rollback(): {e}")


def conn_close(conn):

    if conn:
        try:
            #logger.debug(f"Closing database connection after total_changes: {conn.total_changes}")
            conn.close()
        except Exception as e:
            logger.exception(f"Error during conn.close(): {e}")


