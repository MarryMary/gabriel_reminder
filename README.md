# ガヴちゃんリマインダー on discord
ガヴちゃんがdiscord上で予定をリマインドしてくれます  

# サ終
Herokuじゃ動かせなくなったのでこういう悲しい結果で終わりですね・・・(サ終)


# ファイル説明
* main.py
  * botの全てを司るファイルです。主に設定への反応やヘルプの表示を担当しています。  
* cronExec.py
  * cronで実行されるべきファイルです。データベースから取得したデータからdiscordにリマインドを送信します。  
* database.sql
  * データベース構成です。postgre SQLでの記法になっています。
* help.txt
  * ヘルプが書かれたファイルです。ヘルプ表示時はこのファイルを見ています。
* Procfile
  * herokuで動作させる際のコマンドが記述されています。  
* requirements.txt
  * このbotを動作させるのに必要なモジュールが記載されたファイルです。
* runtime.txt
  * このbotを動作させるために使用するpythonバージョンを記載しています。python 3.10.5 で動作させています。

# 動作イメージ
![image](https://user-images.githubusercontent.com/92404990/182513133-634cf87b-16d4-49f8-b88e-8c5aeb777d92.png)  
![image](https://user-images.githubusercontent.com/92404990/182513151-61bb04ec-992f-41a7-95f8-c1fdb6fb41e6.png)  
![image](https://user-images.githubusercontent.com/92404990/182513174-22aa4207-6c23-4a23-8ed2-9eb50d4db2ef.png)  
![image](https://user-images.githubusercontent.com/92404990/182513199-726125b1-3b64-4f2b-93d5-4276ad5e4d55.png)  
![image](https://user-images.githubusercontent.com/92404990/182513263-8ef50248-2264-4b65-8135-443fa4cb78b5.png)  
![image](https://user-images.githubusercontent.com/92404990/182513366-82384c87-1a16-4c72-bce1-dc3a3d997032.png)   


# なぜ時間に正確性がないのか
ガヴちゃんが割とルーズだからです（大嘘）  
heroku scheduler（cronみたいなもの、任意の処理を定期実行できるサービス）のインターバルの最低時間が10分だからです。  
つまりheroku schedulerの実行が一旦9:00に終了し、次の実行時間が9:10の場合、9:05に設定したリマインダーも全て9:10に実行されるということになります。

# 使い方
「@ガヴ」はメンション(bot指名)を指します。  

* @ガヴ  
  - ヘルプが表示されます  

* @ガヴ 1day  
  - リマインドが設定されます  

* $明日  
  - リマインドが設定されます(メンション省略記法)  
  

(何らかのメッセージへのリプライとして以下を記述)
* 明日  
  - リマインドが設定されます(省略記法)  

# 記法詳細
メンション記法で説明しますが、いずれの記法でも使用できます。
* @ガヴ 明日  
  - 日を指定すると指定した日の朝9時にリマインドされます。使える指定については下の「使える指定」の項目を参照して下さい。  

* @ガヴ 明日 8:00  
  - 日、時間をスペース区切りで指定すると指定日時にリマインドされます。
  - 例では明日の朝8時にリマインドされます。24時間表記で指定してください。マイナスは絶対値に置換されます。  

* @ガヴ 明日 8:00 歯医者  
  - 日、時をスペース区切りで指定した後にスペースを入れてメッセージを入力するとカスタムメッセージ(リマインド時にガヴちゃんがカスタムメッセージ付きでリマインド)が設定できます。  
  - 例では明日の朝8時に以下のように歯医者とリマインドされます。  
  -「@ユーザー名 、前に自分で歯医者って言ってたの忘れてない？」  

# 使える指定
* 今日 または today  
  - 本日リマインドが設定されます(時間指定しない場合はリマインドされません。)  

* 明日 または tommorow  
  - 翌日にリマインドが設定されます  

* 明後日 または daftommorow  
  - 翌々日にリマインドが設定されます(daftommorow → day after tommorowの意)  
  
以下、Xには任意の整数（1, 2, 3...）が入ります。  
分・時間単位で指定された際に同時に時刻が指定されていた場合、分・時間指定を優先して設定します。  
また、分・時間単位での指定では必ずしも正確に指定の時間にリマインドされる保証はできません。  

* Xminute  
  - 指定した分後にリマインドが設定されます。10分単位で指定できます。1分単位で指定しても10分単位の指定に置き換わります。  

* Xhour  
  - 指定した時間後にリマインドが設定されます。  

* Xday  
  - 指定した日にちが経過した後にリマインドが設定されます。(e.g. 2day → 2日後) 
 
* Xweek
  - 指定した週が経過した後にリマインドが設定されます(e.g. 2week → 2週間後)

* Xmonth  
  - 指定した月が経過した後にリマインドが設定されます。(e.g. 2month → 2ヶ月後)  

* Xyear
  - 指定した年が経過した後にリマインドが設定されます。(e.g. 2year → 2年後)  
