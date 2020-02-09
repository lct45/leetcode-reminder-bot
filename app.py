import traceback
import yaml
import random
from flask import Flask, request
from pymessenger.bot import Bot
from pg.pginstance import PgInstance
from util import validation
from util import dialog

# Load variables from secret.yaml
with open("secret.yaml") as secretFile:
    secretDict = yaml.load(secretFile, Loader=yaml.BaseLoader)
    # Facebook page access token
    PAGE_ACCESS_TOKEN = secretDict["PAGE_ACCESS_TOKEN"]
    # Verification token for Facebook chatbot
    VERIFY_TOKEN = secretDict["VERIFY_TOKEN"]
    # PSQL command to execute to login to database
    PSQL_LOGIN_CMD = secretDict["PSQL_LOGIN_CMD"]

bot = Bot(PAGE_ACCESS_TOKEN)  # Initialize PyMessenger Bot
app = Flask(__name__)  # Initialize Flask app

# Sent if first time user is using bot, check is handled by FB API rather than our end
greeting = {
    "greeting": [  # Greeting text
        {
            "locale": "default",
            "text": "Are you ready to get that bread, {{user_first_name}}?",
        }
    ]
}
bot.set_get_started(greeting)
gs = {"get_started": {"payload": "start"}}  # Get started button
bot.set_get_started(gs)

bot.remove_persistent_menu()

quick_replies_list = [
    {
        "content_type": "text",
        "title": "Set LeetCode username",
        "payload": "qr_set_username",
    },
    {
        "content_type": "text",
        "title": "Set daily goal",
        "payload": "qr_set_daily_goal",
    },
    {
        "content_type": "text",
        "title": "Set reminder",
        "payload": "qr_set_reminder",
    },
    {
        "content_type": "text",
        "title": "Check daily goal",
        "payload": "qr_check_daily_goal",
    },
    {
        "content_type": "text",
        "title": "Disable reminder",
        "payload": "qr_disable_reminder",
    },
]

PREVIOUS_PAYLOAD_DICT = {}

"""
Handles GET and POST requests to Flask endpoint.

Requests:
    GET: Facebook API is asking for verification, verify Facebook verification token against VERIFY_TOKEN variable
    POST: User sent a message, handle either text or postback response
"""


@app.route("/", methods=["GET", "POST"])
def endpoint():
    if request.method == "GET":  # Facebook requested verification token
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    else:  # If the request wasn't GET it was a POST request
        output = request.get_json()
        for event in output["entry"]:
            messaging = event["messaging"]
            for message in messaging:
                try:
                    if message.get("message"):  # Got text
                        received_text(message)
                    elif message.get("postback"):  # Got message
                        received_postback(message)
                except Exception as e:
                    print(traceback.format_exc())
                    bot.send_text_quick_replies(
                        message["sender"]["id"], "Something went horribly wrong!", quick_replies_list)
                    print("Something went horribly wrong: " + str(e))
    return "Message Processed"


"""
If followUp is none, responds to user to communicate with one of the postback options, else perform PREVIOUS_PAYLOAD_DICT[sender_id] action from the following:
    1. Set LeetCode username
    2. Set daily goal for questions to complete
    3. Set time to remind
    4. Disable reminder

Args:
    event: Nested dictionary that contains Facebook user ID, chatbot page's ID, and message that was sent
"""


