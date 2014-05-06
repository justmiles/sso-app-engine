# http://docs.aws.amazon.com/STS/latest/UsingSTS/STSMgmtConsole-manualURL.html

import cgi
from google.appengine.api import users
import webapp2

class AWSAuth(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # TODO: parse settings.cfg for redirect url (alias)
        self.redirect("https://findingapogee.signin.aws.amazon.com/console")