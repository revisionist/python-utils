# Copyright 2023-2024 David Goddard.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

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


def conn_commit(conn):

    if conn:
        try:
            #logger.debug("Doing conn.commit()")
            conn.commit()
        except Exception as e:
            logger.exception(f"Error during conn.commit(): {e}")


def conn_close(conn):

    if conn:
        try:
            #logger.debug(f"Closing database connection after total_changes: {conn.total_changes}")
            conn.close()
        except Exception as e:
            logger.exception(f"Error during conn.close(): {e}")


def concat_sql(sql_parts):

    return ' '.join(s.strip() for s in sql_parts if s.strip())

