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
import types

from . import _persistent

logger = logging.getLogger(__name__)


# Import specific functions from utility modules
#from .sqlite import configure_db, get_db_conn, conn_rollback, conn_close

# Alternatively, import entire modules
from . import db


ABOUT = """domestique [doh-mes-teek] _noun_
   1. Cycling. a member of a bicycle-racing team who assists the leader, as by setting a pace, preventing breakaways by other teams, or supplying food during a race."""


persistent = types.SimpleNamespace()
persistent.defaults = types.SimpleNamespace()
persistent.defaults.id = ""


# Package-level initialization code can also be placed here
#print("Initializing the 'domestique' package")


# Optionally, you can define some package-level functions
#def package_function():
#    print("This is a package-level function")


