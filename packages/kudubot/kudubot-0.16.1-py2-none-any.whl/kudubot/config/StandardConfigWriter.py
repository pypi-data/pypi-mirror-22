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
from kudubot.config.GlobalConfigHandler import GlobalConfigHandler
from io import open


class StandardConfigWriter(object):
    u"""
    A config handler class that writes the standard configuration for connections
    and services into the config.
    """

    def __init__(self, config_handler = GlobalConfigHandler()):
        u"""
        Initializes the Standard Config Writer's configuration file locations
        :param config_handler: The GlobalConfigHandler to use. Default to the default one.
        """
        self.connection_config = config_handler.global_connection_config_location
        self.service_config = config_handler.services_config_location

    def write_standard_connection_config(self):
        u"""
        Writes the standard connection configuration file

        :return: None
        """

        with open(self.connection_config, u'w') as config:
            for connection in \
                    [u"from kudubot.connections.cli.CliConnection import CliConnection",
                     u"from kudubot.connections.whatsapp.WhatsappConnection import WhatsappConnection",
                     u"from kudubot.connections.telegram.TelegramConnection import TelegramConnection"]:
                config.write(connection + u"\n")

    def write_standard_service_config(self):
        u"""
        Writes the standard service configuration file

        :return: None
        """

        native = u"from kudubot.services.native."
        external = u"from kudubot.services.external."

        with open(self.service_config, u'w') as config:
            for service in \
                    [native + u"simple_responder.SimpleResponderService import SimpleResponderService",
                     native + u"reminder.ReminderService import ReminderService",
                     native + u"anime_reminder.AnimeReminderService import AnimeReminderService",
                     native + u"jokes.JokesService import JokesService",
                     external + u"helloworld_rust.HelloWorldService import HelloWorldService",
                     external + u"hello_kotlin.HelloKotlinService import HelloKotlinService"]:
                config.write(service + u"\n")
