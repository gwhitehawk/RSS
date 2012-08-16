from operator import attrgetter

from treq import get
import feedparser

from rss import __version__


USER_AGENT = "RSS, Simply Syndicated %s" % (__version__,)


def parse(feed):
    return feedparser.parse(feed)


def fetch(feed_url):
    feed = get(feed_url, headers={"User-Agent" : [USER_AGENT]})
    return feed.addCallback(attrgetter("content")).addCallback(parse)
