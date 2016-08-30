import json
from urllib2 import Request, urlopen, URLError

from datable_project.exceptions import GoogleBadTokenError


class Google:
    def __init__(self, access_token):
        self.access_token = access_token

    def verify(self):
        """if verified return user else raise error"""

        headers = {'Authorization': 'OAuth '+ self.access_token}
        req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                    None, headers)
        try:
            res = urlopen(req)
        except URLError, e:
            if e.code == 401:
                # Unauthorized - bad token
                raise GoogleBadTokenError()
            return json.loads(res.read())
        return json.loads(res.read())
