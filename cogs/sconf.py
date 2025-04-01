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

class scf(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command = True)
    async def role(self, ctx):
        embed = discord.Embed(title = "Role Commands!", description = "**Create Role** - Creates a Role With the Name you Want!\n`-role create <name of role>`\n\n**Delete Role** - Deletes A Role You Want to delete\n`-role delete <@role>`\n\n**Edit Role** - Edits a Role's Name\n`-role edit <@role> <new name>`", color = discord.Color.random())
        await ctx.send(embed = embed)

    @role.group(aliases=['make_role'])
    @commands.has_permissions(manage_roles=True)
    async def create(self, ctx, *, name, color = None):
        guild = ctx.guild
        await guild.create_role(name=name, color=color)
        embed = discord.Embed(title = "<a:verified:914545848648597524> Role Created!", description = f"**Created By:** {ctx.author}\n**Role Name:** {name}")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Role Created By {ctx.author}")
        await ctx.send(embed = embed)

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **You Don't have the Required Permission to Run Create Role Command! Trying to raid? hmmm sus** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please Make Sure to add The Roles Name!**")

    @role.group()
    async def delete(self, ctx, role_name: discord.Role):
        if role_name == "@everyone":
            await ctx.send("srsly?")
        await role_name.delete()
        embed = discord.Embed(title = "<a:verified:914545848648597524> Role Deleted!", description = f"**Deleted By:** {ctx.author}\n**Role Name:** {role_name}")
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Role Deleted By {ctx.author}")
        await ctx.send(embed = embed)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **You Don't have the Required Permission to Run Delete Role Command! Trying to raid? hmmm sus** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please Make Sure to add The Roles Name!**")

    @commands.command(aliases = ["sm"])
    async def slowmode(self, ctx, timeInput):
        try:
            try:
                time = int(timeInput)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            if time > 86400:
                await ctx.send("**:x: I can\'t add a slowmode over a 6 hours long noob :robot:**")
                return
            if time <= 0:
                await ctx.send("**:x: slowmodes don\'t go into negatives :/ noob :robot:**")
                return
            if time >= 3600:
                await ctx.channel.edit(slowmode_delay = time)
                await ctx.send(f"**<a:verified:914545848648597524> Changed Slowmode to {time//3600} hours {time%3600//60} minutes {time%60} seconds <a:verfy:896928527935500299>**")
            elif time >= 60:
                await ctx.channel.edit(slowmode_delay = time)
                await ctx.send(f"**<a:verified:914545848648597524> Changed Slowmode to {time//60} minutes {time%60} seconds <a:verfy:896928527935500299>**")
            elif time < 60:
                await ctx.channel.edit(slowmode_delay = time)
                await ctx.send(f"**<a:verified:914545848648597524> Changed Slowmode to {time} seconds <a:verfy:896928527935500299>**")
        except:
            await ctx.send("**Try Again Properly!** - `-sm <timeinput>` **Reminder: no Slowmode above 6 Hours**")


def setup(client):
    client.add_cog(scf(client))