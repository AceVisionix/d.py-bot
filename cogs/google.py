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
import googletrans

class test(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['tr'])
    async def translate(self, ctx, lang_to, *args):
        lang_to = lang_to.lower()
        if lang_to not in googletrans.LANGUAGES and lang_to not in googletrans.LANGCODES:
            raise commands.BadArgument(":x: Invalid language to translate text to")

        text = ' '.join(args)
        translator = googletrans.Translator()
        text_translated = translator.translate(text, dest=lang_to).text
        await ctx.send(text_translated)

def setup(client):
    client.add_cog(test(client))