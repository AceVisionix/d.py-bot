from asyncio.tasks import wait_for
import discord
import os
from discord import guild
from discord.ext import commands
import json
import random
import datetime
from datetime import datetime, timedelta
import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import re
import requests
import keep_alive
print("imported modules")

def get_prefix(client,message):
    with open("./CDB/prefixes.json", "r") as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, intents = discord.Intents.all())

@client.event
async def on_guild_join(guild):
    with open("./CDB/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "."
    with open("./CDB/prefixes.json", "w") as f:
        json.dump(prefixes,f)

@client.command()
@commands.has_permissions(administrator = True)
async def prefix(ctx, prefix):
    with open("./CDB/prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open("./CDB/prefixes.json", "w") as f:
        json.dump(prefixes,f)
    embed = discord.Embed(title = "Prefix Change!", description = f"My Prefix was changed to {prefix}")
    embed.set_footer(icon_url= ctx.guild.icon_url, text=ctx.guild.name)
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed = embed)

@client.event
async def on_message(msg):
    try:
        if msg.mentions[0] == client.user:
            with open("./CDB/prefixes.json", "r") as f:
                prefixes = json.load(f)
            pre = prefixes[str(msg.guild.id)] 
        embed = discord.Embed(title = "Prefix", description = f"My Prefix for this server is {pre}")
        embed.timestamp = datetime.utcnow()
        await msg.channel.send(embed = embed)
    except:
        pass
    await client.process_commands(msg)

@client.remove_command('help')

@client.event
async def on_ready():
    print("Ready")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name= "To .Help"))
    print("Changed Prensence")
    print(client.user.id)
    print("-------------------------------")

@client.command()
async def load(ctx):
    vision_id = 880846666624811088
    if ctx.author.id == vision_id:
        client.load_extension(f'cogs/mod.py')
        await ctx.send(f"Loaded Successfully")
    else:
        return

@client.command()   
async def unload(ctx, extension):
    vision_id = 880846666624811088
    if ctx.author.id == vision_id:
        client.unload_extension(f'cogs.{extension}')    
        await ctx.send(f"Unloaded {extension} Successfully")
    else:
        return

@client.command()
async def reload(ctx, extension):
    vision_id = 880846666624811088
    if ctx.author.id == vision_id:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await ctx.send(f"Reloaded {extension} Successfully")
    else:
        return

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.command()
async def lockguess(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title = "Guess!!", description = "Guess The Lock's Code...... NOW! Its any number from 1000 to 9999", color = discord.Color.random())
    await ctx.send(embed = embed)
    r = [2121, 2383, 3112]
    pog = random.choice(r)
    response = await client.wait_for(f'message')
    if ctx.author.id is not response.author.id:
        return
    if ctx.author.id == response.author.id:
        if pog is response:
            await ctx.send("YOU GUESSED IT!")
    if ctx.author.id == response.author.id:
        if pog is not response:
            await ctx.send("Wrong try again by doing `.guesss`")

@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def say(ctx, *,message):
    embed = discord.Embed(title = "New Message Request", description = f"{message}", color = discord.Color.random())
    await ctx.send(embed = embed)

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Command "Say" is on cooldown, you can us it in {round(error.retry_after, 2)} seconds.')

@client.command()
@commands.has_permissions(administrator = True)
async def activity(ctx, *, activity):
    vision_id = 880846666624811088
    falcon_id = 881095807565172776
    if ctx.author.id == vision_id : 
        await client.change_presence(activity=discord.Game(name=activity))
        await ctx.send(f"Bot's activity changed to {activity}")
    elif ctx.author.id == falcon_id :
        await client.change_presence(activity=discord.Game(name=activity))
        await ctx.send(f"Bot's activity changed to {activity}")
    else:
        return await ctx.send("Only Founders Can use This Command lol")

keep_alive.keep_alive()
client.run("OTA5MDg3OTg3MTM5MjE5NDU2.GunX7X.dogQ2XHpEQDekzr6aInkV_pqqhhZEClk3YQW88")