from typing import Text
import discord
from discord.ext import commands
import os
import json
import random
import datetime
from datetime import datetime
import asyncio
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import re
import requests
from io import BytesIO
from PIL import Image, ImageChops, ImageDraw, ImageFont
print("imported utility")

messagecounts = {}

def circle(pfp,size = (215,215)):
    
    pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
    
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask) 
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.ANTIALIAS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

def __init__(self, client):
        self.client = client

class embed(commands.Cog):

    @commands.command(aliases=['ar','giverole','gr'])
    @commands.has_permissions(manage_roles = True)
    async def addrole(self, ctx, member:discord.Member, role: discord.Role or discord.Role.id):
        if ctx.author.top_role < role:
            return await ctx.send(":robot: role Mentioned Is Above Your Role So you cannot add it because of role hierarchy :x:")
        await member.add_roles(role)
        embed = discord.Embed(title = f"Role Successfully Added!! <a:verified:914545848648597524>", description = f"<a:r_arrow:889034352225308693> **Role Name -** {role.mention}\n <a:r_arrow:889034352225308693> **User -** {member}", color = discord.Color.green())
        embed.set_footer(icon_url = ctx.guild.icon_url, text = f"Role Added by {ctx.author}!")
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed = embed)

    @addrole.error
    async def addrole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
        	await ctx.send(":no_entry_sign: **Yo Bro get some permisions first you need `Manage Roles` for this command** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":no_entry_sign: **Mention The command user and role! `-addrole [@user] [@role]`** :robot:")
        if isinstance(error, commands.MemberNotFound):
        	await ctx.send(":no_entry_sign: **Noob, im not blind that person isn't in the server or doesnt even exsist** :eyes:")

    @commands.command(aliases=['takerole'])
    @commands.has_permissions(manage_roles = True)
    async def removerole(self, ctx, member: discord.Member, role: discord.Role):
        if ctx.author.top_role < role:
            return await ctx.send("nab")
        await member.remove_roles(role)
        embed = discord.Embed(title = f"Role Successfully Removed!! <a:verified:914545848648597524>", description = f"<a:r_arrow:889034352225308693> **Role Name -** {role.mention}\n <a:r_arrow:889034352225308693> **User -** {member}", color = discord.Color.green())
        embed.set_footer(icon_url = ctx.guild.icon_url, text = f"Role Removed by {ctx.author}!")
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @removerole.error
    async def removerole_error(self, ctx, error):
	    if isinstance(error, commands.MissingPermissions):
		    await ctx.send(":no_entry_sign: **Yo Bro get some permisions first you need `Manage Roles` for this command** :robot:")
	    elif isinstance(error, commands.MissingRequiredArgument):
		    await ctx.send(":no_entry_sign: **Mention The command user and role! `-rr [@user] [@role]`** :robot:")
	    if isinstance(error, commands.MemberNotFound):
		    await ctx.send(":no_entry_sign: **Noob, im not blind that person isn't in the server or doesnt even exsist** :eyes:")

    @commands.command()
    @commands.has_permissions(manage_nicknames = True)
    async def nick(self, ctx, member: discord.Member,*, nick):
        await member.edit (nick = nick)
        embed = discord.Embed(title = "<a:verified:914545848648597524> Nickname Changed!", description = f"Changed {member}'s Nickname\n **New Nickname** = *{nick}*", color = discord.Color.random())
        await ctx.send(embed = embed)

    @commands.command()
    async def userinfo(self, ctx, member:discord.Member = None):
        if member == None:
            member = ctx.author
        with open("./EDB/balance.json", "r") as f:
            data = json.load(f)
        if str(member.id) not in data:
            data[str(member.id)] = {}
            data[str(member.id)]["wallet"] = 10000
            data[str(member.id)]["Gems"] = 0
            data[str(member.id)]["bank"] = 0
            data[str(member.id)]["bank_space"] = 25000
            with open("./CDB/balance.json", "w") as f:
                json.dump(data,f, indent = 4)
        with open("./EDB/balance.json", "r") as f:
            data = json.load(f)
        wallet = data[str(member.id)]["wallet"]
        bank = data[str(member.id)]["bank"]
        bank_space = data[str(member.id)]["bank_space"]
        gems = data[str(member.id)]["Gems"]
        net_worth = bank + wallet + gems
        embed = discord.Embed(title="USER INFO", description=f"Here is the info we retrieved about {member}", colour=discord.Color.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Name", value=f":arrow_right: {member.name}", inline=True)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Nickname", value=f":arrow_right: {member.nick}", inline=True)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: ID", value=f"{member.id}", inline=True)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Status", value=f":arrow_right: {member.status}", inline=True)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Top Role", value=f":large_blue_diamond: {member.top_role.name}", inline=True)
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Created At", value = f":gear: {str(member.created_at)[0:11]}")
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Joined At", value = f":sparkler: {str(member.joined_at)[0:11]}")
        embed.add_field(name=":diamond_shape_with_a_dot_inside: Economy Money", value=f"<:ascoinstack:888722390480220181> **Wallet -** {wallet}\n :bank: **Bank Money -** {bank}\n :arrow_right: **Bank Space -** {bank_space}\n:gem: **Gems -** {gems}\n<:Moneybag:889741330945835008> **Net Worth -** {net_worth}")
        await ctx.send(embed=embed)

    @commands.command()
    async def suggest(self, ctx, *, question = None):
        if question == None:
            await ctx.send(":x: Please Incude what you want to suggest.")
        SuggestEmbed = discord.Embed(title = "New Suggestion Has Come up!", description = f"{question}", color = discord.Color.blue())

        SuggestEmbed.set_footer(text = f"Suggestion By {ctx.author}")

        await ctx.message.delete()
        suggest_msg = await ctx.send(embed = SuggestEmbed)

        await suggest_msg.add_reaction("⬆")
        await suggest_msg.add_reaction("⬇")

    @commands.command()
    async def report(self, ctx, *, question = None):
        if question == None:
            await ctx.send(":x: Please Incude who you want to report.")
        SuggestEmbed = discord.Embed(title = "New report Has Come up!", description = f"{question}", color = discord.Color.blue())

        SuggestEmbed.set_footer(text = f"Report By {ctx.author}")

        await ctx.message.delete()
        suggest_msg = await ctx.send(embed = SuggestEmbed)


    @commands.command()
    async def embed(self, ctx, *, arg):
        try:
            message, question = arg.split("||")
            SuggestEmbed = discord.Embed(title = f"{message}", description = f"{question}", color = discord.Color.blue())
            SuggestEmbed.set_footer(text = f"Embed By {ctx.author}")
        except:
            SuggestEmbed = discord.Embed(title = f"{arg}")
            SuggestEmbed.set_footer(text = f"Embed By {ctx.author}")

        await ctx.message.delete()
        suggest_msg = await ctx.send(embed = SuggestEmbed)

    @embed.error
    async def embed_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(":x: Please Include Title and desctiption :x:")

    @commands.command()
    async def storenotes(self, ctx, *,question = None):
        member = ctx.author
        with open("./CDB/notes.json", "r") as f:
            data = json.load(f)
        if str(member.id) not in data:
            data[str(member.id)] = {}
            data[str(member.id)]["Notes"] = question
            with open("./CDB/notes.json", "w")as f:
                json.dump(data, f, indent = 4)
                await ctx.send("Successfully Added your Notes to view them Run `-mynotes`")
        elif str(member.id) in data:
            return await ctx.send("You already stored notes run `-removenotes` to store new notes")

    @commands.command()
    async def mynotes(self, ctx):
        member = ctx.author
        with open("./CDB/notes.json", "r") as f:
            data = json.load(f)
        notes = data[str(member.id)]["Notes"]
        embed = discord.Embed(title = "Your Notes!", description = f"{notes}", color = discord.Color.random())
        await ctx.send(embed = embed)

    @commands.command()
    async def removenotes(self, ctx):
        member = ctx.author
        with open('./CDB/notes.json', 'r') as file:
            data = json.load(file)
            data.pop(str(member.id))
        with open('./CDB/notes.json', 'w') as notes_update:
            json.dump(data, notes_update, indent=4)

        await ctx.send(':white_check_mark: **Removed from Notes**')

    @commands.command()
    async def timer(self, ctx, timeInput):
        try:
            try:
                time = int(timeInput)
            except:
                convertTimeList = {'s':1, 'm':60, 'h':3600, 'd':86400, 'S':1, 'M':60, 'H':3600, 'D':86400}
                time = int(timeInput[:-1]) * convertTimeList[timeInput[-1]]
            if time > 86400:
                await ctx.send("**:x: I can\'t do timers over a day long noob :robot:**")
                return
            if time <= 0:
                await ctx.send("**:x: Timers don\'t go into negatives :/ noob :robot:**")
                return
            if time >= 3600:
                message = await ctx.send(f"Timer: {time//3600} hours {time%3600//60} minutes {time%60} seconds")
            elif time >= 60:
                message = await ctx.send(f"Timer: {time//60} minutes {time%60} seconds")
            elif time < 60:
                message = await ctx.send(f"Timer: {time} seconds")
            while True:
                try:
                    await asyncio.sleep(5)
                    time -= 5
                    if time >= 3600:
                        await message.edit(content=f"Timer: {time//3600} hours {time %3600//60} minutes {time%60} seconds")
                    elif time >= 60:
                        await message.edit(content=f"Timer: {time//60} minutes {time%60} seconds")
                    elif time < 60:
                        await message.edit(content=f"Timer: {time} seconds")
                    if time <= 0:
                        await message.edit(content="Ended!")
                        await ctx.send(f"**<a:verified:914545848648597524> {ctx.author.mention} Your countdown Has ended!**")
                        break
                except:
                    break
        except:
            await ctx.send(f"Alright, first you gotta let me know how I\'m gonna time Nooby kid **{timeInput}**....")

    @commands.command()
    async def stats(self, ctx):
        embed=discord.Embed(title=f"{ctx.guild.name}'s Server Stats!", color = discord.Color.blue())
        embed.add_field(name="Users:", value=ctx.guild.member_count, inline=False)
        embed.add_field(name="Channels:", value=len(ctx.guild.channels), inline=False)
        embed.add_field(name="Messages Sent Since Bot Added:", value=messagecounts[ctx.guild.id], inline=False)
        embed.set_footer(icon_url = ctx.guild.icon_url, text= ctx.guild.name)
        embed.timestamp = datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id not in messagecounts.keys():
            messagecounts[message.guild.id] = 0
        messagecounts[message.guild.id] += 1
    
    @commands.command()
    async def serverinfo(self, ctx):
        with open("./CDB/dscp.json", "r") as f:
            data = json.load(f)
        if str(ctx.guild.id) not in data:
            await ctx.send("No Description Set, Run `-configdscp <descripton>` to set one! then try again!")
            return
        dsp = data[str(ctx.guild.id)]["Notes"]
        role_count = len(ctx.guild.roles)
        embed = discord.Embed(title = f"{ctx.guild.name}'s Info!", description = f":arrow_right: **Description:** {dsp}", color = discord.Color.gold())
        embed.add_field(name = ":white_small_square: **Owner**", value = f":crown: {ctx.guild.owner}", inline = True)
        embed.add_field(name = ":white_small_square: **Boosts**", value = f"<a:boost:914414974858821663> **Total Boosts:** {ctx.guild.premium_subscription_count}", inline = True)
        embed.add_field(name = ":white_small_square: **Verification Level**", value = f":lock: {str(ctx.guild.verification_level)}")
        embed.add_field(name = ":white_small_square: **Members**", value=f"**Total Members:** {ctx.guild.member_count}")
        embed.add_field(name = ":white_small_square: **Roles**", value = f":arrow_up: **Top Role:** {ctx.guild.roles[-2]}\n:page_facing_up: **Total Roles:** {str(role_count)}")
        embed.add_field(name = ":white_small_square: **Channels**", value=f":hash: **Text Channels:** {len(ctx.guild.text_channels)} \n:loud_sound: **Voice Channels:** {len(ctx.guild.voice_channels)}\n:gem: **Total:** {len(ctx.guild.channels)}")
        embed.add_field(name = ":white_small_square: **Messages Sent**", value = f":speech_balloon: **Since Added:** {messagecounts[ctx.guild.id]}")
        embed.add_field(name = ":white_small_square: **Created At**", value = f"**Created:** {(ctx.guild.created_at)}")
        embed.add_field(name = ":white_small_square: **Region**", value = f":earth_asia: **Region:** {(ctx.guild.region)}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.set_footer(icon_url=ctx.guild.icon_url, text = ctx.guild.name)
        await ctx.send(embed = embed)

    @commands.command()
    async def configdscp(self, ctx,* ,question = None):
        with open("./CDB/dscp.json", "r") as f:
            data = json.load(f)
        if str(ctx.guild.id) not in data:
            data[str(ctx.guild.id)] = {}
            data[str(ctx.guild.id)]["Notes"] = question
            with open("./CDB/dscp.json", "w")as f:
                json.dump(data, f, indent = 4)
                await ctx.send("Successfully Added")

    @commands.command()
    async def purgeuser(self, ctx,user:discord.User, messages = 0):
        if user.bot:
            return await ctx.send("this isnt a bot")
        limit = 2000
        msg = []
        async for m in ctx.channel.history():
            if int(messages) == 0:

                if len(msg) == int(limit):
                    break
                if m.author.id == user.id:
                    msg.append(m)
            else:
                if len(msg) == int(messages):
                    break
                if m.author.id == user.id:
                    msg.append(m)
            
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Deleted {len(msg)} For {user}")

        
    @commands.command()
    async def purgebot(self, ctx,user:discord.User, messages = 0):
        limit = 2000
        msg = []
        async for m in ctx.channel.history():
            if user.bot:
                if int(messages) == 0:

                    if len(msg) == int(limit):
                        break
                    if m.author.id == user.id:
                        msg.append(m)
                else:
                    if len(msg) == int(messages):
                        break
                    if m.author.id == user.id:
                        msg.append(m)
            else:
                await ctx.send("You Are Not A Bot")
                break
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Deleted {len(msg)} For {user}")


def setup(client):
    client.add_cog(embed(client))