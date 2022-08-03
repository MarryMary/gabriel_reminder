# cron実行用pythonファイル
import database
import discord

client = discord.Client()

# データベースからデータを取得（詳しくはdatabase.pyを参照）
result = database.gather()

# 実行時呼び出し関数
@client.event
async def on_ready():
    # 起動確認
    print("Start up remmy cron remind system.")

    # データベースから取得してきたデータをループ
    for res in result:
        # guildid(サーバーの内部識別ID)
        gld = int(res[2])
        # channelid(チャンネルの内部識別ID)
        channel = int(res[3])
        # userid(設定したユーザーの内部識別ID)
        user = res[4]
        # もしも返信での設定がされていた場合
        if res[5] is not None:
            # 返信先のメッセージID
            message = int(res[5])
        # 返信ではなく単にメッセージだった場合
        else:
            message = None
        # カスタムメッセージ
        custom_message = res[6]

        # カスタムメッセージが設定されている場合のリマインドの文言
        if custom_message != "":
            text = f"<@{user}> 、前に自分で{custom_message}って言ってたの忘れてない？"
        # カスタムメッセージ未設定のリマインドの文言
        else:
            text = f"<@{user}> 忘れてない？"
        
        # 送信先チャンネルの指定
        send_channel = client.get_guild(gld).get_channel(channel)

        # 返信でのリマインド設定ではない場合はそのままメッセージを送信
        if message is None:
            await send_channel.send(content = text)
        # 返信でのリマインド設定の場合は、返信先のメッセージを指定してそれに返信する形でメッセージを送信
        else:
            access_message = await send_channel.fetch_message(message)
            await send_channel.send(content = text, reference = access_message.to_reference())
    # 処理が終了したらexit()でプログラムを終了
    exit()

client.run("YOUR BOT ACCESS TOKEN")