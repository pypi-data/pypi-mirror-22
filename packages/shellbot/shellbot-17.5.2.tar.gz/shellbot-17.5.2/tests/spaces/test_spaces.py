#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import logging
import mock
import os
from multiprocessing import Process
import sys
import time

sys.path.insert(0, os.path.abspath('../..'))

from shellbot import Context, ShellBot
from shellbot.spaces import SpaceFactory


class SpaceFactoryTests(unittest.TestCase):

    def test_build(self):

        logging.info("*** build")

        bot = ShellBot(settings={  # from settings to member attributes
            'spark': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODVGlZWU1NmYtyY',
                'personal_token': '*personal*secret*token',
                'webhook': "http://73a1e282.ngrok.io",
            }
        })

        space = SpaceFactory.build(bot=bot)
        self.assertEqual(space.token, 'hkNWEtMJNkODVGlZWU1NmYtyY')
        self.assertEqual(space.personal_token, '*personal*secret*token')
        self.assertEqual(space.id, None)   #  set after bond()
        self.assertEqual(space.title, space.DEFAULT_SPACE_TITLE)
        self.assertEqual(space.teamId, None)

    def test_sense(self):

        logging.info("*** sense")

        context = Context(settings={  # sense='spark'
            'spark': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            }
        })

        self.assertEqual(SpaceFactory.sense(context), 'spark')

        context = Context(settings={  # sense='space'
            'space': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            }
        })

        self.assertEqual(SpaceFactory.sense(context), 'space')

        context = Context(settings={  # 'space' is coming before 'spark'
            'spark': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },

            'space': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },
        })

        self.assertEqual(SpaceFactory.sense(context), 'space')

        context = Context(settings={  # 'space' is coming before 'spark'
            'space': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },

            'spark': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },
        })

        self.assertEqual(SpaceFactory.sense(context), 'space')

        context = Context(settings={  # no recognizable space type
            'not_a_space_type': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },

            'neither_me': {
                'room': 'My preferred room',
                'moderators':
                    ['foo.bar@acme.com', 'joe.bar@corporation.com'],
                'participants':
                    ['alan.droit@azerty.org', 'bob.nard@support.tv'],
                'team': 'Anchor team',
                'token': 'hkNWEtMJNkODk3ZDZLOGQ0OVGlZWU1NmYtyY',
                'personal_token': '$MY_FUZZY_SPARK_TOKEN',
                'fuzzy_token': '$MY_FUZZY_SPARK_TOKEN',
                'webhook': "http://73a1e282.ngrok.io",
            },
        })

        with self.assertRaises(ValueError):
            SpaceFactory.sense(context)

    def test_get_space(self):

        logging.info("*** get('space')")

        space = SpaceFactory.get(type='space')
        self.assertEqual(space.prefix, 'space')
        self.assertEqual(space.id, None)
        self.assertEqual(space.title, space.DEFAULT_SPACE_TITLE)
        self.assertEqual(space.hook_url, None)

        space = SpaceFactory.get(type='space', context='c', weird='w')
        with self.assertRaises(AttributeError):
            self.assertEqual(space.context, 'c')
        with self.assertRaises(AttributeError):
            self.assertEqual(space.weird, 'w')
        self.assertEqual(space.prefix, 'space')
        self.assertEqual(space.id, None)
        self.assertEqual(space.title, space.DEFAULT_SPACE_TITLE)
        self.assertEqual(space.hook_url, None)

    def test_get_local(self):

        logging.info("*** get('local')")

        space = SpaceFactory.get(type='local')
        self.assertEqual(space.prefix, 'space')
        self.assertEqual(space.id, None)
        self.assertEqual(space.title, space.DEFAULT_SPACE_TITLE)
        self.assertEqual(space.hook_url, None)
        self.assertEqual(space.moderators, [])
        self.assertEqual(space.participants, [])

    def test_get_spark(self):

        logging.info("*** get('spark')")

        bot = ShellBot()
        space = SpaceFactory.get(type='spark', bot=bot, ex_token='b')
        self.assertEqual(space.token, 'b')
        self.assertEqual(space.id, None)
        self.assertEqual(space.title, space.DEFAULT_SPACE_TITLE)
        self.assertEqual(space.teamId, None)

    def test_get_unknown(self):

        logging.info("*** get('*unknown')")

        with self.assertRaises(ValueError):
            space = SpaceFactory.get(type='*unknown', ex_token='b', ex_ears='c')

if __name__ == '__main__':

    Context.set_logger()
    sys.exit(unittest.main())
