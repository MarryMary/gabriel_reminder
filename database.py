# heroku postgreを使うので接続用にpsycopg2というモジュールを使用します。
import psycopg2

# データベースとのコネクションを作成して返却します。
def connection():
    conn = psycopg2.connect("YOUR CONNECT URL")
    return conn

# 予定を登録する関数
def register(when, server, channel, user, message, cmessage):
    conn = connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO reminder(when_data, gld_id, ch_id, say_user_id, message_id, custom_message) VALUES(%s, %s, %s,%s, %s, %s)",
        (when, server, channel, user, message, cmessage)
    )
    conn.commit()

# 予定を取得する関数（現在時刻よりも前の予定を取得した後に削除）
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