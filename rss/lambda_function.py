import logging
from rss_feed import RssFeed
from parse_article import ParseArticle
from translate_article import TranslateArticle
from mailchimp_emails import MailchimpEmails
from mailer import Mailer

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event=None, context=None):
    logger.info('Lambda function invoked!')

    rss_feed = RssFeed.parse('http://ep00.epimg.net/rss/elpais/portada_america.xml')
    logger.info('rss_feed success')
    article_text = ParseArticle.new(rss_feed)
    logger.info('article_text success')
    translated_article = TranslateArticle(article_text)
    logger.info('translation success')
    emails = MailchimpEmails.get()
    logger.info('emails success')

    Mailer(emails, translated_article)

    return 'Success!'
