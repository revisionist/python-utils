# Copyright 2025 David Goddard.
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
from fastapi.responses import JSONResponse
from domestique.text import tidy_and_truncate_string
from domestique.identifiers import generate_shorter_id
from domestique.logging import get_calling_method_text, log_exception

logger = logging.getLogger(__name__)

META = "_meta"

class ResponseFormatter:

    def __init__(self, client_id: str, request, function_info=None, abstraction_level=3):

        if not request:
            raise ValueError("ResponseFormatter requires a request object")

        self.request = request
        self.client_id = client_id
        self.start_time = datetime.utcnow()
        self.response_id = generate_shorter_id()
        self.method_text = function_info or get_calling_method_text(abstraction_level)
        self.exception_id = None

        logger.debug(f"Init ResponseFormatter: client_id={client_id}, url={request.url}")


    def _infer_status(self, e) -> int:

        name = e.__class__.__name__
        msg = str(e).lower()
        try:
            from fastapi.exceptions import RequestValidationError as _RVE  # type: ignore
        except Exception:
            _RVE = ()
        try:
            from pydantic_core import ValidationError as _PCVE  # type: ignore
        except Exception:
            _PCVE = ()
        if isinstance(e, _RVE) or isinstance(e, _PCVE) or name == "ValidationError":
            return 422
        if isinstance(e, (ValueError, KeyError)):
            return 400
        if isinstance(e, PermissionError):
            return 403
        if isinstance(e, FileNotFoundError) or "not found" in msg:
            return 404

        return 500


    def generate_response_with_data(self, data, status_code=200, exception_id=None):

        self.exception_id = exception_id
        return self._generate(data, status_code)


    def generate_response_with_exception(self, e, status_code: int | None = None):

        user_message, exception_id = log_exception(
            client_id=self.client_id,
            e=e,
            calling_method_name=self.method_text,
            include_traceback=True,
            response_id=self.response_id,
        )
        self.exception_id = exception_id

        if exception_id not in user_message:
            user_message = f"{user_message} [error_id:{exception_id}]"

        if status_code is None:
            status_code = self._infer_status(e)

        logger.info(f"[{self.response_id}] returning error {status_code} ({self.method_text}) ref={exception_id}")

        return self._generate(user_message, status_code)


    def _generate(self, data, status_code):

        now = datetime.utcnow()
        execution_time_ms = int((now - self.start_time).total_seconds() * 1000)
        epoch_ms = int(now.timestamp() * 1000)

        response_data = {}
        if isinstance(data, dict):
            response_data = data.copy()
        elif isinstance(data, str):
            response_data["message"] = data
        else:
            response_data["message"] = str(data)

        meta = {
            "response_id": self.response_id,
            "client_id": self.client_id,
            "host": self.request.headers.get("host", "unknown"),
            "path": self.request.url.path,
            "method": self.request.method,
            "handler": self.method_text,
            "timestamp_ms": epoch_ms,
            "timestamp_str": str(now),
            "execution_time_ms": execution_time_ms
        }

        if self.exception_id:
            meta["exception_id"] = self.exception_id

        response_data[META] = meta

        if "message" in response_data:
            preview = tidy_and_truncate_string(response_data["message"], 120)
        else:
            preview = "with no message"

        logger.debug(f"{self.response_id} [{status_code}] from '{self.method_text}' {preview}")

        return JSONResponse(status_code=status_code, content=response_data)
