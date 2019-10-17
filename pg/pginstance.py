import psycopg2
import psycopg2.extras

class PgInstance:

    def __init__(self, PSQL_LOGIN_CMD, fb_id):
        self.PSQL_LOGIN_CMD = PSQL_LOGIN_CMD # Raw command used to login to PSQL database through psycopg2
        self.fb_id = fb_id                   # Facebook user ID
        self.conn = None                     # Current connection object, None if no connection
        self.curs = None                     # Current cursor object, None if no cursor/connection

    """
    Open connection and initialize cursor for PSQL database

    Returns:
        connection object and database cursor object, or error if connection failed
    """
    def Connect(self):
        try:
            self.conn = psycopg2.connect(self.PSQL_LOGIN_CMD)
            self.curs = self.conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
        except Exception as e:
            return e

    """
    Close cursor and connection to PSQL database

    Returns:
        None if successful disconnection, else Exception
    """
    def Disconnect(self,):
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
        self.curs.execute("SELECT * FROM reminders WHERE fb_id=%s", (self.fb_id,))
        return self.curs.fetchone() # We should never get more than one

    """
    Set LeetCode username for user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
    """
    def Set_username(self):
        row = self.get_user_row()
        if row == None:
            pass
        else:
            pass

        return ""

    """
    Set daily goal for LeetCode question bodycount for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
    """
    def Set_daily_goal(self):
        row = self.get_user_row()
        if row == None:
            pass
        else:
            pass

        return ""

    """
    Set time for reminder for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
    """
    def Set_reminder(self):
        row = self.get_user_row()
        if row == None:
            pass
        else:
            pass

        return ""

    """
    Check daily goal for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
    """
    def Check_daily_goal(self):
        row = self.get_user_row()
        if row == None:
            pass
        else:
            pass

        return ""

    """
    Disable reminder for FB user

    Returns:
        str response that bot should relay to user, empty string ("") if nothing should be relayed
    """
    def Disable_reminder(self):
        row = self.get_user_row()
        if row == None:
            return "No reminder has been set!"
        else:
            pass

        return ""
