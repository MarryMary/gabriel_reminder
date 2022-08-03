import re
import discord
import database
from datetime import datetime
from datetime import timedelta

client = discord.Client()
VERSION = "1.0"

# int判定関数
def isint(s):
    try:
        int(s, 10)
    except ValueError:
        return False
    else:
        return True

# メッセージ内から日時やカスタムメッセージを抜き出すための関数
def read(message):
    # 1day 2dayのエイリアスをリストで保管
    command = ["tommorow", "daftommorow", "明日", "明後日"]
    # 現在時刻を取得
    day = datetime.now()

    # スペースを基に文字列を配列に変換
    message_exploded = message.split()

    # 日付が入っているリストのキーと時間が入っているリストのキーの初期値を設定（1day 8:00 → ["1day", "8:00"]になるので、0番が日付、1番が時間になる。）
    day_key = 0
    time_key = 1

    # リストが2つ以上（["1day", "8:00"]のように指定）あるかどうか（時間指定がない場合はtimeはNoneになる）
    if len(message_exploded) >= 2:
        day_key = 0
        time_key = 1
    elif len(message_exploded) == 1:
        day_key = 0
        time_key = None
        
    # ユーザー指定から日付指定のある部分のみ抽出
    days = message_exploded[day_key]

    # エイリアスを正しい指定に変換
    if days.strip() in command:
        if days.strip() == "tommorow" or days.strip() == "明日":
            days = "1day"
        elif days.strip() == "today" or days.strip() == "今日":
            days = "0day"
        else:
            days = "2day"

    # 分・時間・日・週・月・年のどれで指定されているかを確認、今日の日付(datetime)に対して適切なものをtimedeltaで加算する
    if "min" in days:
        day = day + timedelta(minutes=abs(int(days.replace("minute", ""))))

    elif "hour" in days:
        day = day + timedelta(hours=abs(int(days.replace("hour", ""))))

    elif "day" in days:
        day = day + timedelta(days=abs(int(days.replace("day", ""))))
    
    elif "week" in days:
        day = day + timedelta(days=abs(int(days.replace("week", ""))))

    elif "month" in days:
        day = day + timedelta(months=abs(int(days.replace("month", ""))))

    elif "year" in days:
        day = day + timedelta(years=abs(int(days.replace("year", ""))))
    
    # デフォルトでは朝9時
    day = day.replace(hour = 9, minute = 0, second = 0, microsecond = 0)

    # 時間指定がある、または分・時間がすでに日付で指定されていない場合（指定がある場合は分・時間指定を優先）
    if time_key is not None and "minute" not in days and "hour" not in days:
        # 時間を「:」で配列に変換（8:00 → ["8", "00"]）
        times_exploded = message_exploded[time_key].split(":")
        # 両者数字だった場合
        if isint(times_exploded[0]) and isint(times_exploded[1]):
            # 分まで指定されている場合（8:00）
            if len(times_exploded) == 2:
                day = day.replace(hour = abs(int(times_exploded[0])), minute = abs(int(times_exploded[1])), second = 0)
            # 秒まで指定されている場合(8:00:00)
            elif len(times_exploded) == 3:
                if isint(message_exploded[2]):
                    day = day.replace(hour  = abs(int(times_exploded[0])), minute = abs(int(times_exploded[1])), second = abs(int(times_exploded[2])))
                # 秒指定が数字でない場合はNoneに
                else:
                    time_key = None
        # 時間・分指定が数値でなかった場合はNoneに
        else:
            time_key = None
    # 時間指定がない場合、または分・時間がすでに日付で指定されている場合はNoneに
    else:
        time_key = None

    # ユーザーの発言から日付指定を削除
    message_exploded.pop(0)

    # 時間指定もある場合は時間指定も削除
    if time_key is not None:
        message_exploded.pop(0)
    
    # 配列に残った文字を配列から文字列に戻してカスタムメッセージとして設定
    custom_message = "".join(message_exploded)

    # カスタムメッセージが空白だけ、空だった場合はカスタムメッセージを空文字にする
    if custom_message.strip() == "":
        custom_message = ""

    # 完成した日時指定とカスタムメッセージをタプルで返却
    return day, custom_message


# bot起動時に実行される関数
@client.event
async def on_ready():
    # 起動確認のために文字列を表示（herokuの場合はログ画面に表示される）
    print("Welcome to Remmy the reminder bot program with Python!")
    print(f'Version: {VERSION}')

