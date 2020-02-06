import re
import datetime
import parsedatetime

"""
Validates username submitted by user

Args:
    username: str sent by user to chatbot

Returns:
    str response that bot should relay to user, empty string ("") if nothing should be relayed
    boolean whether username was valid
    Exception if error from SQL query, else None
"""


def validate_username(username):
    try:
        if re.match(
            "^[A-Za-z0-9\-\_\S]+$",
            username,  # Note for testing, the FB API trims any leading or trailing spaces but not spaces inbetween
        ):  # Leetcode usernames only allow letters, numbers, hyphens and underscores.
            return "", True, None
        else:
            # TO-DO: validate username on leetcode.com
            return "That's not a valid Leetcode username!", False, None
    except Exception as e:
        return "That's not a valid Leetcode username!", False, e


def validate_reminder(reminder_time, timezone):
    try:
        cal = parsedatetime.Calendar()
        reminder_time_parsed = cal.parse(reminder_time)[0]
        # timezone is time relative to GMT
        conversion = -1 * timezone["timezone"]
        r_h = reminder_time_parsed.tm_hour + conversion
        if r_h > 23:
            r_h -= 24
        elif r_h < 0:
            r_h += 24
        r_m = reminder_time_parsed.tm_min
        return datetime.time(r_h, r_m), True, None
    except Exception as e:
        return "That's not a valid time of day! Try something like: 4:20 pm", False, e


def validate_daily_goal(daily_goal):
    if daily_goal.isdigit():
        daily_goal_int = int(daily_goal)
        if daily_goal_int > 0 and daily_goal_int < 100:
            return "", True, None
    return "Please specify a valid daily goal between 1 and 100!", False, None
