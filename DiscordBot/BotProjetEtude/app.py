import discord
from discord.ext import commands
import fonctionnalite as f
from datetime import datetime
import threading
import asyncio
import json

intents = discord.Intents().all()
intents.message_content = True
idToken = "MTE4MTU3MzU3OTMxNDI5ODkwMg.G5hllA.S5ZKYd_CbZj3-ibgQbQYZTCFcpaAEmAMzT2VD0"
prefix = '.'

nasa = commands.Bot(command_prefix=prefix, intents=intents)

@nasa.command(name='photo')
async def photo(ctx):
    await f.afficherApod(ctx)

@nasa.command(name='apod')
async def apod(ctx):
    await f.afficherApod(ctx)

    


async def write_channel_id_to_file(server_id, channel_ids):
    data = {}
    try:
        with open("BotProjetEtude/Conf.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    
    data[str(server_id)] = channel_ids
    
    with open("BotProjetEtude/Conf.json", "w") as file:
        json.dump(data, file)

@nasa.command(name='config')
async def config(ctx):
    server_id = ctx.guild.id
    channel_id = ctx.channel.id
    
    data = {}
    try:
        with open("BotProjetEtude/Conf.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass
    
    if str(server_id) in data:
        if channel_id in data[str(server_id)]:
            data[str(server_id)].remove(channel_id)
            await ctx.send(f"Channel ID {channel_id} removed from the list.")
        else:
            data[str(server_id)].append(channel_id)
            await ctx.send(f"Channel ID {channel_id} added to the list.")
    else:
        data[str(server_id)] = [channel_id]
        await ctx.send(f"Channel ID {channel_id} added to the list.")
    
    with open("BotProjetEtude/Conf.json", "w") as file:
        json.dump(data, file)


async def checkTimeWrapper():
    while True:
        await checkTime()
        await asyncio.sleep(1)  # Attendre 1 seconde entre chaque vérification

async def read_channel_ids_from_file():
    try:
        with open("BotProjetEtude/Conf.json", "r") as file:
            data = json.load(file)
            return list(data.values())  # Renvoyer uniquement les valeurs du dictionnaire
    except FileNotFoundError:
        return []

    
async def checkTime():
    now = datetime.now()
    current_time = now.strftime("%H")
    if current_time in ['09']:  # vérifie si la minute se termine par 0 ou 5
        list_channel_ids = await read_channel_ids_from_file()
        for channel_ids in list_channel_ids:
            for channel_id in channel_ids:
                channel = nasa.get_channel(channel_id)
                await f.afficherApodTest(channel)
    await asyncio.sleep(3600)
        
async def main():
    task1 = asyncio.create_task(checkTimeWrapper())  # exécuter checkTimeWrapper en arrière-plan
    await nasa.start(idToken)  # exécuter nasa.run(idToken) dans le thread principal

asyncio.run(main())
