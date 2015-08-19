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
                    'suggestedResponses': ['Send a New Message']
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
                    'suggestedResponses': ['Send a New Message']
                })
                #Add user to DB with default values
                database.addUser('false','false', message['from'],0)

            if message['body'] == 'Send a New Message':
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
                'body': 'Please enter the message you\'d like to send to the number provided.' 
                })
                database.setGivenMessage(message['from'],'true')
                database.storePhoneNum(message['from'], message['body'])

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == True:
                #Insert logic to send the text messsage
                twilio_api.sendsms(database.getPhoneNumber(message['from']), message['body'])
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Message sent.' 
                })

            else:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'I\'m not sure what you\'re trying to tell me. Please provide a valid command' 
                })


    if responses:
        # send the responses through the Chat Engine API
        requests.post(
            'https://engine.apikik.com/api/v1/message',
            auth=(os.environ['USERNAME'], os.environ['API_KEY']),
            json={'messages': responses}
        )

    return Response(status=200)