# ユーザーが何か発言した場合
@client.event
async def on_message(message):
    # messageオブジェクトをraw_messageとして保存（後でmessage変数を上書きするため）
    raw_message = message
    # botがメンションされたか
    if client.user in message.mentions:
        # 正規表現でメンション部分を削除(@ガヴ のようなメンションは内部的に <@123456789...>のような文字列になっているため、<@>の囲み文字を検索して削除すれば良い)
        check = re.sub("<@.*>", "", message.content)

        # 発言者がbotだった場合はスルーする
        if message.author.bot:
            return
        
        # メンションだけされた場合はヘルプ（使い方）を出す
        elif check.strip() == "":
            with open('help.txt', 'r') as f:
                helps = f.read()
            await raw_message.channel.send(helps)
        # それ以外
        else:
            # もし誰かの発言の返信にぶら下がってメンションされた場合
            if message.reference is not None:
                 # 正規表現でメンション部分を削除して、read関数（ファイル上部で定義している関数）で日付とカスタムメッセージを抽出
                received = re.sub("<@.*>", "", message.content)
                res, cmessage = read(received)
                # guildid(サーバーの内部識別id)
                gld = message.guild.id
                # channel_id(チャンネルの内部識別id)
                channel = message.channel.id
                # user(botをメンションしてきたユーザーのid)
                user = message.author.id
                # message_id(ユーザーがメンション時に返信していたメッセージの内部識別ID)
                message = message.reference.message_id
                # データベースに登録（詳細はdatabase.py参照）
                database.register(res, gld, channel, user, message, cmessage)

                # 応答用のメッセージを作成
                reply = f"<@{user}> おけおけ、じゃあ{received}で設定しとくから。"

                # 送信
                await raw_message.channel.send(reply)
            # 返信ではなく単にメッセージだった場合
            else:
                # 正規表現でメンション部分を削除して、read関数（ファイル上部で定義している関数）で日付とカスタムメッセージを抽出
                received = re.sub("<@.*>", "", message.content)
                res, cmessage = read(received)
                # guildid(サーバーの内部識別id)
                gld = message.guild.id
                # channel_id(チャンネルの内部識別id)
                channel = message.channel.id
                # user(botをメンションしてきたユーザーのid)
                user = message.author.id
                
                database.register(res, gld, channel, user, None, cmessage)

                # 応答用のメッセージを作成
                reply = f"<@{user}> おけおけ、じゃあ{received}で設定しとくから。"

                # 送信
                await raw_message.channel.send(reply)
    # もし冒頭が$で始まっていたら（メンション省略記法）
    elif message.content.startswith("$"):
        # 内部処理はメンション時と同じ
        # TODO 関数化

        if message.reference is not None:
            received = message.content.strip()[1:]
            res, cmessage = read(received)
            gld = message.guild.id
            channel = message.channel.id
            user = message.author.id
            message = message.reference.message_id
            database.register(res, gld, channel, user, message, cmessage)

            reply = f"<@{user}> おけおけ、じゃあ{received}で設定しとくから。"
            await raw_message.channel.send(reply)
        else:
            received = message.content.strip()[1:]
            res, cmessage = read(received)
            gld = message.guild.id
            channel = message.channel.id
            user = message.author.id
            database.register(res, gld, channel, user, None, cmessage)

            reply = f"<@{user}> おけおけ、じゃあ{received}で設定しとくから。"
            await raw_message.channel.send(reply)
    
    # 返信時（すべての返信に反応）
    elif message.reference is not None:
        # 分指定や時間指定が入っているかどうか
        pattern_list = [r"[0-9]+min", r"[0-9]+hour", r"[0-9]+day", r"[0-9]+week", r"[0-9]+month", r"[0-9]+year"]
        day_list = ["明日", "tommorow", "明後日", "daftommorow"]

        # botに向けたものかどうかの判定フラグ
        flag = False

        # pattern内に文字が入っているか
        for pattern in pattern_list:
            match = re.search(pattern, message.content)
            if match is None:
                flag = False
            elif match is not None and flag:
                flag = False
            elif match is not None:
                flag = True
            else:
                flag = False
        
        # daylist内に文字が入っているか
        for daylist in day_list:
            if daylist in message.content and flag:
                flag = False
            elif daylist in message.content:
                flag = True
            elif daylist not in message.content:
                flag = False
            else:
                flag = False
        
        # flagがtrueなら
        if flag:
            # 以下はメンション時と同じ
            # todo 関数化
            received = message.content
            res, cmessage = read(received)
            gld = message.guild.id
            channel = message.channel.id
            user = message.author.id
            message = message.reference.message_id
            database.register(res, gld, channel, user, message, cmessage)

            reply = f"<@{user}> おけおけ、じゃあ{received}で設定しとくから。"
            await raw_message.channel.send(reply)
            






client.run("YOUR BOT ACCESS TOKEN")