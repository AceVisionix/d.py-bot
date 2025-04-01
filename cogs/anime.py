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

panime = []

class Anime(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def anime(self, ctx,*,query):
        try:
            anime = animec.Anime(query)
        except:
            await ctx.send(embed = discord.Embed(description = "No Anime Found for the Search Query!", color = discord.Color.red()))
            return
        embed = discord.Embed(title = anime.title_english, url = anime.url, description = f"{anime.description[:200]}...", color = discord.Color.green())
        embed.add_field(name = "Episodes", value = str(anime.episodes))
        embed.add_field(name = "Rating", value = str(anime.rating))
        embed.add_field(name = "Broadcast", value = str(anime.broadcast))
        embed.add_field(name = "Status", value = str(anime.status))
        embed.add_field(name = "Type", value = str(anime.type))
        embed.add_field(name = "NSFW Status", value = str(anime.is_nsfw()))
        embed.add_field(name = "Ranking", value = str(anime.ranked))
        embed.set_footer(icon_url = ctx.guild.icon_url, text= ctx.guild.name)
        embed.set_thumbnail(url = anime.poster)
        buttons = [[Button(style=ButtonStyle.URL, label="Invite", url = "https://discord.com/api/oauth2/authorize?client_id=888322899281330186&permissions=2147483135&scope=bot%20applications.commands")]]
        buttons2 = [[Button(style=ButtonStyle.URL, label="Invite", disabled = True, url = "https://discord.com/api/oauth2/authorize?client_id=888322899281330186&permissions=2147483135&scope=bot%20applications.commands")]]
        await ctx.send(embed=embed, components = buttons)

    @anime.error
    async def anime_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**type the name of which anime noob** :x:")

    @commands.command(aliases = ["animecharacter"])
    async def animec(self, ctx,*,query):
        try:
            char = animec.Charsearch(query)
        except:
            await ctx.send(embed = discord.Embed(description = "No Anime Character is Found on the Search!", color = discord.Color.red()))
            return

        embed = discord.Embed(title = char.title, url = char.url, color = discord.Color.random())
        embed.set_image(url = char.image_url)
        embed.set_footer(text = ", ".join(list(char.references.keys())[:2]))
        await ctx.send(embed = embed)
        await ctx.send("Some Characters Need Full name to Be Shown Blame the API lol")

    @animec.error
    async def animec_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Type the name of which anime character you lazy noob** :x:")

    @commands.command()
    async def aninews(self, ctx, amount:int=3):
        news = animec.Aninews(amount)
        links = news.links
        titles = news.titles
        descriptions = news.description

        embed = discord.Embed(title = "Latest Anime News!", color = discord.Color.random(), timestamp = datetime.utcnow())
        embed.set_thumbnail(url = news.images[0])

        for i in range(amount):
            embed.add_field(name = f"{i+1}) {titles[i]}", value = f"{descriptions[i][:200]}...\n[Read More]({links[i]})", inline = False)
        await ctx.send(embed = embed)

    @commands.command()
    async def addtodata(self, ctx,name, link):
        vision_id = 880846666624811088
        if ctx.author.id == vision_id:

            global panime
        
            with open("./CDB/anime.json", "r") as f:
                data = json.load(f)
       
            data[str(name)] = {}
            data[str(name)]["animelink"] = str(link)
            panime.append(name)        
            with open("./CDB/anime.json", "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send("data added successfully")
    
    @commands.command()
    async def guess(self, ctx):
        with open("./CDB/anime.json", "r") as f:
            data = json.load(f)
        

        randomanime = random.choice(panime)
        animepic = data[randomanime]["animelink"]
        raniem = discord.Embed(title = "<a:sharingan:911922792671363073> Guess The Anime!, Please do not add any **Caps letter** and instead of a `space` please use `-` <a:sharingan:911922792671363073>")
        raniem.set_image(url = animepic)
        await ctx.send(embed=raniem)
        await ctx.send("<a:pepeclap:911917864359985183> Guess The Anime Starts Now! <a:pepeclap:911917864359985183>")
        while True:
            response = await self.client.wait_for('message')
            guess = str(response.content)
            if ctx.author.id == response.author.id:  
                if guess == str(randomanime):    
                    await ctx.send("<a:verify:911917442996011008> Correct answer")
                    break
            
                if guess != str(randomanime):
                    await ctx.send(":x: Wrong Answer")
                    break

    @commands.command(aliases = ["obito"])
    async def kakashi(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/881743806964314193/882783613408673802/ezgif-2-d82b543466f1.gif")

    @commands.command(aliases = ["Naruto", "9-tails", "9tails", "nine tails"])
    async def naruto(self, ctx):
        await ctx.send("https://media.discordapp.net/attachments/882509916470915100/883190188908642305/ezgif-6-4afd5cd813bd.gif")

    @commands.command()
    async def removefromdata(self, ctx,name):
        vision_id = 880846666624811088
        falcon_id = 881095807565172776
        if ctx.author.id == vision_id or falcon_id:
            with open("./CDB/anime.json", "r") as f:
                data = json.load(f)
            global panime
            del data[name]
            panime = [i for i in panime if i != name] 
            with open("./CDB/anime.json", "w") as f:
                json.dump(data, f, indent=4)
            await ctx.send("<a:verify:911917442996011008> data Removed successfully")
            
def setup(client):
    client.add_cog(Anime(client))