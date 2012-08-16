from cStringIO import StringIO
import os.path
import sys
import textwrap

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.trial.unittest import TestCase
from twisted.web import static, server

from rss.script import run_command


class TestCommandOutput(TestCase):
    @inlineCallbacks
    def setUp(self):
        endpoint = TCP4ServerEndpoint(reactor, 0)
        root = static.File(os.path.join(os.path.dirname(__file__), "fixtures"))
        site = server.Site(root)

        self.port = yield endpoint.listen(site)
        self.addCleanup(self.port.stopListening)

        self.stdout = sys.stdout = StringIO()
        self.addCleanup(lambda : setattr(sys, "stdout", sys.__stdout__))

    def url(self, path):
        return "http://localhost:%s/%s" % (self.port.getHost().port, path)

    def run_command(self, **arguments):
        return run_command(arguments)

    @inlineCallbacks
    def test_rss_simple_get(self):
        yield self.run_command(
            get=True,
            **{"<url>" : [self.url("rss.xml")]}
        )

        self.assertEqual(
            self.stdout.getvalue(),
            textwrap.dedent("""
            \x1b[34mRSS Test\x1b[0m
            First Item
            Second Item
            Third item has only a description.
            """).lstrip()
        )

    @inlineCallbacks
    def test_add_list_remove(self):
        yield self.run_command(list=True)
        self.assertFalse(self.stdout.getvalue())

        yield self.run_command(
            add=True,
            **{"<feeds>" : ["http://foo.com/feed.rss"]}
        )
        self.assertFalse(self.stdout.getvalue())

        yield self.run_command(
            rm=True,
            **{"<feeds>" : ["http://foo.com/feed.rss"]}
        )
        self.assertFalse(self.stdout.getvalue())
