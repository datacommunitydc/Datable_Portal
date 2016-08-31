import json
import requests
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

        req = requests.get(self.url)

        if req.status_code == 200:
            return json.loads(req.content)
        else:
            msg = 'Linkedin: Token cannot be verified ' + req.content
            raise BadTokenError(msg, req.status_code)