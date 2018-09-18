from newspaper import Article

class ParseArticle:
    @classmethod
    def new(cls, rss_feed):
        article = Article(rss_feed)
        article.download()
        article.parse()
        return article.text
