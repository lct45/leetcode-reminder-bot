from pg.pginstance import PgInstance
from util import validation


def get_inquiry_msg(quick_reply):
    inquiry_msg = None
    if quick_reply == "username":
        inquiry_msg = "Sounds good! What is your Leetcode username?"
    elif quick_reply == "reminder":
        inquiry_msg = "Sweet! When would you like to be reminded daily? e.g. 4:20 PM"
    elif quick_reply == "daily":  # daily_goal
        inquiry_msg = "Awesome! What number of questions do you plan on doing daily? Give me a number between 0 and 100!"
    return inquiry_msg


def get_checklist(db):
    checklist = db.Get_checklist()
    leetcode_username_emoji = "❎"
    daily_goal_emoji = "❎"
    reminder_time_emoji = "❎"
    if checklist["leetcode_username"] != None:
        leetcode_username_emoji = "✅"
    if checklist["daily_goal"] != None:
        daily_goal_emoji = "✅"
    if checklist["reminder_time"] != None:
        reminder_time_emoji = "✅"
    checklist_msg = (
        "1.  Your LeetCode username "
        + leetcode_username_emoji
        + "\n2. A daily goal for the number of questions completed "
        + daily_goal_emoji
        + "\n3. The time of day to remind you "
        + reminder_time_emoji
    )
    return checklist_msg


def handle_quick_replies(payload, text, db, timezone):
    db_response = None
    user_err_msg = None
    err = None
    if payload == "qr_check_daily_goal":
        db_response, err = db.Check_daily_goal()
    elif payload == "qr_disable_reminder":
        db_response, err = db.Disable_reminder()
    elif payload == "qr_set_username":
        user_err_msg, valid, err = validation.validate_username(text)
        if valid:
            db_response, err = db.Set_username(text)
    elif payload == "qr_set_reminder":
        user_err_msg, valid, err, reminder_time = validation.validate_reminder(
            text, timezone)
        if valid:
            db_response, err = db.Set_reminder(
                reminder_time)
    elif payload == "qr_set_daily_goal":
        user_err_msg, valid, err = validation.validate_daily_goal(text)
        if valid:
            db_response, err = db.Set_daily_goal(text)
    return db_response, user_err_msg, err
