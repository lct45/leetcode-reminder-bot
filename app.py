import yaml
import random
from flask import Flask, request
from pymessenger.bot import Bot
from pg.pginstance import PgInstance

# Load variables from secret.yaml
with open("secret.yaml") as secretFile:
    secretDict = yaml.load(secretFile,  Loader=yaml.BaseLoader)
    PAGE_ACCESS_TOKEN = secretDict["PAGE_ACCESS_TOKEN"] # Facebook page access token
    VERIFY_TOKEN = secretDict["VERIFY_TOKEN"] # Verification token for Facebook chatbot
    PSQL_LOGIN_CMD = secretDict["PSQL_LOGIN_CMD"] # PSQL command to execute to login to database

bot = Bot(PAGE_ACCESS_TOKEN) # Initialize PyMessenger Bot
app = Flask(__name__) # Initialize Flask app

# Sent if first time user is using bot, check is handled by FB API rather than our end
greeting =  {"greeting":[ # Greeting text
        {
        "locale":"default",
        "text":"We're going to make a 10Xer out of you, {{user_first_name}}!"
        }
    ]}
bot.set_greeting(greeting)
gs = { # Get started button
            "get_started":{
            "payload":"start"
            }
    }
bot.set_get_started(gs)

# Response options that persist during entire chat
persistent_menu = {
            "persistent_menu": [
                {
                    "locale": "default",
                    "composer_input_disabled": False,
                    "call_to_actions": [
                        {
                            "type": "postback",
                            "title": "Set LeetCode username",
                            "payload": "pm_set_username"
                        },
                        {
                            "type": "postback",
                            "title": "Set reminder",
                            "payload": "pm_set_reminder"
                        },
                        {
                            "type": "postback",
                            "title": "Set daily goal",
                            "payload": "pm_set_daily_goal"
                        },
                        {
                            "type": "postback",
                            "title": "Check daily goal",
                            "payload": "pm_check_daily_goal"
                        },
                        {
                            "type": "postback",
                            "title": "Disable reminder",
                            "payload": "pm_disable_reminder"
                        }
                    ]
                }
            ]
        }
bot.set_persistent_menu(persistent_menu)

"""
Handles GET and POST requests to Flask endpoint.

Requests:
    GET: Facebook API is asking for verification, verify Facebook verification token against VERIFY_TOKEN variable
    POST: User sent a message, handle either text or postback response
"""
@app.route("/", methods=["GET", "POST"])
def endpoint():
    if request.method == "GET": # Facebook requested verification token
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else: # If the request wasn't GET it was a POST request
       output = request.get_json()
       for event in output["entry"]:
          messaging = event["messaging"]
          for message in messaging:
            if message.get("message"): # Got text
                received_text(message)
            elif message.get("postback"): # Got message
                received_postback(message)
            else: # Change this behavior in the future, as it's the same as receiving text msg
                received_text(message)
    return "Message Processed"

"""
Responds to user to communicate with one of the postback options.

Args:
    event: Nested dictionary that contains Facebook user ID, chatbot page's ID, and message that was sent
"""
def received_text(event):
    sender_id = event["sender"]["id"] # the FB ID of the person sending the message
    recipient_id = event["recipient"]["id"] # page's facebook ID
    text = event["message"]["text"]
    
    bot.send_text_message(sender_id, "Please use one of the options to communicate with me!")

"""
Responds to user either the welcome message or responds to postback response from the persistent menu.
Through the persistent menu, users are able to do the following with postback responses, which are logged in the PSQL db:
    1. Set LeetCode username
    2. Set daily goal for questions to complete
    3. Set time to remind
    4. Disable reminder

Args:
    event: Nested dictionary that contains Facebook user ID, chatbot page's ID, and message that was sent

Documentation:
    Postbacks: https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messaging_postbacks
"""
def received_postback(event):
    sender_id = event["sender"]["id"] # the FB ID of the person sending the message
    recipient_id = event["recipient"]["id"] # page's facebook ID
    payload = event["postback"]["payload"]
    
    if payload == "start": # Initial welcome message for first-time users
        bot.send_text_message(sender_id, "Hello, we're going to make a 10Xer out of you!")
        bot.send_image_url(sender_id,"https://i.imgur.com/D4JtitY.png")
        bot.send_text_message(sender_id, "To get started, set your LeetCode username, daily goal for questions you plan on completing, and the time of day to remind you!")
    else: # Persistent menu
        # Connect to db
        db = PgInstance(PSQL_LOGIN_CMD, sender_id)
        err = db.Connect()
        if err == None: # Successful connection
            db_response = None
            if payload == "pm_set_username":
                db_response = db.Set_username()
            elif payload == "pm_set_reminder":
                db_response = db.Set_reminder()
            elif payload == "pm_set_daily_goal":
                db_response = db.Set_daily_goal()
            elif payload == "pm_check_daily_goal":
                db_response = db.Check_daily_goal()
            elif payload == "pm_disable_reminder":
                db_response = db.Disable_reminder()
            else:
                print("Invalid payload: " + payload)
            err = db.Disconnect()
            if err != None:
                raise err
            # Send db query response to user
            if db_response != "":
                bot.send_text_message(sender_id, db_response)
        else: # Unsuccessful connection
            bot.send_text_message(sender_id, "Uh-oh, my database is currently down! Take a break and go outside for a change!")
            print(err)


"""
Compare verification token set in the Facebook API against VERIFY_TOKEN variable from secret.yaml

Args:
    VERIFY_TOKEN: Local copy of verification token

Returns:
    string response whether VERIFY_TOKEN == FB verification token
"""
def verify_fb_token(token_sent):
    #take token sent by facebook and verify it matches the verify token you sent
    #if they match, allow the request, else return an error 
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error: invalid verification token"

if __name__ == "__main__":
    app.run()