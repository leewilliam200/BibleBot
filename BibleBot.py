import os
from datetime import datetime
import discord
from discord.ext import commands, tasks
import asyncio
import json

async def bible(group, id):
    channel = client.get_channel(id)
    for key, value in group.items():
        if value[1] == "":
            response = f'{value[0]} has not done their QT\n'
            await channel.send(response)

token_file = open("tokens.json", "r")
token = json.load(token_file)
DISCORD_TOKEN = token[0]["token"]
GROUP_id = token[1]["group"]
client = discord.Client()

@client.event
async def on_ready():
    print("hi")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    channel_id = message.channel.id
    txt = message.content.lower()
    json_file = open("boys.json", "r")
    group = json.load(json_file)
    if txt == 'done':
        if str(channel_id) == str(GROUP_id):
            for key, value in group.items():
                if key == str(message.author.id):
                    value[1] = '1'
                    response = f'ok {value[0]}'
                    await message.channel.send(response)
                    print(group)
    json_file2 = open("boys.json", "w")
    json.dump(group, json_file2)


@tasks.loop(hours=24)
async def called_once_a_day():
    json_file = open("boys.json", "r")
    group = json.load(json_file)
    await bible(group, GROUP_id)

    channel1 = client.get_channel(GROUP_id)

    now = datetime.now()
    date = now.strftime("%d")
    month = now.strftime("%m")
    year = now.strftime("%Y")

    response = f"Today's QT is https://www.duranno.com/livinglife/qt/?OD={date}-{month}-{year}"

    await channel1.send(response)

    reset = open("fresh.json", "r")
    group = json.load(reset)
    json_file2 = open("boys.json", "w")
    json.dump(group, json_file2)

@called_once_a_day.before_loop
async def before():
    time = datetime.now()
    h = time.strftime("%H")
    m = time.strftime("%M")
    s = time.strftime("%S")

    if int(h) < 9:
        sleeptime = 9*60*60 - (int(h) * 60 * 60 + int(m) * 60 + int(s))
    else:
        sleeptime = 24*60*60 - (int(h) * 60 * 60 + int(m) * 60 + int(s)) + 9*60*60
    print(sleeptime)
    await asyncio.sleep(sleeptime)
    await client.wait_until_ready()

called_once_a_day.start()
client.run(DISCORD_TOKEN)