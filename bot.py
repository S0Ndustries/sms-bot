from flask import Flask, request, Response
from verification import verify_signature
import requests
import os

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
        # create a response to each received message just echoing the body text
        if message['type'] == 'text':
            responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'You said "{}"'.format(message['body'])
            })

    if responses:
        # send the responses through the Chat Engine API
        requests.post(
            'https://engine.apikik.com/api/v1/message',
            auth=(os.environ['USERNAME'], os.environ['API_KEY']),
            json={'messages': responses}
        )

    return Response(status=200)
