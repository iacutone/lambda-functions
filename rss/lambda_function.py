import logging
import os
import requests
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

    rss_feed = RssFeed.parse(os.environ['EL_PAIS_RSS_URL'])
    logger.info('rss_feed success')
    article_text = ParseArticle.new(rss_feed)
    logger.info('article_text success')
    translated_article = TranslateArticle(article_text)
    logger.info('translation success')
    emails = MailchimpEmails.get()
    logger.info('emails success')

    Mailer(emails, translated_article)

    requests.get("https://cronhub.io/ping/9b7e1860-7ffb-11ea-83b7-11422ae8ff81") 
    return 'Success!'
