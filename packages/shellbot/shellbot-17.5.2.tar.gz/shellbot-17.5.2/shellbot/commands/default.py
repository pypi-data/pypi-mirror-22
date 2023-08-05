# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .base import Command


class Default(Command):
    """
    Handles unmatched command
    """

    keyword = u'*default'
    information_message = u'Handle unmatched command'
    is_hidden = True

    def execute(self, arguments):
        """
        Handles unmatched command
        """
        self.bot.say(
            u"Sorry, I do not know how to handle '{}'".format(self.shell.verb))
