import random_gen
def points():
	request.post({
	    url: "https://engine.apikik.com/api/v1/message",
	    auth: {
	        user: "smsbot",
	        pass: "6fe6f6dd-7970-4033-ae59-07bbd2f5d1cc"
	    },
	    json: {
	    	"messages":[{
	    		"to":message['from'],
	    		"type":"link",
	    		"url":"https://points.kik.com"
<<<<<<< HEAD
	    		"transaction":{  
				     "id":random_gen.randomgen(),
				     "sku":"KikPointsforSMS"
				     "points":10,
				     "url":"https://sms-chat-bot.herokuapp.com",
				     "callback_url":"https://sms-chat-bot.herokuapp.com/kikpoints",
				     #"data":{  
				     #   //Any other arbitrary data you may need
				     #}
				   },
=======
	    		"data":{
	    			"transaction":{  
				      "id":random_gen.randomgen(),
				      "sku":"KikPointsforSMS"
				      "points":10,
				      #"url":"points.kik.com",
				      #"callback_url":"https://sms-chat-bot.herokuapp.com/kikpoints",
				      #"data":{  
				       #   //Any other arbitrary data you may need
				      #}
				   }	
	    		},
>>>>>>> origin/master
	    		"noForward":true
	    		}]
	    }
	}, callback);
	return
<<<<<<< HEAD
=======

# Things to Do:
# Ask Sanchit/Mike about the callback urls and the url
>>>>>>> origin/master
