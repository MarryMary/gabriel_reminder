import psycopg2

def connection():
    conn = psycopg2.connect("YOUR CONNECT URL")
    return conn

def register(when, server, channel, user, message, cmessage):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reminder(when_data, gld_id, ch_id, say_user_id, message_id, custom_message) VALUES(%s, %s, %s,%s, %s, %s)",
        (when, server, channel, user, message, cmessage)
    )
    conn.commit()

def gather():
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM reminder WHERE when_data <= localtimestamp"
    )
    res = cur.fetchall()
    cur.execute(
        "DELETE FROM reminder WHERE when_data <= localtimestamp"
    )
    conn.commit()
    return res