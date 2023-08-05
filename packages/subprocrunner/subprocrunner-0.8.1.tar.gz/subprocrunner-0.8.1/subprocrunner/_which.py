# encoding: utf-8

"""
.. codeauthor:: Tsuyoshi Hombashi <gogogo.vm@gmail.com>
"""

from __future__ import absolute_import
from __future__ import unicode_literals

import shutil

import six
import typepy

from ._error import CommandNotFoundError
from ._error import InvalidCommandError


class Which(object):

    @property
    def command(self):
        return self.__command

    def __init__(self, command):
        if not typepy.is_not_null_string(command):
            raise InvalidCommandError("invalid str {}: ".format(command))

        self.__command = command

    def is_exist(self):
        if self.which() is None:
            return False

        return True

    def verify(self):
        if not self.is_exist():
            raise CommandNotFoundError(
                "command not found: '{}'".format(self.command))

    def which(self):
        if six.PY2:
            from distutils.spawn import find_executable
            return find_executable(self.command)

        return shutil.which(self.command)
