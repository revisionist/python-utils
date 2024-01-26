# Copyright 2024 David Goddard.
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

from flask import request

from ..db import conn_commit, conn_close
from ..validation import Validator, NoiseLevel
from .response import ResponseWrapper



logger = logging.getLogger(__name__)


class Session:

    def __init__(self, client_id, request, calling_method_text=None, validator_noise_level=NoiseLevel.DEBUG):

        if not client_id:
            raise ValueError("Session init missing required parameter: client_id")
        if not request:
            raise ValueError("Session init missing required parameter: request")

        self._client_id = client_id
        self._request = request
        self._conn = None

        try:
            self._resp = ResponseWrapper(request, client_id, calling_method_text)
        except Exception as e:
            log_exception(client_id, e)
            raise e

        self._id = self._resp.get_id()

        logging_identifiers = [client_id, self._id]

        self._validator = Validator(calling_method_text=calling_method_text, logging_identifiers=logging_identifiers, default_noise_level=validator_noise_level)

        logger.debug(f"Session INIT {self._id} with client_id: {client_id}")
        logger.debug(f"Request: {request}")


    def terminate(self):
    
        logger.debug(f"Session TERMINATE {self._id} with client_id: {self._client_id}")

        conn_close(self._conn)
        self._conn = None


    @property
    def conn(self):

        return self._conn


    @conn.setter
    def conn(self, value):

        self._conn = value


    @property
    def resp(self):

        return self._resp


    @property
    def validator(self):

        return self._validator


    def get_client_id(self):

        return self._client_id


    def get_request(self):

        return self._request


    def get_id(self):

        return self._id
        

    def log_info(self):

        logger.info(f"Route: {self._request.method} {self._request.path} from {self._request.remote_addr} with client '{self._client_id}' - setup response ID: {self._id}")

