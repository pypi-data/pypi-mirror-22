import logging
import mock
from raven.handlers.logging import SentryHandler
import unittest
from ZConfig import configureLoggers

class TestConfig(unittest.TestCase):

    @mock.patch("raven.handlers.logging.Client")
    def test_minimal(self, Client):
        configureLoggers("""
        <logger>
          %import j1m.ravenzconfig
          <sentry>
            dsn https://abc:def@example.com/42
          </sentry>
        </logger>
        """)
        [handler] = [h for h in logging.getLogger().handlers
                     if isinstance(h, SentryHandler)]
        logging.getLogger().handlers.remove(handler)
        self.assertEqual(handler.level, logging.ERROR)
        Client.assert_called_with(
            dsn='https://abc:def@example.com/42',
            site=None,
            name=None,
            release=None,
            environment=None,
            exclude_paths=None,
            include_paths=None,
            sample_rate=1.0,
            list_max_length=None,
            string_max_length=None,
            auto_log_stacks=None,
            processors=None,
            level=logging.ERROR
            )

    @mock.patch("raven.handlers.logging.Client")
    def test_many(self, Client):
        configureLoggers("""
        <logger>
          %import j1m.ravenzconfig
          <sentry>
            level WARNING
            dsn https://abc:def@example.com/42
            site test-site
            name test
            release 42.0
            environment testing
            exclude_paths /a /b
            include_paths /c /d
            sample_rate 0.5
            list_max_length 9
            string_max_length 99
            auto_log_stacks true
            processors x y z
          </sentry>
        </logger>
        """)
        [handler] = [h for h in logging.getLogger().handlers
                     if isinstance(h, SentryHandler)]
        logging.getLogger().handlers.remove(handler)
        self.assertEqual(handler.level, logging.WARNING)
        Client.assert_called_with(
            dsn='https://abc:def@example.com/42',
            site='test-site',
            name='test',
            release='42.0',
            environment='testing',
            exclude_paths=['/a', '/b'],
            include_paths=['/c', '/d'],
            sample_rate=0.5,
            list_max_length=9,
            string_max_length=99,
            auto_log_stacks=True,
            processors=['x', 'y', 'z'],
            level=logging.WARNING
            )

