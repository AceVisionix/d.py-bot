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

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title = "Alvora Help Page!", description = "**Need more Help?** Join our **[Support / Community Server](https://discord.gg/2VGJbkMsqQ)**\n**Enjoying The Bot?** Vote for Us **[Here](https://discordbotlist.com/bots/)** and **[Here](https://top.gg/bot/)**", color = discord.Color.gold())
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(test(client))