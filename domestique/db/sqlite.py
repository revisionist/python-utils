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

    dbfile = _persistent.get_value(PROPNAME_SQLITE_DB_FILE)
    try:
        conn = sqlite3.connect(dbfile)
    except Exception as e:
        logger.error(f"Unable to connect to database file: {dbfile}")
        raise e

    # To enable using column names to address result items
    conn.row_factory = sqlite3.Row

    #logger.debug(f"Method get_db_conn returning {repr(conn)}")

    return conn


