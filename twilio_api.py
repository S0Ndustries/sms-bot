import re
from twilio.rest import TwilioRestClient
 # Your Account Sid and Auth Token from twilio.com/user/account
def sendsms(phonenumber, usermessage):
	account_sid = "AC164a87fb536f9ead23575f129196c639"
	auth_token  = "45f2016a23a6629ecc9df46ad2f3212a"
	client = TwilioRestClient(account_sid, auth_token)
	error_string = ''
	try:
		message = client.messages.create(body=usermessage,
		    to=phonenumber,  
		    from_="+12264003340")
	except Exception as error:
		error_string = str(error)
		error_string = re.search('https\:\/\/www\.twilio\.com\/docs\/errors\/[0-9]*',error_string).group()[35:]
	if error_string == '21211':
		return False
	else:
		return True