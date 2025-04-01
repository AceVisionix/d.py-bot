import animec
import discord
from discord import guild
from discord.ext import commands
import os
from discord.client import Client
from discord.embeds import Embed
from discord.ext import commands
import json
import random
import datetime
from datetime import *
import asyncio
from discord.ext.commands.errors import MissingRequiredArgument
from discord_components import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import re
import requests
import aiohttp
from animec import *

def convert(time):
    pos = ["s","m","h","d"]

    time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

class gaw(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def giveaway(self, ctx):
        await ctx.send("Let's start with this giveaway! 🎉 **Answer** these questions within **30** seconds!🧧")

        questions = [f"Which **channel** should it be hosted in?\n Example: {ctx.channel.mention}", "What should be the duration of the giveaway? **(s | m | h | d)**\n Example: 1s | 1m | 1h | 1d", "What is the prize of the giveaway?\n Example: 1,000,000 Coins!"]

        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for info in questions:
            await ctx.send(info)
            try:
                msg = await self.client.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You **didn\'t answer in time**, please be **quicker** next time!')
                return
            else:
                answers.append(msg.content)

        try:
            c_id = int(answers[0][2:-1])
        except:
            await ctx.send(f"You didn't mention a channel **Properly**. **Do it like this {ctx.channel.mention} next time.**", "How Many Winners?", "Note:")
            return
        channel = self.client.get_channel(c_id)

        time = convert(answers[1])
        if time == -1:
            await ctx.send(f"You **didn't answer** with a proper unit. Use **(s | m | h | d)** next time!")
            return
        elif time == -2:
            await ctx.send(f"The Time Has to Be An **Integer!**, **Please Enter an Integer Next time!**")
            return
        
        prize = answers[2]

        await ctx.send(f"The **Giveaway** will be in {channel.mention} and will last **{answers[1]}!**")
        embed = discord.Embed(title = f"{prize}", description = f"React with 🎉 to enter!\n Winners: 1\n Hosted By: {ctx.author.mention}", color = discord.Color.random())
        embed.set_footer(icon_url = ctx.author.avatar_url ,text = f"Ends {answers[1]} From now!")
        mmsg = await channel.send("🎉 New Giveaway 🎉",embed = embed)
        await mmsg.add_reaction("🎉")
        await asyncio.sleep(time)

        nm = await channel.fetch_message(mmsg.id)
        users = await nm.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))
        winner = random.choice(users)

        await channel.send(f"🎉 Congratulations! **{winner.mention}** Won the prize: **{prize}!** 🎉")


    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def reroll(self, ctx, channel : discord.TextChannel, id_ : int):
        try:
            m = await channel.fetch_message(id_)
        except:
            await ctx.send(":x: The ID that you (or u told someone to get it for u) entered was incorrect like bruh?, **make sure you have entered the correct giveaway message ID next time you noob**.")
        users = await m.reactions[0].users().flatten()
        users.pop(users.index(self.client.user))

        winner = random.choice(users)

        await channel.send(f"🎉 **Congratulations** the new winner is: {winner.mention} for the **giveaway reroll**! 🎉")

def setup(client):
    client.add_cog(gaw(client))