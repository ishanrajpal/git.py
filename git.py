import discord
from discord.ext import commands

client = discord.Client()

@client.event
async def on_member_join(member):
    for channel in member.guild.channels:
        if str(channel) == "general":
            await channel.send_message(f"""Welcome to the server {member.mention}""")

@client.event
async def on_message(message):
    id = client.get_guild(your server id)
    if message.content.find("!hello") != -1:
        await message.channel.send("Hi")
    elif message.content == "!users":
         await message.channel.send(f"""Total Members in this Server is: {id.member_count}""")
    play = ['khala','aaja']
    for word in play:
        if message.content.count(word) > 0:
            await message.channel.send("if you want to play you can call me")
    if message.content =="phone":
         await message.channel.send("if you don't have my Phone no Then don't Bother ")    
    if message.content == "help":
        embed= discord.Embed(title="What can killer Frost do?",description="Some useful commands")
        embed.add_field(name="!hello",value="Greets the user")
        embed.add_field(name="!users",value="Prints no of users")
        embed.add_field(name="khala",value="message")
        await message.channel.send(content=None, embed=embed)
    

client.run("your id")
