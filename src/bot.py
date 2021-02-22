# ParsaIzadmehr

#----- import -----
from discord.ext import commands
from asyncio import *
from random import randint,choice
import discord
import time
import datetime

class Config:
    TOKEN = "YOUR TOKEN"
    PREFIX = "!"

client = commands.Bot(command_prefix=Config.PREFIX)

# remove default halp commnad.  
# client.remove_command("help")
# in next update use custom help command

#==================================== Event ====================================
@client.event
async def on_ready():
    # await client.change_presence(activity=discord.Game("!help"))
    print("Bot is ready!")

# see member's delete self messages
@client.event
async def on_message_delete(message):
    embed=discord.Embed(title="{} deleted a message".format(message.author), description="", color=discord.Color.blue())
    embed.add_field(name= message.content ,value="This is the message that he has deleted", inline=True)
    channel=client.get_channel("YOUR CHANNEL ID")
    await channel.send(channel, embed=embed)

#======================================= COMMANDS ===========================================

# ----- send dm message to user -----
@client.command(help="!send_dm @user")
@commands.has_role("Outis moderator")
async def send_dm(ctx, member: discord.Member, *, content):
    channel = await member.create_dm()
    await channel.send(content)
    

# ----- Clear -----
@commands.has_permissions(administrator=True)
@client.command(help="!clear <number>")
async def clear(ctx, count="50"):
    count = int(count)
    await ctx.channel.purge(limit=count+1)
    await ctx.channel.send(embed=discord.Embed(description=f"{str(count)}  Messages deleted. "))
    time.sleep(1)
    await ctx.channel.purge(limit=1)

#------ Create new category and channels ------
@commands.has_permissions(administrator=True)
@client.command(help="!new <tchannel, category, vchannel> <Name of channel>")
async def new(ctx, arg1, *, arg2):
    mention = ctx.author.mention
    guild = ctx.message.guild
    if arg1 == "tchannel":
        await guild.create_text_channel(arg2)
        await ctx.channel.send(embed=discord.Embed(description=f"Text channel created by {mention}.", color=discord.Color.black()))

    elif arg1 == "category":
        await guild.create_category(arg2)
        await ctx.channel.send(embed=discord.Embed(description=f"Category created by {mention}.", color=discord.Color.black()))
    
    elif arg1 == "vchannel":
        await guild.create_voice_channel(arg2)
        await ctx.channel.send(embed=discord.Embed(description=f"Voice channel created by {mention}.", color=discord.Color.black()))

#----- Send Custom message in any channel -----
#send embed message
@commands.has_permissions(administrator=True)
@client.command(help="!sende <channel id> <message>")
async def sende(ctx, channelid, *, message):
    mention = ctx.channel.mention
    await client.wait_until_ready()
    channel = client.get_channel(int(channelid))
    await channel.send(embed=discord.Embed(description=message, color=discord.Color.black()))

#send normal message
@commands.has_permissions(administrator=True)
@client.command(help="!sendm <channel id> <message>")
async def sendm(ctx, channelid, *, message):
    mention = ctx.channel.mention
    await client.wait_until_ready()
    channel = client.get_channel(int(channelid))
    await channel.send(message)

#------ activity ------
@commands.has_permissions(administrator=True)
@client.command(help="!set <activity_type> <activity_text>")
async def set(ctx, activity_type, *,activity_text):
    mention = ctx.author.mention
    if (activity_type == "playing"):
        await client.change_presence(activity=discord.Game(name=activity_text))
        await ctx.send("Status changed by "+mention)

    elif (activity_type=="streaming"):
        await client.change_presence(activity=discord.Streaming(name=activity_text, url=""))
        await ctx.send("Status changed by "+mention)

    elif (activity_type == "watching"):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity_text))
        await ctx.send("Status changed by "+mention)

    elif (activity_type =="listening"):
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity_text))
        await ctx.send("Status changed by "+mention)

    else:
        await ctx.send("is updating....")

#----- Lock channel -----
@commands.has_permissions(administrator=True)
@client.command(help="!lock ")
async def lock(ctx, channel : discord.TextChannel=None):
    mention = ctx.author.mention
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send("Channel locked by "+mention)

# ----- unlock -----
@commands.has_guild_permissions(administrator=True)
@client.command(help="!unlock")
async def unlock(ctx, channel : discord.TextChannel=None):
    mention = ctx.author.mention
    overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True
    await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send(f"Channel unlocked by "+mention)

#----- kick command -----
@client.command(help="!kick @user")
@commands.has_permissions(manage_messages = True)
async def kick(ctx, member : discord.Member, *, reason = None ):
    await member.kick(reason = reason)
    await ctx.send(embed=discord.Embed(description=f"{member.mention}  {reason}", color=discord.Color.red()))

#----- ban command -----
@client.command(help="!ban @user")
@commands.has_permissions(manage_messages = True)
async def ban(ctx, member : discord.Member, *, reason = None ):
    await member.ban(reason = reason)
    await ctx.send(embed=discord.Embed(description=f"{member.mention}  {reason}", color=discord.Color.red()))

# ----- taas -----
@client.command(help="!taas")
async def taas(ctx):
    #a simple game
    x = randint(1, 6)
    await ctx.send(f"Your number is: {x}" )

# ----- date -----
@client.command(help="!date")
async def date(ctx):
    message = str(datetime.datetime.now().strftime("%Y - %m - %d"))
    await ctx.send(embed=discord.Embed(description=message, color=discord.Color.orange()))

@client.command()
async def about(ctx):
    about = '''
    Hi, I'm Parsa🙋‍♂️
    🤖 Outis bot's father
    💻mathematics student
    👨‍💻Python,Ruby Developer

    About updates in the future
    update:
          - Warn system
          - Give away
          - Welcome
          - Play music
    '''
    m1 = discord.Embed(
        title = "About programmer of this project",
        description = about,
        color = discord.Color.green(),
    )
    await ctx.send(embed = m1)

#======================= HANDLING ERROR =======================
# ----Error handling command ----
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        mention = ctx.author.mention
        await ctx.send(embed=discord.Embed(description=f"{mention} command not found", color=discord.Color.red()))

client.run(Config.TOKEN)