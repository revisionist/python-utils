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
import inspect
import enum

from .logging import get_calling_method_text, get_calling_method_name_quick


logger = logging.getLogger(__name__)


class NoiseLevel(enum.Enum):
    SILENT = 0
    DEBUG = 1
    INFO = 2


class Validator:

    def __init__(self, calling_method_text=None, logging_identifiers=[], default_noise_level=NoiseLevel.DEBUG):

        self.logger = logging.getLogger(__name__)

        if not calling_method_text:
            calling_method_text = get_calling_method_text(2)#get_calling_method_name_quick(True)
            # Note that get_calling_method_text(2) should also work

        self.calling_method_text = calling_method_text
        self.logging_identifiers = logging_identifiers
        self.default_noise_level = default_noise_level

    def check_required(self, **values):

        for key, value in values.items():
            if not value:
                raise ValueError(f"Missing required value: {key}")


    def get_logging_id_string(self):
    
        if not self.logging_identifiers:
            return None
        return " ~ ".join(self.logging_identifiers)


    def check(self, required_keys=[], noise_level=None, **values):

        if noise_level is None:
            noise_level = self.default_noise_level

        log_func = {
            NoiseLevel.SILENT: lambda *args, **kwargs: None,
            NoiseLevel.INFO: self.logger.info,
            NoiseLevel.DEBUG: self.logger.debug
        }.get(noise_level, self.logger.debug)

        logging_id_string = self.get_logging_id_string()
        validation_message = f"Validating parameters for: {self.calling_method_text}"
        if logging_id_string:
            validation_message += f" -- [{logging_id_string}]"

        log_func(validation_message)
        method_name = self.calling_method_text.split('.')[-1]

        # Check and log required values
        for key in required_keys:
            if key not in values or values[key] is None:
                message = f"Missing required value: {key}"
                self.logger.error(f"{self.calling_method_text}: {message}")
                raise ValueError(message)
            log_func(f"{method_name}: *{key} = {values[key]}")

        # Log optional values
        for key, value in values.items():
            if key not in required_keys:
                log_func(f"{method_name}: {key} = {value}")


    def check_all(self, noise_level=None, **values):

        required_keys = list(values.keys())

        self.check(required_keys=required_keys, noise_level=noise_level, **values)
