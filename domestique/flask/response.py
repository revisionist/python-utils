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

from datetime import datetime

from flask import make_response, jsonify

from .. import _persistent

from ..text import tidy_and_truncate_string, truncate_string
from ..identifiers import generate_id, generate_shorter_id
from ..convert import get_dict_or_string

from ..logging import get_calling_method_text, get_calling_method_name_quick, log_exception


logger = logging.getLogger(__name__)

META = "_meta"


class ResponseWrapper:

    def __init__(self, request, client_id=None, calling_method_text=None, abstraction_level=3):

        if not request:
            raise ValueError("ResponseWrapper requires a request parameter!")

        if not calling_method_text:
            calling_method_text = get_calling_method_text(abstraction_level)

        self.start_time = datetime.now()
        self.response_id = generate_shorter_id()
        self.request = request
        self.response_data = {}
        self.meta = {}
        self.set_message("")
        self.set_status("OK")
        self.code = 200
        self.client_id = client_id
        self.exception_id = None
        self.method_text = calling_method_text

        debug_message = "Init ResponseWrapper: "
        if client_id:
            debug_message += f"client_id: {client_id}, "
        debug_message += f"url: {request.url}"
        logger.debug(debug_message)


    def get_id(self):

        return self.response_id


    def set_status(self, status):

        self.response_data["status"] = status


    def set_message(self, message):

        self.response_data["message"] = message


    def set_data(self, data, code, exception_id=None):

        self.code = code
        self.exception_id = exception_id

        if isinstance(data, dict):
            self.response_data = data.copy()
        elif isinstance(data, list):
            self.response_data = jsonify(data)
        elif isinstance(data, tuple):
            message, exception_identifier = data
            self.exception_id = exception_identifier
            self.response_data = {"message": message}
        elif isinstance(data, str):
            self.response_data = {"message": data}
        else:
            raise ValueError(f"Invalid response_data type: {data}")


    def set_plain(self, data, code):

        self.code = code
        self.response_data = get_dict_or_string(data)


    def set_exception(self, e):

        logger.debug(f"set_exception: {e}")
        message, exception_id = log_exception(self.client_id, e, self.method_text, True, self.response_id)
        self.set_status("ERROR")
        self.code = 500
        self.exception_id = exception_id
        self.set_message(message)


    def set_error(self, message=None, code=500):

        logger.debug(f"set_error: {code} - {message}")
        self.set_status("ERROR")
        self.code = code
        if message:
            self.set_message(message)


    def add_meta(self, key, value):

        self.meta[key] = value


    def generate_response(self, add_meta=True):

        current_time = datetime.now()
        epoch_ms = int(current_time.timestamp() * 1000)
        execution_time_ms = int((current_time - self.start_time).total_seconds() * 1000)

        if isinstance(self.response_data, dict):
            return_response_data = self.response_data.copy()
        else:
            return_response_data = self.response_data

        if add_meta:
            request = self.request
            self.add_meta("response_id", self.response_id)
            if self.client_id:
                self.add_meta("client_id", self.client_id)
            self.add_meta("host", request.host)
            self.add_meta("path", request.path)
            self.add_meta("method", request.method)
            self.add_meta("handler", self.method_text)
            self.add_meta("timestamp_ms", epoch_ms)
            self.add_meta("timestamp_str", str(current_time))
            self.add_meta("execution_time_ms", execution_time_ms)
            if self.exception_id:
                self.add_meta("exception_id", self.exception_id)
            return_response_data[META] = self.meta

        if isinstance(return_response_data, dict) and return_response_data.get('message'):
            msg_text_for_debug = "with message: " + tidy_and_truncate_string(return_response_data.get('message'), 120)
        else:
            msg_text_for_debug = "with no message"

        logger.debug(f"{self.response_id} [{self.code}] from '{self.method_text}' {msg_text_for_debug}")

        return make_response(return_response_data, self.code)


    def generate_response_with_exception(self, e):

        self.set_exception(e)
        return self.generate_response()


    def generate_response_with_data(self, data, code, exception_id=None):
    
        self.set_data(data, code, exception_id)
        return self.generate_response()


def check_response_status(response, url=None):

    if not response:
        raise Exception(f"No response passed to check_response_status for URL: {url}")
    #logger.debug(f"Checking response: {response.text}")
    if not 200 <= response.status_code <= 299:
        error_message = f"Error calling web service: {response.message}" if 'message' in response else f"Error calling web service: {response.text}"
        logger.error(error_message)
        if url:
            logger.error(f"URL was: {url}")
        raise Exception(error_message)
