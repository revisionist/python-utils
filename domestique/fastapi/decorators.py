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
from functools import wraps
from typing import Any, Awaitable, Callable, TypeVar, Coroutine

from fastapi import Request

from ..validation import NoiseLevel
from .session import get_session_context, SessionContext

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Awaitable[Any]])


def route_decorator(func: F) -> F:

    module_path = inspect.getmodule(func).__name__ if inspect.getmodule(func) else "unknown_module"
    handler_name = func.__name__
    function_info = f"{module_path}.{handler_name}"

    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Request = None
        for a in args:
            if isinstance(a, Request):
                request = a
                break
        if request is None:
            for v in kwargs.values():
                if isinstance(v, Request):
                    request = v
                    break
        if request is None:
            raise RuntimeError("route_decorator requires a FastAPI Request parameter in the handler")

        session: SessionContext = get_session_context(request, function_info=function_info, noise_level=NoiseLevel.DEBUG)
        request.state.session = session

        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.debug(f"Unhandled exception in {function_info}")
            return session.resp.generate_response_with_exception(e)
        finally:
            session.terminate()

    return wrapper  # type: ignore[return-value]
