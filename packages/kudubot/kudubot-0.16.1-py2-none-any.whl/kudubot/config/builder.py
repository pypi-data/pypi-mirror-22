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

from __future__ import with_statement
from __future__ import absolute_import
import os
import stat
import json
from typing import List
from subprocess import Popen
from io import open


# noinspection PyUnusedLocal
def build(service_directory):
    u"""
    Builds a Service using the service configuration inside the service directory.

    :param service_directory: The location of the service directory
    :return: The path to the generated executable file
    """

    service_name = os.path.basename(service_directory)
    current_dir = os.getcwdu()
    os.chdir(service_directory)

    with open(u"service.json", u'r') as f:
        config = json.load(f)

    try:
        Popen(config[u"build_commands"]).wait()
    except BaseException, e:
        print e

    output = config[u"output_file"]
    st = os.stat(output)
    os.chmod(output, st.st_mode | stat.S_IEXEC)  # Make executable

    if os.path.basename(output) != service_name:
        new_output = os.path.join(os.path.dirname(output), service_name)
        os.rename(output, new_output)
        output = new_output

    os.chdir(current_dir)

    return os.path.join(service_directory, output)


def build_external(move_to = u""):
    u"""
    Builds all external services

    :param move_to: If specified, all built files are moved to that directory
    :return: A list of all generated executable files
    """

    external_dir = os.path.join(u"kudubot", u"services", u"external")
    built_executables = []

    for service in os.listdir(external_dir):

        service_dir = os.path.join(external_dir, service)
        if not os.path.isdir(service_dir) or service == u"__pycache__":
            continue

        result = build(service_dir)

        if move_to != u"" and os.path.isfile(result):
            destination = os.path.join(move_to, service)
            os.rename(result, destination)
            built_executables.append(destination)

        elif os.path.isfile(result):
            built_executables.append(result)

    return built_executables
