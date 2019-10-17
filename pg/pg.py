import psycopg2

# Establish connection to db
def Connect(PSQL_LOGIN_CMD):
    try:
        conn = psycopg2.connect(PSQL_LOGIN_CMD)
        curs = conn.cursor()
        return conn, curs, None
    except Exception as e:
        return None, None, e

# Disconnect from db
def Disconnect(conn, curs):
    curs.close()
    conn.close()

def Set_username(curs):
    curs.execute()

def Set_daily_goal(curs):
    curs.execute()

def Set_reminder(curs):
    curs.execute()

def Disable_reminder(curs):
    curs.execute()