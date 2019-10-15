import yaml
import random
from flask import Flask, request

from pymessenger.bot import Bot

"""
The follow variables must be specified in secret.yaml:
CLIENT_ACCESS_TOKEN: Client access token from DialogFlow
PAGE_ACCESS_TOKEN: Facebook page access token
VERIFY_TOKEN: Verification token for Facebook chatbot
"""
with open("secret.yaml") as secretFile:
    secretDict = yaml.load(secretFile,  Loader=yaml.BaseLoader)
    CLIENT_ACCESS_TOKEN =  secretDict["CLIENT_ACCESS_TOKEN"]
    PAGE_ACCESS_TOKEN = secretDict["PAGE_ACCESS_TOKEN"]
    VERIFY_TOKEN = secretDict["VERIFY_TOKEN"]

bot = Bot(PAGE_ACCESS_TOKEN) # PyMessenger Bot
app = Flask(__name__) # Flask app

#We will receive messages that Facebook sends our bot at this endpoint 
@app.route("/", methods=["GET", "POST"])
def receive_message():
    if request.method == "GET": # Facebook requested verification token
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else: # If the request wasn't GET it was a POST request
       output = request.get_json()
       for event in output["entry"]:
          messaging = event["messaging"]
          for message in messaging:
            if message.get("message"):
                #Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message["sender"]["id"]
                if message["message"].get("text"):
                    response_sent_text = get_message()
                    send_message(recipient_id, response_sent_text)

    return "Message Processed"


def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Invalid verification token"

#chooses a random message to send to the user
def get_message():
    sample_responses = ["Yeet"]
    # return selected item to the user
    return random.choice(sample_responses)

#uses PyMessenger to send response to user
def send_message(recipient_id, response):
    #sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"

if __name__ == "__main__":
    app.run()