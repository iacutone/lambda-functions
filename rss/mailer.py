import boto3
import requests
import os

class Mailer:
    def __init__(self, emails, article):
        client = boto3.client(service_name = 'ses', 
                              region_name = 'us-east-1', 
                              aws_access_key_id = os.environ['AWS_ACCESS_KE'], 
                              aws_secret_access_key = os.environ['AWS_SECRET_KE'])

        for _, value in emails.items():
            client.send_email(
                Destination={
                    'ToAddresses': [value],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': 'UTF-8',
                            'Data': article.html() + self.unsubscribe_link(),
                        },
                        'Text': {
                            'Charset': 'UTF-8',
                            'Data': article.text(),
                        },
                    },
                    'Subject': {
                        'Charset': 'UTF-8',
                        'Data': "Today's Article",
                    },
                },
                Source='hello@masterspanish.today',
            )

    def unsubscribe_link(self):
        return "<br><br><a href='https://amazonaws.us13.list-manage.com/unsubscribe?u=93b41a1871734324d088abc68&id=208637560c'>Unsubscribe</a>"
