import logging

from datetime import datetime

from flask import make_response

from .. import _persistent

from ..text import tidy_and_truncate_string, truncate_string
from ..identifiers import generate_id, generate_shorter_id
from ..logging import get_calling_method_text, get_calling_method_name_quick, log_exception


logger = logging.getLogger(__name__)

META = "_meta"


class ResponseWrapper:

    def __init__(self, request, client_id=None):

        if not request:
            raise ValueError("ResponseWrapper requires a request parameter!")

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
        self.method_text = get_calling_method_text(3)

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
        elif isinstance(data, tuple):
            message, exception_identifier = data
            self.exception_id = exception_identifier
            self.response_data = {"message": message}
        elif isinstance(data, str):
            self.response_data = {"message": data}
        else:
            raise ValueError(f"Invalid response_data type: {data}")


    def set_exception(self, e):

        logger.debug(f"set_exception: {e}")
        message, exception_id = log_exception(self.client_id, e, get_calling_method_name_quick(True))
        self.set_status("ERROR")
        self.code = 500
        self.exception_id = exception_id
        self.set_message(message)


    def add_meta(self, key, value):

        self.meta[key] = value


    def generate_response(self, add_meta=True):

        current_time = datetime.now()
        epoch_ms = int(current_time.timestamp() * 1000)
        execution_time_ms = int((current_time - self.start_time).total_seconds() * 1000)

        return_response_data = self.response_data.copy()

        if add_meta:
            request = self.request
            self.add_meta("response_id", self.response_id)
            if self.client_id:
                self.add_meta("client_id", self.client_id)
            self.add_meta("host", request.host)
            self.add_meta("path", request.path)
            self.add_meta("method", self.method_text)
            self.add_meta("timestamp_ms", epoch_ms)
            self.add_meta("timestamp_str", str(current_time))
            self.add_meta("execution_time_ms", execution_time_ms)
            if self.exception_id:
                self.add_meta("exception_id", self.exception_id)
            return_response_data[META] = self.meta

        if return_response_data.get('message'):
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
