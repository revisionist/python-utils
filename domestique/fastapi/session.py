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

from __future__ import annotations

import inspect
import logging
from typing import Optional, Dict, Any

from fastapi import Request

from ..validation import Validator, NoiseLevel
from .response import ResponseFormatter

logger = logging.getLogger(__name__)


class SessionContext:

    def __init__(
        self,
        client_id: str,
        function_info: str,
        request: Request,
        noise_level: NoiseLevel = NoiseLevel.DEBUG,
    ) -> None:

        self.client_id = client_id
        self.function_info = function_info
        self.request = request

        self.resp = ResponseFormatter(
            client_id=client_id,
            request=request,
            function_info=function_info,
        )

        self.validator = Validator(
            calling_method_text=function_info,
            default_noise_level=noise_level,
            # Potentially also pass these or other logging_identifiers:
            #logging_identifiers=[client_id, request.url.path]
        )

        self.state: Dict[str, Any] = {}

        logger.debug(f"SessionContext created: client_id={client_id} func={function_info}")


    def terminate(self) -> None:

        try:
            logger.debug(f"Terminating session for {self.function_info} (client_id={self.client_id})")
        except Exception:
            logger.exception("Error while terminating session")


    def validate_params(
        self,
        required: Optional[list[str]] = None,
        **values: Any,
    ) -> None:

        if required:
            self.validator.check(required_keys=required, **values)
        else:
            self.validator.check_all(**values)


def _derive_function_info_from_handler(handler) -> str:

    module_path = inspect.getmodule(handler).__name__ if inspect.getmodule(handler) else "unknown_module"
    handler_name = handler.__name__

    return f"{module_path}.{handler_name}"


def get_session_context(
    request: Request,
    function_info: Optional[str] = None,
    noise_level: NoiseLevel = NoiseLevel.DEBUG,
) -> SessionContext:

    client_id = request.headers.get("X-Client-Id", "anonymous")

    if function_info is None:
        frm = inspect.currentframe()
        caller = frm.f_back if frm else None
        func = caller.f_locals.get('func') if caller else None  # decorator path
        if func is None:
            # Fallback: best effort using the stack
            stack_func = None
            for fr in inspect.stack():
                if fr.function not in {"wrapper", "inner", "<lambda>"}:
                    stack_func = fr
                    break
            function_info = f"{stack_func.filename}:{stack_func.lineno}" if stack_func else "unknown"
        else:
            function_info = _derive_function_info_from_handler(func)

    return SessionContext(client_id=client_id, function_info=function_info, request=request, noise_level=noise_level)
