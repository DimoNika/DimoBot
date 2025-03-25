import discord # Подключаем библиотеку
from discord.ext import commands

from discord.ext.commands.context import Context

from discord import FFmpegPCMAudio

import yt_dlp
import uuid
import os
import asyncio
# URL of the video you want to download


# Define options for the download
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}
# Create a downloader object
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     # Download the video
#     ydl.download([video_url])





intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
# Задаём префикс и интенты
bot = commands.Bot(command_prefix='!', intents=intents) 

# С помощью декоратора создаём первую команду
@bot.command()
async def ping(ctx):
    await ctx.send('pong')



@bot.command()
async def join(ctx: Context):
    
    await ctx.send('Joining')
    if ctx.voice_client != None:
        await ctx.voice_client.disconnect()
        channel = ctx.message.author.voice.channel
        
        await channel.connect()

    if ctx.voice_client == None:

        channel = ctx.message.author.voice.channel
        
        await channel.connect()




async def play_again(ctx, song_name):
    
    await play(ctx, video_url=song_name)

@bot.command(name="play")
async def play(ctx: Context, video_url, r=None):
    """!play (place yt url)"""
    print(ctx)
    await ctx.send('Got your request...')
    
    
        
    if ctx.author.voice:
        if ctx.voice_client is  None:

            channel = ctx.message.author.voice.channel
            await channel.connect()
  

    else:
        await ctx.send('You are not in voice')

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # music = await ydl.download([video_url])
        await ctx.send('Loading...')

        info_dict = ydl.extract_info(video_url, download=True)
        file_name = ydl.prepare_filename(info_dict)
        
        await ctx.send('Playing!')

    if ctx.voice_client is not None:
        voice = ctx.voice_client
        
        
        real_file_name = file_name[:-5] + ".mp3"
        
        uid = str(uuid.uuid4())
        new_real_file_name = real_file_name.replace(".mp3", uid + ".mp3")
        os.rename(real_file_name, new_real_file_name)
        source = FFmpegPCMAudio(new_real_file_name)

        # async def play_song():
            
        #     voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(play_song(), bot.loop) if r == "r" else None)
        #     # voice.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(ctx.send(new_real_file_name), bot.loop) if r == "r" else None)


        # await play_song()

        player = voice.play(source)
        

        

@bot.command()
async def leave(ctx: Context):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Disconnected from the voice channel.")
    else:
        await ctx.send("I'm not connected to any voice channel.")


from . import config


bot.run(config.token)


