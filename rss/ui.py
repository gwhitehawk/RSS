import urwid


class Feed(urwid.WidgetWrap):
    def __init__(self, feed):
        self.title = feed.feed.get("title", "Untitled")
        self.entries = urwid.SimpleListWalker([
            urwid.Text(entry["title"]) for entry in feed["entries"]
        ])
        self.box = urwid.ListBox(self.entries)

        super(Feed, self).__init__(urwid.LineBox(self.box, title=self.title))


class UrwidUI(object):
    def __init__(self):
        self.feeds_list = urwid.SimpleListWalker([])
        self.feeds_box = urwid.ListBox(self.feeds_list)

        self.loop = urwid.MainLoop(
            self.feeds_box, event_loop=urwid.TwistedEventLoop()
        )

    def got_feed(self, feed):
        feed = Feed(feed)
        self.feeds_list.append(urwid.BoxAdapter(feed, 11))
        self.loop.draw_screen()

    def run(self):
        self.loop.run()
