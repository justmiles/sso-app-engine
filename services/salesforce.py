# This implementation of SSO to SalesForce will use the Delegated Auth method. See below PDF for more info.
# https://na1.salesforce.com/help/pdfs/en/salesforce_single_sign_on.pdf
# Additional resources:
#  https://help.salesforce.com/apex/HTViewHelpDoc?id=sso_delauthentication_configuring.htm&language=en
#  view and edit the sandbox in salesforce to test

from google.appengine.api import users
import ConfigParser
import webapp2
from xml.etree import ElementTree
import logging
import utilities

class SalesForceAuth(webapp2.RequestHandler):
	def get(self):
		config = ConfigParser.ConfigParser()
		config.read('settings.cfg')

		user = users.get_current_user()
		if (user):
			logging.info('Logging in ' + user.email())
			# Assign token to user.
			# self.redirect(config.get('salesforce','login_url') + "?un=" + user.email() + "&pw=" + user.token)
		self.redirect(config.get('salesforce','login_url'))

	def post(self):
		config = ConfigParser.ConfigParser()
		config.read('./salesforce/settings.cfg')

		authenticated = False

		# parse posted xml from SalesForce
		xml = ElementTree.fromstring(self.request.body)
		username = xml[0][0][0].text
		password = xml[0][0][1].text
		sourceIp = xml[0][0][2].text
		logging.info('Received credentials for ' + username + ' from ' + sourceIp)

		authenticated = utilities.AdConnect().test_credentials(username,password, sourceIp)

		logging.info(username + ' auth: ' + str(authenticated))

		self.response.headers['Content-Type'] = 'xml/application'
		self.response.write('<?xml version="1.0" encoding="UTF-8"?>')
		self.response.write('<soapenv:Envelope')
		self.response.write(' xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">')
		self.response.write('<soapenv:Body>')
		self.response.write('<AuthenticateResult xmlns="urn:authentication.soap.sforce.com">')
		self.response.write('<Authenticated>' + str(authenticated).lower() + '</Authenticated>')
		self.response.write('</AuthenticateResult>')
		self.response.write('</soapenv:Body>')
		self.response.write('</soapenv:Envelope>')