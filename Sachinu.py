import discord
from discord.ext import commands
import RPi.GPIO as GPIO
import datetime
import time
import threading
import sys

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

# 起動確認
@bot.event
async def on_ready():
    print("Bot起動完了")
    # 緑色LED
    GPIO.output(19, True)
    time.sleep(3)
    GPIO.output(19, False)

# 動作確認
@bot.command()
async def test(ctx):
    print(f"{ctx.author.name}がtestコマンドを実行しました。Botは正常に動作しています。")
    await ctx.send("Botは正常に動作しています。")

#help
@bot.command()
async def hs(ctx):
    print(f"{ctx.author.name}がhsコマンドを実行しました。")
    await ctx.send("```!hs コマンドの使い方を表示\n!yd サーバー管理者に来てほしいとき、メンションしてもなかなか来ない時に使うと来るかもしれません。```")

# 呼び出し
executed = {}

@bot.command()
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
            print(f"{ctx.author.name}がydコマンドを実行しましたが10分以内にすでに実行しているため、処理は行われませんでした。")
            await ctx.send("10分以内に実行しましたので、このコマンドを使用することができません。")
            return
    
    if check_time():
        executed[user_id] = now
        print(f"{ctx.author.name}がydコマンドを実行しました。")
        await ctx.send("さちぬへもを呼びます。")
        def task1():
            l = 0
            while (l < 30):
                GPIO.output(13, True)    # 黄色LED
                GPIO.output(19, True)
                time.sleep(1)
                GPIO.output(13, False)
                GPIO.output(19, False)
                time.sleep(1)
                l += 1

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
        print(f"{ctx.author.name}がydコマンドを実行しましたが使用できる時間帯ではなかったため、処理は行われませんでした。")
        await ctx.send("現在の時間帯は使用できません。")

# Pythonプログラム強制終了
@bot.command()
async def exit(ctx):
    # アカウント使用制限
    allowed_user_id = 869870003338493962
    if ctx.author.id != allowed_user_id:
        print(f"{ctx.author.name}がexitコマンドを実行しましたがさちぬへも以外のため、処理は行われませんでした。")
        await ctx.send("このコマンドは使用しないでください。")
        return

    print("exitコマンド実行しました。5秒後にPythonプログラムを終了します。")
    await ctx.send("5秒後にPythonプログラムを終了します。")
    # 赤色LED
    GPIO.output(13, True)
    time.sleep(5)
    GPIO.output(13, False)
    sys.exit()

bot.run('')
