import feedparser

class RssFeed:
    @classmethod
    def parse(cls, url):
        rss_feed = feedparser.parse(url)
        return rss_feed['entries'][0]['link']
