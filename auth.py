import webapp2
import views
import services
import os

debug = os.environ.get('SERVER_SOFTWARE', '').startswith('Dev')

web_settings = {'debug': debug }


# define service urls and create app
app = webapp2.WSGIApplication([
	('/', views.DefaultPage),
	('/salesforce', services.SalesForceAuth),
	('/salesforce/adconnect', services.SalesForceAuth),
	('/aws', services.AWSAuth)
], debug=debug, config=web_settings)

def main():
	app.run()

if __name__ == "__main__":
	main()