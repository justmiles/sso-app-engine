import cgi
from google.appengine.api import users
import webapp2

# display a root page
class DefaultPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if user:
            greeting = ('Welcome, %s!  <p>Choose a service to login or <a href="%s">sign out</a><ul><li>%s</li><li>%s</li></ul></p>' %
                        (user.nickname(),
                         users.create_logout_url('http://www.edointeractive.com/'),'<a href="salesforce">Salesforce<a>','<a href="aws">Amazon Web Services</a>'))
        else:
            greeting = ('<a href="%s">Sign in</a>.' %
                        users.create_login_url('/'))

        self.response.out.write('<html><body>%s</body></html>' % greeting)
