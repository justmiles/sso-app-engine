import cgi
from google.appengine.api import users
import webapp2

class AWSAuth(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.redirect("https://edointeractive.signin.aws.amazon.com/console")