import feedparser
from newspaper import Article
from googletrans import Translator
import requests
import json
import boto3
import os

request = requests.get('https://us13.api.mailchimp.com/3.0/lists/208637560c/members', auth=('anystring', os.environ['MAILCHIMP_API_KEY']))

json = json.loads(request.text)
emails = []
for member in json['members']:
    emails.append(member['email_address'])

rss = 'http://ep00.epimg.net/rss/elpais/portada_america.xml'
feed = feedparser.parse(rss)
url = feed['entries'][0]['link']

article = Article(url)
article.download()
article.parse()
original_text = article.text
paragraph = original_text.split('\n')

translator = Translator()
eng_translation = []
for text in paragraph:
    eng_translation.append(translator.translate(text).text)
merged_paragraph = list(zip(paragraph, eng_translation))

txt_message = ''
for org, tran in filter(None, merged_paragraph):
    txt_message += org
    txt_message += '\n\n'
    txt_message += tran

html_message = ''
for org, tran in filter(None, merged_paragraph):
    html_message += org
    html_message += '<br><br>'
    html_message += tran

client = boto3.client(service_name = 'ses', 
                          region_name = 'us-east-1', 
                          aws_access_key_id = os.environ['AWS_ACCESS_KE'], 
                          aws_secret_access_key = os.environ['AWS_SECRET_KE'])

response = client.send_email(
    Destination={
        'BccAddresses': emails,
    },
    Message={
        'Body': {
            'Html': {
                'Charset': 'UTF-8',
                'Data': html_message,
            },
            'Text': {
                'Charset': 'UTF-8',
                'Data': txt_message,
            },
        },
        'Subject': {
            'Charset': 'UTF-8',
            'Data': "Today's Article",
        },
    },
    Source='hello@masterspanish.today',
)

print(response)

