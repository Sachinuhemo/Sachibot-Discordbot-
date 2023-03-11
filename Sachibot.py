from xmlrpc import client
import discord
from discord.ext import commands
import RPi.GPIO as GPIO
import datetime
import asyncio
import time
import threading
import sys

intents = discord.Intents.all()
intents.members = True
Client = commands.Bot(command_prefix='!', intents=intents)
GPIO.setwarnings(False)
executed = {}
user_id = 869870003338493962
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# 起動
@Client.event
async def on_ready():
    print("Bot起動完了")
    # 緑色LED
    GPIO.output(19, True)
    time.sleep(3)
    GPIO.output(19, False)

# 存在しないこのコマンド
@Client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        print(f"{ctx.author.name}#{ctx.author.discriminator}が存在しないコマンドを実行しました。")
        await ctx.send("このコマンドは存在しません。")

# 動作確認
@Client.command()
async def test(ctx):
    print(f"{ctx.author.name}#{ctx.author.discriminator}がtestコマンドを実行しました。Botは正常に動作しています。")
    await ctx.send("BotはPythonで正常に動作しています。")

    if user_id == 869870003338493962:
        GPIO.output(13,True)
        GPIO.output(6,True)
        time.sleep(1)
        GPIO.output(13,False)
        GPIO.output(6,False)
        GPIO.output(19,True)
        time.sleep(1)
        GPIO.output(19,False)
        GPIO.output(26,True)
        time.sleep(1)
        GPIO.output(26,False)

# コマンド一覧
@Client.command()
async def hs(ctx):
    print(f"{ctx.author.name}#{ctx.author.discriminator}がhsコマンドを実行しました。")
    await ctx.send("```!hs コマンドの使い方を表示\n!test botが正常に動作しているか確認\n!yd サーバー管理者に来てほしいとき、メンションしても来ない時に使う```")

# 呼び出し
@Client.command()
async def yd(ctx):
    now = datetime.datetime.now()
    user_id = str(ctx.author.id)

    def check_time():
        if now.hour >= 21 or now.hour < 8:
            return False
        return True

    if user_id in executed:
        delta = now - executed[user_id]
        if delta.total_seconds() < 600:
            # 前回実行が10分以内
            print(f"{ctx.author.name}#{ctx.author.discriminator}がydコマンドを実行しましたが、10分以内にすでに実行しているため、処理は行われませんでした。")
            await ctx.send("10分以内に実行しましたので、このコマンドを使用することができません。")
            return
    
    if check_time():
        executed[user_id] = now
        print(f"{ctx.author.name}#{ctx.author.discriminator}がydコマンドを実行しました。")
        await ctx.send("さちぬへもを呼びます。")

        def task1():
            led = 0
            while (led < 30):
                GPIO.output(13, True)    # 黄色LED
                GPIO.output(19, True)
                time.sleep(1)
                GPIO.output(13, False)
                GPIO.output(19, False)
                time.sleep(1)
                led += 1

        def task2():
            b = 0
            while (b < 3):
                GPIO.output(6, True)    # ブザー
                time.sleep(0.1)
                GPIO.output(6, False)
                time.sleep(0.1)
                b += 1

        thread1 = threading.Thread(target=task1)
        thread2 = threading.Thread(target=task2)
        thread1.start()
        thread2.start()
        
    else:
        # 21:00 ～ 8:00 実行
        print(f"{ctx.author.name}#{ctx.author.discriminator}がydコマンドを実行しましたが、使用できる時間帯ではなかったため、処理は行われませんでした。")
        await ctx.send("現在の時間帯は使用できません。")

# Pythonプログラム強制終了
@Client.command()
async def exit(ctx):
    # アカウント使用制限
    if ctx.author.id != user_id:
        print(f"{ctx.author.name}#{ctx.author.discriminator}がexitコマンドを実行しましたが、さちぬへも以外のため、処理は行われませんでした。")
        await ctx.send("exitコマンドは使用しないでください。")
        return

    print("exitコマンド実行しました。プログラムを終了します。")
    await ctx.send("プログラムを終了します。")
    # 赤色LED
    GPIO.output(13, True)
    time.sleep(5)
    GPIO.output(13, False)
    sys.exit()

Client.run('TOKEN')
