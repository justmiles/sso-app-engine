# http://docs.aws.amazon.com/STS/latest/UsingSTS/STSMgmtConsole-manualURL.html

import cgi, urllib, json
import requests
from google.appengine.api import users
from google.appengine.api import app_identity
from google.appengine.api import oauth
import webapp2
import boto
from boto import sts

class AWSAuth(webapp2.RequestHandler):
    def get(self):
		user = oauth.get_current_user()
		token = app_identity.sign_blob('0010')
		self.response.out.write('<html><body>%s</body></html>' % oauth.get_oauth_consumer_key())

		# TODO: get keys from config file
		sts = boto.sts.connect_to_region('us-west-2',
			aws_access_key_id='AKIAJ2YKJZJ6SAVM32RA',
			aws_secret_access_key='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',
			validate_certs=False)
		assumed_role_object = sts.get_federation_token(user.nickname(),duration=900)

		# assumed_role_object = sts.assume_role(
			# role_arn="arn:aws:iam::314819186751:role/federated_auth",
			# role_session_name="edo"
		# )

		# Format resulting temporary credentials into JSON
		json_string_with_temp_credentials = '{'
		json_string_with_temp_credentials += '"sessionId":"' + assumed_role_object.credentials.access_key + '",'
		json_string_with_temp_credentials += '"sessionKey":"' + assumed_role_object.credentials.secret_key + '",'
		json_string_with_temp_credentials += '"sessionToken":"' + assumed_role_object.credentials.session_token + '"'
		json_string_with_temp_credentials += '}'

		# Make request to AWS federation endpoint to get sign-in token. Pass the action and JSON
		# document with temporary credentials as parameters.
		request_parameters = "?Action=getSigninToken"
		request_parameters += "&Session=" + urllib.quote_plus(json_string_with_temp_credentials)
		request_url = "https://signin.aws.amazon.com/federation" + request_parameters
		
		r = urllib.urlopen(request_url)
		
		# Returns a JSON document with a single element named SigninToken.
		signin_token = json.loads(r.read())

		# Create URL that will let users sign in to the console using the
		# sign-in token. This URL must be used within 15 minutes of when the
		# sign-in token was issued.
		request_parameters = "?Action=login" 
		request_parameters += "&Issuer=Example.org" 
		request_parameters += "&Destination=" + urllib.quote_plus("https://console.aws.amazon.com/")
		request_parameters += "&SigninToken=" + signin_token["SigninToken"]
		request_url = "https://signin.aws.amazon.com/federation" + request_parameters

		# TODO: parse settings.cfg for redirect url (alias)
		# Send final URL to stdout
		self.response.out.write('<html><body>%s</body></html>' % assumed_role_object)
		# self.redirect( str(request_url) )