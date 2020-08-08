import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os
from os import system
from discord import Spotify
import spotdl
import shutil

client = commands.Bot(command_prefix = ".")
client.remove_command('help')

global name

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('With my own life'))
    print('Bot is ready.')


@client.command()
async def ping(ctx):
    await ctx.send(f"Your ping is :{round(client.latency * 1000)} ms")


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')                     #change
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send(f"""Welcome to the server {member.mention}""")
@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')
    for channel in member.guild.channels:                   #change
        if str(channel) == "general":
            await channel.send(f"""Member has been Kicked/Removed from server {member.mention}""")

@client.command()
async def clear(ctx,amount=5):
    await ctx.channel.purge(limit=amount)


@client.command()
async def khela(ctx):
    await ctx.channel.send("if you want to play you can call me")
   
@client.command()
async def aaja(ctx):
    await ctx.channel.send("if you want to play you can call me")

@client.command()
async def phone(ctx):
    await ctx.channel.send("if you don't have my Phone no Then don't Bothere")
@client.command()
async def users(ctx):
    id = client.get_guild(guild id)
    await ctx.channel.send(f"""Total Members in this Server is: {id.member_count}""")
@client.command()
async def hi(ctx):
    await ctx.channel.send("hello")
@client.command()
async def help(ctx):  
    embed = discord.Embed(title="What can killer Frost do?",description="Some useful commands")
    embed.add_field(name="hi",value="Greets the user")
    embed.add_field(name="users",value="Prints no of users")
    embed.add_field(name="khela",value="message")
    embed.add_field(name="join",value="add bot to voice channel")
    embed.add_field(name="leave",value="remove bot from voice channel")
    embed.add_field(name="play youtube link..",value="play the song")
    embed.add_field(name="pause",value="pause the song")
    embed.add_field(name="resume",value="resume the song")
    embed.add_field(name="stop",value="stop the song")
    embed.add_field(name="info",value="some basic details")    
    embed.add_field(name="ping",value="Tells you ping")
    await ctx.channel.send(content=None, embed=embed)


@client.command()
async def info(ctx):  
    embed = discord.Embed(title="About Killerfrost?",description="Some details")
    embed.add_field(name="Owner",value="Ishan rajpal")
    embed.add_field(name="Capabilities",value="play music and do some stuffs")
    await ctx.channel.send(content=None, embed=embed)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('valid command use karo please')

@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"the bot is connected to {channel}\n")

    await ctx.send(f"joined{channel}")

@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"the bot has left{channel}")
        await ctx.send(f"left{channel}")
    else:
        print("not in one")
        await ctx.send("not in one")

@client.command(pass_context=True)
async def play(ctx, url: str):

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file,but it is being played")
        await ctx.send("Error: Music playing")
        return
    
    await ctx.send("Getting everything ready now")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/best',
        'postprocessors':[{
            'key':'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }
    try:    
       with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print("Downloading audio now\n")
            ydl.download([url])
    except:
        print("Fallback: youtube-dl does not support this url ,using spotify")
        c_path = os.path.dirname(os.path.realpath(__file__))
        system("spotdl -f " + '"' + c_path + '"' + " -s " + url)
    
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")
    
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("played"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.9

    nname = name.rsplit("-", 2)#error
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@client.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Paused")
        voice.pause()
        await ctx.send("Music paused")
    else:
        print("Music not playing failed pause")
        await ctx.send("Music not playing failed pause ")

@client.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not pause")
        await ctx.send("Music is not pause ")

@client.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music Stopped")
        voice.stop()
        await ctx.send("Music Stopped")
    else:
        print("No Music playing failed to Stop")
        await ctx.send("No Music playing failed to Stop")




client.run("Mine id")
