import re

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

