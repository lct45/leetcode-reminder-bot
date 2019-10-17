import psycopg2
import psycopg2.extras

class PgInstance:

    def __init__(self, PSQL_LOGIN_CMD, fb_id):
        self.PSQL_LOGIN_CMD = PSQL_LOGIN_CMD
        self.fb_id = fb_id
        self.conn = None
        self.curs = None

    # Establish connection to db
    def Connect(self):
        try:
            self.conn = psycopg2.connect(self.PSQL_LOGIN_CMD)
            self.curs = self.conn.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
        except Exception as e:
            return e

    # Disconnect from db
    def Disconnect(self,):
        self.curs.close()
        self.curs = None
        self.conn.close()
        self.conn = None

    def get_user_row(self):
        self.curs.execute("SELECT * FROM reminders WHERE fb_id=%s", (self.fb_id,))
        return self.curs.fetchone() # We should never get more than one

    def Set_username(self):
        pass

    def Set_daily_goal(self):
        pass

    def Set_reminder(self):
        pass

    def Disable_reminder(self):
        pass
