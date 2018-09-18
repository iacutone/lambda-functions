import requests
import json
import os

class MailchimpEmails:
    @classmethod
    # {'<uniq id>: 'test@test.com}
    def get(cls):

        request = requests.get('https://us13.api.mailchimp.com/3.0/lists/208637560c/members', auth=('anystring', os.environ['MAILCHIMP_API_KEY']))

        email_request = json.loads(request.text)
        emails = {}
        for member in email_request['members']:
            if member['status'] == 'subscribed':
                emails[member['id']] = member['email_address']

        return emails
