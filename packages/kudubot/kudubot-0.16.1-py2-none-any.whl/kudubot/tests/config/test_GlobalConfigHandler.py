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
import shutil
import unittest
from kudubot.tests.helpers.DummyConnection import DummyConnection
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from kudubot.tests.helpers.DummyService import DummyService, DummyServiceWithValidDependency
from kudubot.tests.helpers.test_config import generate_test_environment, clean_up_test_environment
from io import open


class UnitTests(unittest.TestCase):
    u"""
    Tests the GlobalConfigHandler class
    """

    def setUp(self):
        u"""
        Creates a restore point for the class variables of the GlobalConfigHandler and sets these values
        to ones that make sense for the unit tests
        :return: None
        """
        self.config_handler = generate_test_environment()

    def tearDown(self):
        u"""
        Restores the class variables and deletes any temporary directories and files
        :return: None
        """
        clean_up_test_environment()

    def test_generating_new_config(self):
        u"""
        Tests if the configuration generation works as intended
        :return: None
        """
        clean_up_test_environment()

        self.config_handler.generate_configuration(True)
        self.validate_config_directory()
        self.config_handler.generate_configuration(True)
        self.validate_config_directory()
        self.config_handler.generate_configuration(False)
        self.validate_config_directory()

    def validate_config_directory(self):
        u"""
        Validates a configuration directory
        :return: None
        """
        self.assertTrue(self.config_handler.validate_config_directory())
        self.assertTrue(os.path.isdir(u"kudu-test"))
        self.assertTrue(os.path.isfile(os.path.join(u"kudu-test", u"services.conf")))
        self.assertTrue(os.path.isfile(os.path.join(u"kudu-test", u"connections.conf")))
        self.assertTrue(os.path.isdir(os.path.join(u"kudu-test", u"connection_config")))
        self.assertTrue(os.path.isdir(os.path.join(u"kudu-test", u"data")))

    def assure_invalid_config_directory(self):
        u"""
        Makes sure that the current configuration directory is invalid
        :return: None
        """
        self.assertFalse(self.config_handler.validate_config_directory())

    def test_directory_validation(self):
        u"""
        Tests if the global config validation works correctly and finds errors in the config structure
        :return: None
        """
        clean_up_test_environment()

        self.assure_invalid_config_directory()

        for element in [u"services.conf", u"connections.conf", u"data", u"connection_config"]:

            self.config_handler.generate_configuration(True)
            path = os.path.join(u"kudu-test", element)

            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)

            self.assure_invalid_config_directory()

    def test_connection_loading(self):
        u"""
        Tests the loading of connections

        :return: None
        """
        connections = self.config_handler.load_connections()
        self.assertEqual([], connections)

        with open(os.path.join(u"kudu-test", u"connections.conf"), u'w') as f:
            f.write(u"from kudubot.tests.helpers.DummyConnection import DummyConnection")

        self.assertEqual(self.config_handler.load_connections()[0], DummyConnection)

    def test_service_loading(self):
        u"""
        Tests the loading of services

        :return: None
        """
        services = self.config_handler.load_services()

        self.assertEqual([], services)

        with open(os.path.join(u"kudu-test", u"services.conf"), u'w') as f:
            f.write(u"from kudubot.tests.helpers.DummyService import DummyService")

        self.assertEqual(self.config_handler.load_services()[0], DummyService)

    def test_importing(self):
        u"""
        Tests the String import handler method

        :return: None
        """
        os_import = self.config_handler.__handle_import_statement__(u"import os")
        dict_import = self.config_handler.__handle_import_statement__(u"from typing import Dict")
        from typing import Dict

        self.assertEqual(os, os_import)
        self.assertEqual(dict_import, Dict)

    def test_service_dependency_imports(self):
        u"""
        Tests the dependency resolution of the services.

        :return: None
        """
        # First, test service having a valid dependency
        with open(os.path.join(u"kudu-test", u"services.conf"), u'w') as f:
            f.write(u"from kudubot.tests.helpers.DummyService import DummyServiceWithValidDependency")
        services = self.config_handler.load_services()
        self.assertEqual(services, [DummyServiceWithValidDependency])

        # Now test unresolved dependency
        with open(os.path.join(u"kudu-test", u"services.conf"), u'w') as f:
            f.write(u"from kudubot.tests.helpers.DummyService import DummyServiceWithInvalidDependency")
        services = self.config_handler.load_services()
        self.assertEqual(services, [])

    def test_duplicate_removal(self):
        u"""
        Tests the duplicate removal method

        :return: None
        """
        # noinspection PyDecorator
        def other():
            return u"other"

        second_dummy = DummyConnection([], self.config_handler)
        second_dummy.define_identifier = other

        connections = [second_dummy, DummyConnection, DummyConnection]
        # noinspection PyTypeChecker
        new_connections = self.config_handler.__remove_duplicate_services_or_connections__(connections)
        self.assertEqual(new_connections, [second_dummy, DummyConnection])

    def test_loading_invalid_classes(self):

        with open(os.path.join(u"kudu-test", u"connections.conf"), u'w') as f:
            f.write(u"from kudubot.tests.helpers.DummyService import DummyService")

        self.assertEqual(self.config_handler.load_connections(), [])

        with open(os.path.join(u"kudu-test", u"connections.conf"), u'w') as f:
            f.write(u"from kudubot.doesnotexists import AClass")

        self.assertEqual(self.config_handler.load_connections(), [])
