import psycopg2
import psycopg2.extras

# Servers as wrapper for psycopg2 in the context of this project and provides error handling


class PgInstance:
    def __init__(self, PSQL_LOGIN_CMD, fb_id):
        # Raw command used to login to PSQL database through psycopg2
        self.PSQL_LOGIN_CMD = PSQL_LOGIN_CMD
        self.fb_id = fb_id  # Facebook user ID
        self.conn = None  # Current connection object, None if no connection
        # Current cursor object, None if no cursor/connection
        self.curs = None

    """
    Open connection and initialize cursor for PSQL database

    Returns:
        connection object and database cursor object, or error if connection failed
    """

    def Connect(self):
        try:
            self.conn = psycopg2.connect(self.PSQL_LOGIN_CMD)
            self.curs = self.conn.cursor(
                cursor_factory=psycopg2.extras.NamedTupleCursor
            )
        except Exception as e:
            return e

    """
    Close cursor and connection to PSQL database

    Returns:
        None if successful disconnection, else Exception
    """

    def Disconnect(self):
        try:  # make changes persist
            self.conn.commit()
        except Exception as e:
            return e
        if self.conn == None or self.curs == None:
            return Exception("No connection or cursor to disconnect from.")
        self.curs.close()
        self.curs = None
        self.conn.close()
        self.conn = None
        return None

    """
    Get row by Facebook user ID

    Returns:
        Named Tuple for row containing sender Facebook user ID
    """

    def get_user_row(self):
        self.curs.execute(
            "SELECT * FROM reminders WHERE fb_id=%s", (self.fb_id,))
        return self.curs.fetchone()  # We should never get more than one

    """
    Set LeetCode username for user

    Args:
        text: Raw message sent by user to chatbot

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Set_username(self, text):
        row = self.get_user_row()
        if row == None:  # New user
            self.curs.execute(
                "INSERT INTO reminders (fb_id, leetcode_username) VALUES (%s, %s)",
                (self.fb_id, text)
            )
            return "Username added.", None
        else:  # Overwrite username for existing user
            self.curs.execute(
                "UPDATE reminders SET leetcode_username=%s WHERE fb_id=%s",
                (text, self.fb_id)
            )
            return "Username updated.", None

    """
    Set daily goal for LeetCode question bodycount for FB user

    Args:
        text: Raw message sent by user to chatbot

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Set_daily_goal(self, text):
        row = self.get_user_row()
        if row == None:
            self.curs.execute(
                "INSERT INTO reminders (fb_id, daily_goal) VALUES (%s, %s)",
                (self.fb_id, text)
            )
            return "Daily goal set.", None
        else:
            self.curs.execute(
                "UPDATE reminders SET daily_goal=%s WHERE fb_id=%s", (
                    text, self.fb_id)
            )
            return "Daily goal updated.", None

    """
    Set time for reminder for FB user

    Args:
        text: Raw message sent by user to chatbot

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Set_reminder(self, text):
        row = self.get_user_row()
        if row == None:
            self.curs.execute(
                "INSERT INTO reminders (fb_id, reminder_time) VALUES (%s, %s)",
                (self.fb_id, text)
            )
            return "Reminder set.", None
        else:
            self.curs.execute(
                "UPDATE reminders SET reminder_time=%s WHERE fb_id=%s",
                (text, self.fb_id)
            )
            return "Reminder updated.", None
    
    """
    Set current questions from leetcode account

    Args:
        text: current questions completed according to leetcode
    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Set_completed_questions(self, text):
        row = self.get_user_row()
        if row == None:
            self.curs.execute(
                "INSERT INTO reminders (fb_id, completed_questions) VALUES (%s, %s)",
                (self.fb_id, text),
            )

        else:
            self.curs.execute(
                "UPDATE reminders SET questions_completed=%s WHERE fb_id=%s", (text, self.fb_id)
            )
        response = "You've completed " + text + " questions so far"
        return response, None
    """
    Check daily goal for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Check_daily_goal(self):
        row = self.get_user_row()
        if row == None:
            return "You haven't set a reminder yet!", None
        else:
            self.curs.execute(
                "SELECT daily_goal FROM reminders WHERE fb_id=%s", (
                    self.fb_id,)
            )
            return self.curs.fetchone(), None

    """
    Disable reminder for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
        Exception if error from SQL query, else None
    """

    def Disable_reminder(self):
        row = self.get_user_row()
        if row == None:
            return "You haven't set a reminder yet!", None
        else:
            self.curs.execute(
                "UPDATE reminders SET reminder_time=NULL WHERE fb_id=%s", (
                    self.fb_id,)
            )
            return "Reminder disabled.", None

    def Delete_user(self):
        try:
            self.curs.execute(
                "DELETE FROM reminders WHERE fb_id=%s", (self.fb_id,))
            return None
        except Exception as e:
            return e

    def Get_checklist(self):
        row = self.get_user_row()
        checklist = {}
        checklist_items = ["leetcode_username", "daily_goal", "reminder_time"]
        if row == None:
            for checklist_item in checklist_items:
                checklist[checklist_item] = None
        else:
            for checklist_item in checklist_items:
                checklist[checklist_item] = getattr(row, checklist_item)
        return checklist
