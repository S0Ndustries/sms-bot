from twilio.rest import TwilioRestClient
 # Your Account Sid and Auth Token from twilio.com/user/account
def sendsms(phonenumber, usermessage):
	account_sid = "AC164a87fb536f9ead23575f129196c639"
	auth_token  = "45f2016a23a6629ecc9df46ad2f3212a"
	client = TwilioRestClient(account_sid, auth_token)
	 
	message = client.messages.create(body=usermessage,
	    to=phonenumber,    # Replace with your phone number
	    from_="+12264003340") # Replace with your Twilio number
	#print message.sid
	return

