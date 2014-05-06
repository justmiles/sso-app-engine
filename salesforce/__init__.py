import webapp2
from google.appengine.api import users

class SalesForceAuth(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.redirect("http://salesforce.com")