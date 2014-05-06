import cgi
from google.appengine.api import users
import webapp2

import ConfigParser, os
config = ConfigParser.ConfigParser()
config.read('settings.cfg')
services = config.items('services')

# import services
from defaultpage import DefaultPage
from salesforce import SalesForceAuth
from aws import AWSAuth


# define service urls and create app
app = webapp2.WSGIApplication([
    ('/', DefaultPage),
    ('/salesforce', SalesForceAuth),
    ('/aws', AWSAuth)
], debug=True)

def main():
    app.run()

if __name__ == "__main__":
    main()