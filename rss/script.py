from functools import wraps
from string import ascii_lowercase
from termcolor import cprint
from twisted.internet import defer, reactor

from rss.core import fetch


commands = {}

def command(name=None):
    def add_command(fn):
        commands[name or fn.__name__] = fn
        return fn
    return add_command


def main(arguments):
    # XXX: A hack until docopt properly supports subcommands / dispatching
    run_command(arguments).addCallback(lambda succeeded : reactor.stop())
    reactor.run()


def run_command(arguments):
    command = next(
        cmd for cmd, selected in arguments.iteritems()
        if cmd[0] in ascii_lowercase and selected
    )
    return commands[command](arguments)


@command()
def get(arguments):
    d = []
    for url in arguments["<url>"]:
        d.append(fetch(url).addCallback(print_feed))

    return defer.gatherResults(d, consumeErrors=True)


@command()
def add(arguments):
    pass


@command()
def list(arguments):
    pass

@command()
def rm(arguments):
    pass


def print_feed(feed):
    cprint(feed["feed"]["title"], "blue")

    for entry in feed["entries"]:
        if "title" in entry:
            print entry["title"]
        else:
            print entry["description"]
