# やぁ

import discord
from discord.ext import commands
import RPi.GPIO as GPIO
from colorama import init, Back, Style
import datetime
import asyncio
import time
import threading
import sys

intents = discord.Intents.all()
intents.members = True
Client = commands.Bot(command_prefix='!', intents=intents)
user_id = 869870003338493962
last_executed = datetime.datetime.min  # 最後にコマンドが実行された時刻
init()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# 起動
@Client.event
async def on_ready():
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} Bot起動完了")
    # 緑色LED
    GPIO.output(19, True)
    time.sleep(3)
    GPIO.output(19, False)

# {command}コマンドなんかねぇよ。うるせえよ。黙れよ。
@Client.event
async def on_command_error(ctx, error):
    now = datetime.datetime.now()
    if isinstance(error, commands.CommandNotFound):
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mが存在しないコマンドを実行しました。")
        await ctx.send("このコマンドは存在しません。")

# 動作確認
@Client.command()
async def test(ctx):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    username = ctx.author.name
    print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがtestコマンドを実行しました。")
    await ctx.send("BotはPythonで正常に動作しています。")

    user_id = ctx.author.id
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
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    username = ctx.author.name
    print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがhsコマンドを実行しました。")
    await ctx.send("```!hs コマンドの使い方を表示\n!test botが正常に動作しているか確認\n!yd サーバー管理者に来てほしいとき、メンションしても来ない時に使う```")

# さちぬへも呼び出し
@Client.command()
async def yd(ctx):
    now = datetime.datetime.now()

    def check_time():
        if now.hour >= 21 or now.hour < 8:
            return False
        return True

    global last_executed
    delta = now - last_executed
    if delta.total_seconds() < 600:
        # 前回実行が10分以内
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがydコマンドを実行しましたが、前回実行が10分以内のため、処理は行われません。")
        await ctx.send("前回実行が10分以内でしたので、このコマンドを使用することができません。しばらく待ってからコマンドを実行してください。")
        return

    if check_time():
        last_executed = now
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがydコマンドを実行しました。")
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
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがydコマンドを実行しましたが、使用できる時間帯ではないため、処理は行われません。")
        await ctx.send("このコマンドは21時～8時は使用できません。")

# Pythonプログラム終了
@Client.command()
async def exit(ctx):
    now = datetime.datetime.now()
    # アカウント使用制限
    user_id = ctx.author.id
    if user_id == 869870003338493962:
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがexitコマンドを実行しました。Pythonプログラムを終了します。")
        await ctx.send("プログラムを終了します。")
        # 赤色LED
        GPIO.output(13, True)
        time.sleep(5)
        GPIO.output(13, False)
        sys.exit()

    else:
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        username = ctx.author.name
        print(f"{timestamp} \033[36m{ctx.author.name}#{ctx.author.discriminator}\033[39mがexitコマンドを実行しましたが、使用できる権限ではないため、処理は行われません。")
        await ctx.send("exitコマンドを使用する権限はありません。")

Client.run('TOKEN')
