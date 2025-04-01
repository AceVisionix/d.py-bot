import animec
import discord
from discord.ext import commands
import os
from discord.client import Client
from discord.embeds import Embed
from discord.ext import commands
import json
import random
import datetime
from datetime import datetime
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
from cogs.eco import *

with open("./EDB/typing.txt", "r")as file:
    sentences = [i.replace('\n', ' ') or i for i in file.readlines()]

class eco2(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(aliases = ["scout", "Search", "Scout"], invoke_without_command = True)
    async def search(self, ctx):
        embed = discord.Embed(title = "Scouting Locations!", description = "**Aspect's Jewelry store** - Payout = **100,000** to **200,000**\n **Vision's House** - Payouts - **1,000 - 50,000**\n **Vision's Car** - Payouts -  **5,000** - **10,000**\n **Police Station** - Payouts - **30,000 - 50,000**\n **Vision's Brother's House** - Payouts - **50,000**\n  **Aspect's Storage Area** - Payouts - **50,000** - **100,000**", color = discord.Color.gold())
        await ctx.send(embed = embed)
    
    @search.group(aliases = ["jewelry"])
    @commands.cooldown(1,500, commands.BucketType.user)
    async def jewelrystore(self, ctx):
        await open_account(ctx.author)
        r = random.randrange(10)
        e = [int(100000), int(150000), int(200000)]
        if r == 1:
            earnings = random.choice(e)
            embed = discord.Embed(description = f"You Robbed the **Jewelry Store** and Got **{earnings}**", color = discord.Color.gold())
            await update_bank(ctx.author,1*int(earnings),'wallet')
            await ctx.send(embed = embed)
        elif r == 5:
            embed = discord.Embed(title = "Oh No!", description = "You got **Caught Robbing the Store** and were Fined **50,000**", color = discord.Color.red())
            await update_bank(ctx.author,-50000,'wallet')
            await ctx.send(embed = embed)
        else:
            embed = discord.Embed(title = "Oh No!", description = "You got **Caught Robbing the Store** but Managed to Get Away!", color = discord.Color.red())
            await ctx.send(embed = embed)

    @jewelrystore.error
    async def jewelrystore_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f":x: Command \"`Search`\" is on cooldown, you can us it in **{round(error.retry_after, 1)} seconds.** You know patience is the key also i hope you get fined Lol")




    @commands.group(invoke_without_command = True)
    @commands.cooldown(1,3600,commands.BucketType.user)
    async def work(self, ctx):
        r = random.randrange(2)
        await open_account(ctx.author)
        with open("./databases/work.json", "r")as f:
            users = json.load(f)
        if str(ctx.author.id) not in users:
            await ctx.send("You Currently dont Have a **Job** Please run `-worklist` to view Available Jobs and `-work <job name>` to **Work!**")
        job = users[str(ctx.author.id)]["job"]


        if job == "mathematician":
            if r == 1:
                emb = discord.Embed(title = "Working Time!", description = f"69 x 420 + 420 x 69", color = discord.Color.random())
                await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 30.0)
                except asyncio.TimeoutError:
                    await update_bank(ctx.author,1000, 'wallet')
                    em = discord.Embed(title = f"Work Failed!", description = "You **Failed to Answer** The **Boss's Question** In **Time!** I'm Giving you <:aspcoin:897779264043237438> `1,000` For this Hour of **work!**", color = discord.Color.red())
                    await ctx.send(embed = em)
                if msg == "57960":
                    embed = discord.Embed(title = "Good Job!", description = "**Good Job!!** You Answered **Correctly!** I'm Giving you <:aspcoin:897779264043237438> `5,000` For this Hour of **Work!**", color = discord.Color.green())
                    await ctx.send(embed = embed)
                else:
                    embedd = discord.Embed(title = "Wrong!", description = "You Answered **Wrong** Answer Correctly or :knife: :drop_of_blood: I'll give you <:aspcoin:897779264043237438> `2,000` for at least **Answering**", color = discord.Color.red())
                    await ctx.send(embed = embedd)


            if r == 2:
                emb = discord.Embed(title = "Working Time!", description = f"1000 + 8312 x 347 x 212134", color = discord.Color.random())
                await ctx.send(embed = emb)
                try:
                    msg = await self.client.wait_for('message', timeout = 30.0)
                except asyncio.TimeoutError:
                    await update_bank(ctx.author,1000, 'wallet')
                    em = discord.Embed(title = f"Work Failed!", description = "You **Failed to Answer** The **Boss's Question** In **Time!** I'm Giving you <:aspcoin:897779264043237438> `1,000` For this Hour of **work!**", color = discord.Color.red())
                    await ctx.send(embed = em)
                if msg == "611850460376":
                    await update_bank(ctx.author,5000, 'wallet')
                    embed = discord.Embed(title = "Good Job!", description = "**Good Job!!** You Answered **Correctly!** I'm Giving you <:aspcoin:897779264043237438> `5,000` For this Hour of **Work!**", color = discord.Color.green())
                    await ctx.send(embed = embed)
                else:
                    await update_bank(ctx.author,2500, 'wallet')
                    embedd = discord.Embed(title = "Wrong!", description = "You Answered **Wrong** Answer Correctly or :knifle: :blood_drop: I'll give you <:aspcoin:897779264043237438> `2,000` for at least **Answering**", color = discord.Color.red())
                    await ctx.send(embed = embedd)

        if job == "typer":
            sentence = random.choice(sentences)
            lenght = len(sentence.split())
            formatd = re.sub(r'[^A-Za-z ]+', "", sentence).lower()
            emoji = ""
            for i in formatd:
                if i == " ":
                    emoji+="   "
                else:
                    emoji+= f":regional_indicator_{i}:"
            embed = discord.Embed(title = "Job Time!", description = "I Will Send a **random sentence in Emoji's** You have to Type it In **100 Seconds!** Be Quick! and You get money based on that!", color = discord.Color.random())
            await ctx.send(embed = embed)
            send = await ctx.send(f"{emoji}")
            try:
                msg = await self.client.wait_for('message', timeout = 100.0, check = lambda message: message.author == ctx.author)
            except asyncio.TimeoutError:
                await update_bank(ctx.author, 5000, 'wallet')
                embed = discord.Embed(title = "Failed Job!", description = "You \"**Failed**\" To Answer In **Time**, I'm Only Giving You <:aspcoin:897779264043237438> `5,000` For this **Hour** of **Work!**", color = discord.Color.red())
                await ctx.send(embed = embed)
            else:
                if msg.content.lower()==sentence.lower():
                    time = str(datetime.utcnow() - send.created_at)
                    time_format = time[:-5][5:]
                    if time_format[0] == '0':
                        time_format = time_format[1:]

                    embed = discord.Embed(title = "Good Job!", description = f"{ctx.author.mention} You Completed The **Typing** in **{time_format}** Seconds!.", color = discord.Color.random())
                    wpm = int(lenght/(float(time_format)/60))
                    money = (wpm/100)*10000
                    embed.add_field(name = "Money Earned <:7167peepocash:895966571028185089>", value = money)
                    embed.add_field(name = "WPM <:sip:895962626369146891>", value = wpm)
                    await update_bank(ctx.author, money, 'wallet')
                    await ctx.send(embed = embed)
                else:
                    await update_bank(ctx.author, 2500, 'wallet')
                    embed = discord.Embed(title = "Job Failed!", description = "You **Failed** to Answer **Correctly**, I'm Giving you <:aspcoin:897779264043237438> `2,500` for this **Hour** of **Work!**", color = discord.Color.red())
                    await ctx.send(embed = embed)


    @work.error
    async def work_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send('You Worked too much today Try Again After **{:.2f} Minutes**'.format((error.retry_after)/60))

    @work.group()
    async def mathematician(self,ctx):
        await open_account(ctx.author)
        with open("./databases/work.json", "r")as f:
            users = json.load(f)
        if str(ctx.author.id) in users:
            await ctx.send("You Already Have a **Job** Quit it to Get a New One!, Type `-work quit` to quit!")
        if ctx.author.id not in users:
            users[str(ctx.author.id)] = {}
            users[str(ctx.author.id)]["job"] = "mathematician"
            with open("./databases/work.json", "w")as f:
                json.dump(users,f,indent = 4)
                await ctx.send(f"You Are now Working as a Mathematician {ctx.author.mention}")

    @work.group()
    async def typer(self,ctx):
        await open_account(ctx.author)
        with open("./databases/work.json", "r")as f:
            users = json.load(f)
        if str(ctx.author.id) in users:
            await ctx.send("You Already Have a **Job** Quit it to Get a New One!, Type `-work quit` to quit!")
        if str(ctx.author.id) not in users:
            users[str(ctx.author.id)] = {}
            users[str(ctx.author.id)]["job"] = "typer"
            with open("./databases/work.json", "w")as f:
                json.dump(users,f,indent = 4)
                await ctx.send(f"You Are now Working as a Typer {ctx.author.mention}")

    @work.group()
    async def quit(self, ctx):
        member = ctx.author
        with open('./databases/work.json', 'r') as file:
            data = json.load(file)
            data.pop(str(member.id))
        with open('./databases/work.json', 'w') as notes_update:
            json.dump(data, notes_update, indent=4)
        await ctx.send(':white_check_mark: **You Quit You Job!**')


    @commands.command(aliases = ["work-list"])
    async def worklist(self, ctx):
        await open_account(ctx.author)
        embed = discord.Embed(title = "Work For What?", description = "**Job Name** ┃ **Salary** ┃ **Work Hour's** ┃ **Availablity**\n\n **Mathamatician:** ┃ `5,000` ┃ `1` ┃ <a:verify:896345909300973569>\n**Typer:** ┃ `10,000` ┃ `2` ┃ <a:verify:896345909300973569>\n**Gamer:** ┃ `15,000` ┃ `3` ┃ <:wrong:898165331158253579>\n**Bank Manager:** ┃ `Bank Notes` ┃ `4` ┃ <:wrong:898165331158253579>\n**Joker:** ┃ `16,000` ┃ `5` ┃ <:wrong:898165331158253579>\n**Pogster:** ┃ `20,000` ┃ `6` ┃ <:wrong:898165331158253579>", color = discord.Color.random())
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(eco2(client))