import psycopg2

# Establish command to db
def connect(PSQL_LOGIN_CMD):
    conn = None
    try:
        print("connecting")
        conn = psycopg2.connect(PSQL_LOGIN_CMD)
      
        # create a cursor
        cur = conn.cursor()
        
        cur.execute("")
 
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print("connectiong closed")
