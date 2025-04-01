import os
import discord
from discord.ext import commands
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
import aiohttp
print("imported mod")


class mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['m', 'Mute', 'mt'])
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason="No Reason was Provided"):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        if not mutedRole:
            mutedRole = await ctx.guild.create_role(name="Muted")

            for channel in ctx.guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=True)

        await member.add_roles(mutedRole, reason=reason)
        embed = discord.Embed(title="<a:verified:914545848648597524> Successfully Muted!",
                              description=f"**User** : {member.mention}\n**Reason** : {reason}\n  \n**Muted By** : {ctx.author.mention}", color=discord.Colour.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=ctx.guild.name)

        await ctx.send(embed=embed)
        await member.send(f"You were **Muted** in **{ctx.guild.name}**!\n**Reason** : {reason}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **Hey User, You Need `Manage Roles` Permission to Run this Command nab** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **Breh Wrong! Make Sure you Mention any User / Member! you dummy!** :robot:")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: **Make Sure you Actually Mention Someone who is In the Server! Dummy!** :robot:")

    @commands.command(aliases=['um'])
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        embed = discord.Embed(title="<a:verified:914545848648597524> Successfully Unmuted!",
                              description=f"**User** : {member.mention}\n  \n**Unmuted By** : {ctx.author.mention}", color=discord.Colour.green())
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=ctx.guild.name)

        await ctx.send(embed=embed)
        await member.send(f"You were **Unmuted** in **{ctx.guild.name}**!\nEnjoy!!")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **Hey User, You Need `Manage Roles` Permission to Run this Command, dont try to raid lmao** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **wrong! noob! Make Sure you Mention any User / Member!** :robot:")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: **Make Sure you Actually Mention Someone who is In the Server! Nub!** :robot:")

    @commands.command(aliases=['Ban'])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No Reason was Provided!"):
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="<a:verified:914545848648597524> Banned!", description=f"**Reason** : {reason}", color=discord.Colour.blue())
        embed.add_field(name="Member", value=member.mention, inline=True)
        embed.add_field(name="By", value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **Hey User, You Need `Ban Members` Permission to Run this Command, dont try to raid lmao** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **wrong! noob! Make Sure you Mention any User / Member!** :robot:")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: **Make Sure you Actually Mention Someone who is In the Server! Nub!** :robot:")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        bannedUsers = await ctx.guild.bans()
        name, discriminator = member.split("#")
        for ban in bannedUsers:
            user = ban.user

            if(user.name, user.discriminator) == (name, discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user.mention} was unbanned.")
                return

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **Hey User, You Need `Ban Members` Permission to Run this Command, dont try to raid lmao** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **wrong! noob! Make Sure you Mention any User / Member!** :robot:")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: **Make Sure to Enter a person who is banned u nab** :robot:")

    @commands.command(aliases=['clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int):
        if 0 < amount <= 1000:
            await ctx.message.delete()
            await ctx.channel.purge(limit=amount)
            await ctx.send(f"<a:verified:914545848648597524> The Messeges will be Remembered :wastebasket:", delete_after=5)
        else:
            await ctx.send(":x: Too Less/High Number's Broda")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **You Don't have the Required Permission to Run purge Command! Trying to remove evidence? hmmm sus** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("**Please Make Sure to add How many messages You want to Delete!**")

    @commands.command(aliases=['k'])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No Reason was Provided!"):
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="<a:verified:914545848648597524> User Kicked!", description=f"**REASON** : {reason}", color=discord.Colour.purple())
        embed.add_field(name="User", value=member.mention, inline=True)
        embed.add_field(name="Kicked by",
                        value=ctx.author.mention, inline=True)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f"{ctx.guild.name}")

        await ctx.send(embed=embed)

    @commands.command()
    async def tempmute(self, ctx, member: discord.Member, time: int, d, *, reason=None):
        guild = ctx.guild

        for role in guild.roles:
            if role.name == "Muted":
                await member.add_roles(role)

                embed = discord.Embed(title="muted!", description=f"{member.mention} has been tempmuted ", colour=discord.Colour.light_gray())
                embed.add_field(name="reason:", value=reason, inline=False)
                embed.add_field(name="time left for the mute:", value=f"{time}{d}", inline=False)
                await ctx.send(embed=embed)

                if d == "s":
                   await asyncio.sleep(time)

                if d == "m":
                    await asyncio.sleep(time*60)

                if d == "h":
                   await asyncio.sleep(time*60*60)

                if d == "d":
                    await asyncio.sleep(time*60*60*24)

                await member.remove_roles(role)

                embed = discord.Embed(title="Temp Mute Unmuted", description=f"Unmuted -{member.mention} ", colour=discord.Colour.light_gray())
                await ctx.send(embed=embed)

                return


    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":x: **Hey User, You Need `Kick members` Permission to Run this Command, dont try to raid lmao** :robot:")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: **wrong! noob! Make Sure you Mention any User / Member!** :robot:")
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(":x: **Make Sure you Actually Mention Someone who is In the Server! Nub!** :robot:")

    @commands.command(aliases=['lockdown'])
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, role: discord.Role = None):
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(
                send_messages=False)}
            await channel.edit(overwrites=overwrites)
            await ctx.send(f":lock: Locked {channel.mention} for every everyone :closed_lock_with_key:")
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f":lock: Locked {channel.mention} for every everyone :closed_lock_with_key:")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f":lock: Locked {channel.mention} for every everyone :closed_lock_with_key:")

    @commands.command(aliases=['unlockdown'])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=True)}
            await channel.edit(overwrites=overwrites)
            await ctx.send(f":lock_with_ink_pen:  Unlocked {channel.mention} for everyone! :unlock: ")
        elif channel.overwrites[ctx.guild.default_role].send_messages == False or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f":lock_with_ink_pen:  Unlocked {channel.mention} for everyone! :unlock: ")
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = None
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(f":lock_with_ink_pen:  Unlocked {channel.mention} for everyone! :lock: ")

    @lock.error
    async def lockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":rofl: You need `Manage Channels` For This nub! :robot:")

    @unlock.error
    async def unlockdown_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(":rofl: You need `Manage Channels` For This nub! :robot:")

    @commands.command(description="Blocks a user from sending message in that channel")
    @commands.has_permissions(kick_members=True)
    async def block(self, ctx, member: discord.Member):
        guild = ctx.guild
        if member == self.client.user:
            await ctx.send("**Haha, i am immortal**")
        elif guild.me.top_role < member.top_role:
            await ctx.send("**Member is higher than me in hierarchy**")
        elif member.bot:
            await ctx.send("**You cannot block bot**")
        elif member == ctx.author:
            await ctx.send("**You cannot block yourself**")
        else:
            if member.permissions_in(ctx.channel).send_messages == False:
                embed = discord.Embed(
                    title="Invalid usage",
                    description=f"{member.mention} is already blocked",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)
            else:
                #
                await ctx.channel.set_permissions(member, send_messages=False)
                embed = discord.Embed(
                    title="Block",
                    description=f"{member.mention} is blocked by {ctx.author.name} From channe {ctx.channel.name}",
                    color=0xFF000,
                )
                await ctx.send(embed=embed)

    @commands.command(description="Unblocks the blocked user")
    @commands.has_permissions(kick_members=True)
    async def unblock(self, ctx, member: discord.Member):
        if member.permissions_in(ctx.channel).send_messages == True:
            embed = discord.Embed(
                title="Invalid usage",
                description=f"{member.mention} is already unblocked",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

        else:
            await ctx.channel.set_permissions(member, send_messages=True)
            embed = discord.Embed(
                title="Unblock",
                description=f"{member.mention} is unblocked by {ctx.author.name}",
                color=0xFF000,
            )
            await ctx.send(embed=embed)

    @commands.command(description="Nukes a channel ( Clone and delete ) ")
    @commands.has_permissions(manage_channels=True)
    async def nuke(self, ctx, channel_name):
        channel_id = int("".join(i for i in channel_name if i.isdigit()))
        existing_channel = self.client.get_channel(channel_id)
        if existing_channel:
            await existing_channel.clone(reason="Has been nuked")
            await existing_channel.delete()
            embed = discord.Embed(
                title=f"Channel nuked || {ctx.author.name} || ", color=0x00FFFF
            )
            embed.set_image(
                url="https://media.tenor.com/images/e138ef6dcfc0f227e9ba27faf027c6ee/tenor.gif"
            )
            await ctx.author.send(embed=embed)
            await ctx.send(embed = embed)
        else:
            await ctx.send(f"No channel named **{channel_name}** was found")

def setup(client):
    client.add_cog(mod(client))