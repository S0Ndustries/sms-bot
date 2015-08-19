from flask import Flask, request, Response
from verification import verify_signature
import requests
import os
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = postgres://lcgigjguzxyusa:Fl-W3fEmvP5mmgRSgoYiEF63Ro@ec2-54-197-230-210.compute-1.amazonaws.com:5432/dekjsm7qjhos9c
db = SQLAlchemy(app)


@app.route('/receive', methods=['POST'])
def receive_messages():
    """Handle inbound messages and send responses through the Chat Engine API"""

    # ensure that the signature on the request is valid
    if not verify_signature(request):
        return Response(status=403, response='invalid signature')

    messages = request.json['messages']
    responses = []

    for message in messages:
        #Greeting message on initial scan
        if message['type'] == 'scan-data':
            responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada. What would you like to do?',
                'suggestedResponses': ['Send a New Message', 'Help']
            })
        #Other responses    
        elif message['type'] == 'text':
            if message['body'] == 'Send a New Message':
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Please enter a US or Canadian cellphone number' 
            })

           
    if responses:
        # send the responses through the Chat Engine API
        requests.post(
            'https://engine.apikik.com/api/v1/message',
            auth=(os.environ['USERNAME'], os.environ['API_KEY']),
            json={'messages': responses}
        )

    return Response(status=200)
