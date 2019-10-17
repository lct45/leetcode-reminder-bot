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
        connection object and database cursor object
    """
    def Connect(self):
        try:
            self.conn = psycopg2.connect(self.PSQL_LOGIN_CMD)
            self.curs = self.conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
        except Exception as e:
            return e

    """
    Close cursor and connection to PSQL database
    """
    def Disconnect(self,):
        self.curs.close()
        self.curs = None
        self.conn.close()
        self.conn = None

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
    """
    def Set_username(self):
        pass

    """
    Set daily goal for LeetCode question bodycount for user
    """
    def Set_daily_goal(self):
        pass

    """
    Set time for reminder for user
    """
    def Set_reminder(self):
        pass

    """
    Disable reminder for user
    """
    def Disable_reminder(self):
        pass
