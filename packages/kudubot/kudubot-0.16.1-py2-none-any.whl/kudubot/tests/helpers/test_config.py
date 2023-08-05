u"""
LICENSE:
Copyright 2015-2017 Hermann Krumrey

This file is part of kudubot.

    kudubot is a chat bot framework. It allows developers to write
    services for arbitrary chat services.

    kudubot is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    kudubot is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with kudubot.  If not, see <http://www.gnu.org/licenses/>.
LICENSE
"""

from __future__ import absolute_import
import os
import shutil
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler


def generate_test_environment():
    u"""
    Generates the test environment

    :return: The GlobalConfigHandler that points to the configuration
    """

    handler = GlobalConfigHandler(u"kudu-test")
    handler.generate_configuration()
    return handler


def clean_up_test_environment():
    u"""
    Deletes the test environment

    :return: None
    """
    if os.path.isdir(u"kudu-test"):
        shutil.rmtree(u"kudu-test")
