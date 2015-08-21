from flask import Flask, request, Response
from verification import verify_signature
import requests
import os
import database
import twilio_api
import random_gen
<<<<<<< Updated upstream
import logging 
import re
=======
>>>>>>> Stashed changes

app = Flask(__name__)
app.config['DEBUG'] = True


#Function to trigger Kik Points transaction
def chargePoints(username):
    userID = random_gen.randomgen()
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




#Function to trigger Kik Points transaction
def points():
    request.post({
        url: "https://engine.apikik.com/api/v1/message",
        auth: {
            "user": "smsbot",
            "pass": "6fe6f6dd-7970-4033-ae59-07bbd2f5d1cc"
        },
        json: {
            "messages":[{
                "to":message['from'],
                "type":"link",
                "url":"https://points.kik.com"
                "transaction":{
                     "id":random_gen.randomgen(),
                     "sku":"KikPointsforSMS"
                     "points":10,
                     "url":"https://e008dd1d.ngrok.io",
                     "callback_url":"https://e008dd1d.ngrok.io/kikpoints",
                     #"data":{
                     #   //Any other arbitrary data you may need
                     #}
                   },
                "noForward":true
                }]
        }
    }, callback);
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
<<<<<<< Updated upstream
                database.addUser('false','false', message['from'],'0','0','false')
        #Other responses    
=======
                #Add user to DB with default values
                database.addUser('false','false', message['from'],0)
        #Other responses
>>>>>>> Stashed changes
        elif message['type'] == 'text':
            if database.lookUpUser(message['from']) == False:
                responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'Welcome to SMS Bot. I can help you send an SMS message to any number in the United States or Canada for only 10 Kik Points! What would you like to do?',
                    'suggestedResponses': ['Send a new message']
                })
                database.addUser('false','false', message['from'],'0','0','false')

<<<<<<< Updated upstream
            elif ((message['body'] == 'Send a new message' or message['body'] == 'Send another message') and database.hasPaid(message['from']) == False): #TODO:Regex this
                chargePoints(message['from'])


            elif message['body'] == 'Change my message' and database.hasPaid(message['from']) == True:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Enter the phone number you\'d like to send a message to.'
                })
                database.setGivenNum(message['from'],'true')

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == False:
                phone_number_check = re.search('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$',message['body']) #Use Regex to check for proper phone-number format

                if (phone_number_check):
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'Please enter the message you\'d like to send to ' + message['body']
                    })
                    database.setGivenMessage(message['from'],'true')
                    database.storePhoneNum(message['from'], message['body'])
                else:
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': message['body'] + ' is not a valid US or Canada number. Please enter a valid number! Tip: Do NOT add +1 to the number!'
                    })

            elif ((database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == True) or (message['body'] == 'Retry' and database.hasPaid(message['from']) == True)):
                if twilio_api.sendsms(database.getPhoneNumber(message['from']), message['body']):
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'SMS Sent: \n To: ' + database.getPhoneNumber(message['from']) + '\n Message: ' + message['body'] + '\n What would you like to do next?',
                    'suggestedResponses': ['Send another message']
                    })
                    database.setGivenMessage(message['from'], 'false')
                    database.setGivenNum(message['from'], 'false')
                    database.setHasPaid(message['from'],'false')
                else:
                    responses.append({
                    'type': 'text',
                    'to': message['from'],
                    'body': 'I could not send your message for some reason. What would you like to do?',
                    'suggestedResponses': ['Change my message','Retry']
                    })
                    database.setGivenMessage(message['from'], 'false')
                    database.setGivenNum(message['from'], 'false')
=======
            elif message['body'] == 'Send a new message' or message['body'] == 'Send another message':
                points()
                #responses.append({
                #'type': 'text',
                #'to': message['from'],
                #'body': 'Please enter the phone number you\'d like to send the SMS to (must be a US or Canada number)'
                #})
                #database.setGivenNum(message['from'],'true')

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == False:
                responses.append({
                'type': 'text',
                'to': message['from'],
                'body': 'Please enter the message you\'d like to send to ' + message['body']
                })
                database.setGivenMessage(message['from'],'true')
                database.storePhoneNum(message['from'], message['body'])

            elif database.hasGivenNum(message['from']) == True and database.hasGivenMessage(message['from']) == True:
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

>>>>>>> Stashed changes

            else:
                responses.append({
                'type': 'text',
                'to': message['from'],
<<<<<<< Updated upstream
                'body': 'I\'m not sure what you\'re trying to tell me. Please provide a valid command such as \'Send a new message\'.' 
=======
                'body': 'I\'m not sure what you\'re trying to tell me. Please provide a valid command.'
>>>>>>> Stashed changes
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
<<<<<<< Updated upstream
def callback_message():
    username = database.getUsernameFromID(request.json['id'])
    requests.post(
    'https://engine.apikik.com/api/v1/message',
    auth=('smsbot', '6fe6f6dd-7970-4033-ae59-07bbd2f5d1cc'),
    headers={
        'Content-Type': 'application/json'
    },
    data= '{"messages":[{"to":"%s","type":"text", "body":"Transaction successful. Enter the phone number you\'d like to send a message to." }]}' % username
    )   
    database.setGivenNum(username,'true')
    database.setHasPaid(username,'true')
    return Response(status=200)

=======
if not verify_signature(request):
    return Response(status=403, response='invalid signature')
requests.post(
    'https://engine.apikik.com/api/v1/message',
    auth=(os.environ['USERNAME'], os.environ['API_KEY']),
    headers={
        'Content-Type': 'application/json'
    },
    data='{"messages":[{"to":\'' + message['from'] + '\',"type":"text","body":"Please enter the phone number you\'d like to send the SMS to (must be a US or Canada number)"}]}'
)
database.setGivenNum(message['from'],'true')
>>>>>>> Stashed changes










