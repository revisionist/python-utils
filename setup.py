# Copyright 2023-2024 David Goddard.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain a
# copy of the License at:
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, find_packages

setup(
    name='domestique',
    version='0.1',
    packages=find_packages(),
    description='A collection of utility functions to assist your main project',
    #long_description=open('README.md').read(),
    #long_description_content_type='text/markdown',
    author='David Goddard',
    author_email='goddard@acm.org',
    url='https://github.com/revisionist/python-utils/domestique',
    install_requires=[
    ]
)
