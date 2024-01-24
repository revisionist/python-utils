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
import inspect
import traceback
import sys

from . import _persistent

from .identifiers import generate_id, generate_shorter_id


logger = logging.getLogger(__name__)


def get_calling_method_text(depth=2):

        stack = inspect.stack()
        caller_info = stack[depth]
        calling_method = caller_info.function
        calling_module = caller_info.frame.f_globals["__name__"]
        return f"{calling_module}.{calling_method}"


def get_calling_method_name_quick(indirect=False):

    # Faster than using the inspect stack
    if (indirect):
        return sys._getframe().f_back.f_back.f_code.co_name
    else:
        return sys._getframe().f_back.f_code.co_name


def get_exception_details(exception, tbindex=-1):

    exception_identifier = generate_shorter_id()
    tb = traceback.extract_tb(exception.__traceback__)
    last_traceback = tb[tbindex]
    file_name, line_number, func_name, text = last_traceback

    return exception_identifier, file_name, line_number, func_name, text


def log_exception(client_id, e, calling_method_name=None, include_traceback=True):

    logger.debug(f"log_exception for {client_id}: {e}")

    def append_traceback():

        tb_lines = ""
        tb_line = 0
        exc_traceback = e.__traceback__

        while exc_traceback is not None:
            frame = exc_traceback.tb_frame
            filename = frame.f_code.co_filename
            lineno = exc_traceback.tb_lineno
            function = frame.f_code.co_name
            module = frame.f_globals['__name__']
            tb_lines += f"{line_prefix}traceback[{tb_line}] {module}.{function} - {filename},{lineno}"
            tb_line += 1
            exc_traceback = exc_traceback.tb_next
    
        return tb_lines

    exception_identifier, file_name, line_number, func_name, text = get_exception_details(e)

    if isinstance(e, (ValueError, TypeError)):
        message_for_user = f"{e}"
    else:
        message_for_user = f"Guru Meditation Reference: {exception_identifier}"

    if not calling_method_name:
        calling_method_name = get_calling_method_name_quick(True)

    if client_id:
        message = f"An error occurred for client_id '{client_id}' in '{calling_method_name}' - {message_for_user}"
    else:
        message = f"An error occurred in '{calling_method_name}' - {message_for_user}"
    logger.exception(message, exc_info=False)

    details = f"Exception details for {exception_identifier}:"
    line_prefix = f"\n {exception_identifier} - "
    details += line_prefix + f"File: {file_name}"
    details += line_prefix + f"Line: {line_number}"
    details += line_prefix + f"Function: {func_name}"
    details += line_prefix + f"Error line: {text}"
    details += line_prefix + f"Error message: {e}"

    if include_traceback:
        details += append_traceback()
    
    logger.error(details)

    return message, exception_identifier
