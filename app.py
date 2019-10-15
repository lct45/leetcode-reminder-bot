import yaml
import random
import os
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

# Sent if first time user is using bot
greetings =  {"greeting":[ #Greetings 
        {
        "locale":"default",
        "text":"We're going to make a 10Xer out of you, {{user_first_name}}!"
        }
    ]}
bot.set_greetings(greetings)
gs = { #Get started button
            "get_started":{
            "payload":"start"
            }
    }
bot.set_get_started(gs)


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
                received_text(message)
            elif message.get("postback"):
                received_postback(message)
    return "Message Processed"

def received_text(event):
    sender_id = event["sender"]["id"] # the FB ID of the person sending the message
    recipient_id = event["recipient"]["id"] # page's facebook ID
    text = event["message"]["text"]
    
    bot.send_text_message(sender_id, "I love Daniel.")

def received_postback(event):
    sender_id = event["sender"]["id"] # the FB ID of the person sending the message
    recipient_id = event["recipient"]["id"] # page's facebook ID
    payload = event["postback"]["payload"]
    
    if payload=='start': # message to 
        bot.send_text_message(sender_id, "Hello, we're going to make a 10Xer out of you!")
        image_path_list = [os.getcwd(), "images", "10Xer.png"]
        bot.send_image_url(sender_id,"https://i.imgur.com/D4JtitY.png")

def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error: invalid verification token"

if __name__ == "__main__":
    app.run()