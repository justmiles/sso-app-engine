import json
import ConfigParser
import urllib
from google.appengine.api import urlfetch
import logging

class AdConnect():
    def test_credentials(self,username,password, ip):
		config = ConfigParser.ConfigParser()
		config.read('settings.cfg')

		values = {'username' : username,
		          'password' : password,
		          'ip' : ip}

		data = urllib.urlencode(values)
		response = urlfetch.fetch(
			url = config.get('adconnect','adendpoint'),
			payload = data,
			method = urlfetch.POST
			)

		response = json.loads( response.content ) 
		return response["authenticated"];