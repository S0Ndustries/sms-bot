from flask import Flask, request, Response
from verification import verify_signature
import requests
import os
import database
import twilio_api

app = Flask(__name__)

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
                    'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada. What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                })
                #Add user to DB with default values
                database.addUser('false','false', message['from'],0)
        #Other responses    
        elif message['type'] == 'text':
            if database.lookUpUser(message['from']) == False:
                responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada. What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                })
                database.addUser('false','false', message['from'],'0')

            elif message['body'] == 'Send a new message' or message['body'] == 'Send another message':
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Please enter the phone number you\'d like to send the SMS to (must be a US or Canada number)' 
                })
                database.setGivenNum(message['from'],'true')

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == False:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Please enter the message you\'d like to send to ' + database.getPhoneNumber(message['from'])
                })
                database.setGivenMessage(message['from'],'true')
                database.storePhoneNum(message['from'], message['body'])

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == True:
                result = twilio_api.sendsms(database.getPhoneNumber(message['from']), message['body'])

                if result == 'SUCCESS':
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'SMS Sent: \n To: ' + database.getPhoneNumber(message['from']) + '\n Message: ' + message['body'] + '\n What would you like to do next?',
                    'suggestedResponses': ['Send another message']
                    })
                    database.setGivenMessage(message['from'], 'false')
                    database.setGivenNum(message['from'], 'false')
                elif result == 'INVALID NUMBER':
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'We couldn\'t send your message because of an invalid number. Please enter a valid US or Canadian number.'
                    })
                    database.setGivenMessage(message['from'], 'false')

                elif result == 'MESSAGE NOT SENT. PLEASE TRY AGAIN.':
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'I couldn\'t send your message for some reason. What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                    })
                    database.setGivenMessage(message['from'], 'false')
                    database.setGivenNum(message['from'], 'false')


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

@app.route('/receive', methods=['POST'])
if not verify_signature(request):
    return Response(status=403, response='invalid signature')
requests.post(
    'https://engine.apikik.com/api/v1/message',
    auth=(os.environ['USERNAME'], os.environ['API_KEY']),
    headers={
        'Content-Type': 'application/json'
    },
    data='{"messages":[{"to":"laura","type":"text","body":"bar"}]}'
)   









