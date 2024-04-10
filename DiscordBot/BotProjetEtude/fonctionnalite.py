import discord
from discord.ext import commands
from datetime import datetime
import threading
import asyncio
import json
import requests

async def afficherApod(ctx):
    try:
        url = "https://api.nasa.gov/planetary/apod?api_key=EdRYiRLsuOhTjpIAueGPfK68E22UcKFqfOSCkM1a"
        response = requests.get(url).json()

        if "youtube" in response['url']:
            await ctx.send(f"{response['title']} \n {imageFromVideo(response['url'])}")
        else:
            embed = discord.Embed(title=response['title'], description=response['explanation'], color=0x000080)
            embed.set_image(url=response['url'])
            embed.set_footer(text=f"Date: {datetime.now().strftime('%Y-%m-%d')}")
            await ctx.reply(embed=embed, mention_author=False)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

def getVideoId(embed_link):
    embed_link_split = embed_link.split('/')
    video_id_with_params = embed_link_split[4]
    head, sep, tail = video_id_with_params.partition('?')
    video_id = head
    final_youtube_link = f'https://www.youtube.com/watch?v={video_id}'
    return video_id

def imageFromVideo(url):
    return "http://img.youtube.com/vi/%s/0.jpg" % getVideoId(url)

async def write_channel_id_to_file(channel_id):
    with open("BotProjetEtude/channel_ids.txt", "r+") as file:
        file.seek(0)
        channel_ids = file.read().splitlines()
        if str(channel_id) in channel_ids:
            channel_ids.remove(str(channel_id))
            file.seek(0)
            file.truncate()
            file.write("\n".join(channel_ids))
            file.write("\n")
            return f"ID {channel_id} removed from the file."
        else:
            file.write(str(channel_id) + "\n")
            return f"ID {channel_id} added to the file."

async def afficherApodTest(channel):
    try:
        accessKey = "EdRYiRLsuOhTjpIAueGPfK68E22UcKFqfOSCkM1a"
        url = "https://api.nasa.gov/planetary/apod?api_key=" + accessKey
        response = requests.get(url).json()

        if "youtube" in response['url']:
            await ctx.send(f"{response['title']} \n {imageFromVideo(response['url'])}")
        else:
            embed = discord.Embed(title=response['title'], description=response['explanation'], color=0x000080)
            embed.set_image(url=response['url'])
            embed.set_footer(text=f"Date: {datetime.now().strftime('%Y-%m-%d')}")
            await channel.send(embed=embed)
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
