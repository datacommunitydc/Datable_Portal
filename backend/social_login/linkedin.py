from urllib2 import Request, urlopen, URLError
from datable_project.exceptions import BadTokenError

# https://www.linkedin.com/uas/oauth2/accessToken?grant_type=authorization_code&code=TOKEN_RECIEVED_THROUGH_IN.ENV.auth&redirect_uri=my-domain&client_id=API_CLIENT_ID&client_secret=API_SECRET_KEY'


class Linkedin:
    url = 'https://api.linkedin.com/v1/people/~?oauth2_access_token={}&format=json'

    def __init__(self, access_token):
        self.access_token = access_token
        self.url = self.url.format(access_token)

    def verify(self):
        """if verified return user else raise error"""
        print(self.url)
        req = Request(self.url)
        try:
            res = urlopen(req)
        except URLError, e:
            if e.code == 401:
                # Unauthorized - bad token
                raise BadTokenError('Linkedin: Token cannot be verified')
            return res.read()
        return res.read()