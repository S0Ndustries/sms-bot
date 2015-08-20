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
	    		"data":{
	    			"transaction":{  
				      "id":"INSERT RANDOMIZED STRING",
				      "sku":"KikPointsforSMS"
				      "points":10,
				      "url":"ygoel",
				      "callback_url":"URL_FOR_CONFIRMATION",
				      #"data":{  
				       #   //Any other arbitrary data you may need
				      #}
				   }	
	    		}
	    		}]
	    }
	}, callback);
	return
