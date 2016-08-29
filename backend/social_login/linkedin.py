from urllib2 import Request, urlopen, URLError
from datable_project.exceptions import BadTokenError

#https://api.linkedin.com/v1/people/~:?oauth2_access_token=AQXxasONr6ZJcECoOnhwDMqYdPCdLhYn-j4SRdQLRQwpeuUKaxLIkYS-cWe4kvxpPBpE5GlniuZEkQn4lOo0KPf7XYzputTEG1cxm3e3e5RyprmdeGAAYmIjJpM67T-_AFZUXeF-jvL5X7grQbWY4Dmlv5xGnoND5nsoas7LZJKsyhhILqQ&format=json

class Linkedin:
    url = 'https://api.linkedin.com/v1/people/~:(email-address,firstName,' \
          'headline,lastName,id,siteStandardProfileRequest)?' \
          'oauth2_access_token={}&format=json'

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