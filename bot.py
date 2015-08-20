from flask import Flask, request, Response
from verification import verify_signature
import requests
import os
import database
import twilio_api
import random_gen
import logging 

app = Flask(__name__)
app.config['DEBUG'] = True


#Function to trigger Kik Points transaction
def chargePoints(username):
    userID = random_gen.randomgen()
    app.logger.debug(userID)
    requests.post(
    'https://engine.apikik.com/api/v1/message',
    auth=('smsbot', '6fe6f6dd-7970-4033-ae59-07bbd2f5d1cc'),
    headers={
        'Content-Type': 'application/json'
    },
    data= '{"messages":[{"to":"%s","type":"link","url" :"https://points.kik.com/", "text" : "Click me to use your Kik Points",  "noForward" : true , "attribution": {"name": "Kik Points", "iconUrl": "http://offer-service.appspot.com/static/kp-icon.50.jpg"} , "kikJsData" : {"transaction" : {"id" : "%s", "points" : 10, "sku" : "com.kp.forSms", "url" : "https://e008dd1d.ngrok.io/kikpoints", "callback_url" : "https://e008dd1d.ngrok.io/kikpoints"} }}]}' % (username, userID)
    )  
    database.setID(username,userID)
    return



@app.route('/receive', methods=['POST'])
def receive_messages():
    """Handle inbound messages and send responses through the Chat Engine API"""

    # ensure that the signature on the request is valid
    if not verify_signature(request):
        return Response(status=403, response='invalid signature')

    messages = request.json['messages']
    responses = []

    for message in messages:
        if message['type'] == 'scan-data':
            if database.lookUpUser(message['from']) == False:
                responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada for only 10 Kik Points! What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                })
                database.addUser('false','false', message['from'],'0','0')
        #Other responses    
        elif message['type'] == 'text':
            if database.lookUpUser(message['from']) == False:
                responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada for only 10 Kik Points! What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                })
                database.addUser('false','false', message['from'],'0','0')

            elif message['body'] == 'Send a new message' or message['body'] == 'Send another message': #TODO:Regex this
                chargePoints(message['from'])

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == False:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Please enter the message you\'d like to send to ' + message['body']
                })
                database.setGivenMessage(message['from'],'true')
                database.storePhoneNum(message['from'], message['body'])

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == True:
                print ''
               #result = twilio_api.sendsms(database.getPhoneNumber(message['from']), message['body'])

                #if result == 'SUCCESS':
                 #   responses.append({
                  #  'type': 'text',
                   # 'to': message['from'],
                   # 'body': 'SMS Sent: \n To: ' + database.getPhoneNumber(message['from']) + '\n Message: ' + message['body'] + '\n What would you like to do next?',
                   # 'suggestedResponses': ['Send another message']
                   # })
                   # database.setGivenMessage(message['from'], 'false')
                   # database.setGivenNum(message['from'], 'false')
                #elif result == 'INVALID NUMBER':
                 #   responses.append({
                 #   'type': 'text',
                  #  'to': message['from'],
                   # 'body': 'We couldn\'t send your message because of an invalid number. Please enter a valid US or Canadian number.'
                   # })
                   # database.setGivenMessage(message['from'], 'false')

                #elif result == 'MESSAGE NOT SENT. PLEASE TRY AGAIN.':
                 #   responses.append({
                  #  'type': 'text',
                   # 'to': message['from'],
                   # 'body': 'I couldn\'t send your message for some reason. What would you like to do?',
                   # 'suggestedResponses': ['Send a new message']
                   # })
                   # database.setGivenMessage(message['from'], 'false')
                   # database.setGivenNum(message['from'], 'false')


            else:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'I\'m not sure what you\'re trying to tell me. Please provide a valid command.' 
                })
        elif message['type'] == 'picture':
            responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Cool picture but there\'s not much I can do with it...yet...' 
                })

            #Insert easter egg?

    if responses:
        # send the responses through the Chat Engine API
        requests.post(
            'https://engine.apikik.com/api/v1/message',
            auth=(os.environ['USERNAME'], os.environ['API_KEY']),
            json={'messages': responses}
        )

    return Response(status=200)

@app.route('/kikpoints', methods=['POST'])
def callback_message():
    username = database.getUsernameFromID(request.json['id'])
    requests.post(
    'https://engine.apikik.com/api/v1/message',
    auth=('smsbot', '6fe6f6dd-7970-4033-ae59-07bbd2f5d1cc'),
    headers={
        'Content-Type': 'application/json'
    },
    data= '{"messages":[{"to":"%s","type":"text", "body":"Transaction successful. Which phone number shall I send a message to? Tip: Don\'t forget to prepend +1 to the number!" }]}' % username
    )   
    database.setGivenNum(username,'true')
    return Response(status=200)