def received_text(event):
    # the FB ID of the person sending the message
    sender_id = event["sender"]["id"]
    bot.send_action(sender_id, "mark_seen")
    # Attempt to get text
    try:
        text = event["message"]["text"]
    except:
        bot.send_text_quick_replies(
            sender_id, "I didn't quite understand.", quick_replies_list)
        return
    # Attempt to get payload
    payload = None
    try:
        payload = event["message"]["quick_reply"]["payload"]
    except:
        pass
    # If payload exists and is a quick reply
    if payload != None and payload.split("_")[0] == "qr":
        if payload.split("_")[1] == "set":  # set commands require a text follow-up
            PREVIOUS_PAYLOAD_DICT[sender_id] = payload
            selected_info = payload.split("_")[2]
            inquiry_msg = dialog.get_inquiry_msg(selected_info)
            bot.send_text_quick_replies(
                sender_id, inquiry_msg, quick_replies_list)
        else:
            # Connect to db
            db = PgInstance(PSQL_LOGIN_CMD, sender_id)
            err = db.Connect()
            if err != None:
                print(err)
                bot.send_text_quick_replies(
                    sender_id, "Error connecting to db", quick_replies_list)  # replace this eventually
                return
            db_response, user_err_msg, err = dialog.handle_quick_replies(
                payload, text, db, bot.get_user_info(sender_id, ["timezone"]))
            # Check for err from SQL query
            if err != None:
                print(err)
                bot.send_text_quick_replies(
                    sender_id, "Error with sql query", quick_replies_list)  # replace this eventually
                return
            # Disconnect from db
            err = db.Disconnect()
            if err != None:
                print(err)
                bot.send_text_quick_replies(
                    sender_id, "Error disconnecting from db", quick_replies_list)  # replace this eventually
                return
            # Send db query response to user
            if db_response != "":
                bot.send_text_quick_replies(
                    sender_id, db_response, quick_replies_list)
    elif sender_id in PREVIOUS_PAYLOAD_DICT:
        previous_payload = PREVIOUS_PAYLOAD_DICT[sender_id]
        del PREVIOUS_PAYLOAD_DICT[sender_id]
        # Connect to db
        db = PgInstance(PSQL_LOGIN_CMD, sender_id)
        err = db.Connect()
        if err != None:  # Successful connection
            print(err)
            bot.send_text_quick_replies(
                sender_id, "Error connecting to db", quick_replies_list)  # replace this eventually
            return
        db_response, user_err_msg, err = dialog.handle_quick_replies(
            previous_payload, text, db, bot.get_user_info(sender_id, ["timezone"]))
        # Check for user_err_msg
        if user_err_msg != None:
            bot.send_text_quick_replies(
                sender_id, user_err_msg, quick_replies_list)
        # Check for err from SQL query
        if err != None:
            print(err)
            bot.send_text_quick_replies(
                sender_id, "Error with sql query", quick_replies_list)  # replace this eventually
            return
        # Send db query response to user
        if db_response != "":
            bot.send_text_quick_replies(
                sender_id, db_response, quick_replies_list)
        # Send checklist message
        checklist_msg = dialog.get_checklist(db)
        bot.send_text_quick_replies(
            sender_id, "Checklist status:\n" + checklist_msg, quick_replies_list)
        # Disconnect from db
        err = db.Disconnect()
        if err != None:
            print(err)
            bot.send_text_quick_replies(
                sender_id, "Error disconnecting from db", quick_replies_list)  # replace this eventually
            return
    else:
        bot.send_text_quick_replies(
            sender_id, "Please use one of the options below to communicate with me!", quick_replies_list)


"""
Responds to user either the welcome message or responds to postback response from the persistent menu and sets PREVIOUS_PAYLOAD_DICT[sender_id] to alter received_text() behavior

Args:
    event: Nested dictionary that contains Facebook user ID, chatbot page's ID, and message that was sent

Documentation:
    Postbacks: https://developers.facebook.com/docs/messenger-platform/reference/webhook-events/messaging_postbacks
"""


def received_postback(event):
    # the FB ID of the person sending the message
    sender_id = event["sender"]["id"]
    # recipient_id = event["recipient"]["id"]  # page's facebook ID
    payload = event["postback"]["payload"]
    bot.send_action(sender_id, "mark_seen")
    if payload == "start":  # Initial welcome message for first-time users
        bot.send_text_message(
            sender_id, "Hello, we're going to make a 10Xer out of you!"
        )
        bot.send_image_url(sender_id, "https://i.imgur.com/D4JtitY.png")
        db = PgInstance(PSQL_LOGIN_CMD, sender_id)
        err = db.Connect()
        if err == None:
            err = db.Delete_user()
            checklist_msg = dialog.get_checklist(db)
            bot.send_text_quick_replies(
                sender_id,
                "To get started, we're going to need the following information:\n" + checklist_msg, quick_replies_list)
            db.Disconnect()
        else:
            print(err)
            bot.send_text_quick_replies(
                sender_id, "Error connecting to db", quick_replies_list)  # replace this eventually
            return
    else:  # should never happen, should add logging for these cases
        bot.send_text_quick_replies(
            sender_id, "Invalid payload", quick_replies_list)
        print("Invalid payload: " + payload)


"""
Compare verification token set in the Facebook API against VERIFY_TOKEN variable from secret.yaml

Args:
    VERIFY_TOKEN: Local copy of verification token

Returns:
    string response whether VERIFY_TOKEN == FB verification token
"""


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Error: invalid verification token"


if __name__ == "__main__":
    app.run()
