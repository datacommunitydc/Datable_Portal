import oauth2 as oauth
import time

from django.conf import settings

# https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=TOKEN_RECIEVED_THROUGH_IN.ENV.auth&redirect_uri=my-domain&client_id=API_CLIENT_ID&client_secret=API_SECRET_KEY'


class LinkedIn:
    url = "http://api.linkedin.com/v1/people/~"
    consumer_key = settings.SOCIAL_AUTH_PROVIDERS['linkedin']['client_id']
    consumer_secret = settings.SOCIAL_AUTH_PROVIDERS['linkedin']['client_secret']

    def __init__(self, oauth_key, oauth_secret):
        self.oauth_key = oauth_key
        self.oauth_secret = oauth_secret
        self.consumer = oauth.Consumer(
            key=self.consumer_key,
            secret=self.consumer_secret
        )
        self.token = oauth.Token(key=oauth_key, secret=oauth_secret)

    def linked_client(self):
        client = oauth.Client(self.consumer, self.token)
        return client.request(self.url)


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth.Token(key=key, secret=secret)
    client = oauth.Client(consumer, token)
    resp, content = client.request(url, method=http_method, body=post_body, headers=http_headers )
    return content

CONSUMER_KEY='pylTV0VBzBWnTkN4IuKmxSSIs'
CONSUMER_SECRET='0D7j9Mbeu1Qd2o3Wbj7PT4GLCSckT4ESVi7C34i3V82ZPePT3v'
access_token = '102034996-VNHebQh1xInLeIWU90uXWA91dGNNSs07QNFHIVaL'
access_secret = '3QszCxUEeU9kHHcXaGqUuYagKWT1meTuufkO1CZ9pmcQT'
oauth_req("https://api.twitter.com/1.1/", access_token, access_secret, http_method="GET")