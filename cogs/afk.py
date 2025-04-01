import discord
from discord.ext import commands
from discord.utils import get
import random


afks = {}

def remove (afk):
    if "(AFK)" in afk.split():
        return " ".join(afk.split)()[1:]
    else:
        return afk

class away(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def afk(self, ctx, *,reason = "No Reason Provided"):
        member = ctx.author
        if member.id in afks.keys():
          afks.pop(member.id)
        else:
            try:
                await ctx.send(f'<a:verified:914545848648597524> AFK Now! <a:verified:914545848648597524>')
            except:
                pass
        afks[member.id] = reason
        embed = discord.Embed(title = ":zzz: Member AFK", description = f"{member.mention} has Gone AFK", color = member.color)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_author(name = member.name, icon_url = member.avatar_url)
        embed.add_field(name = 'AFK Note: ', value = reason)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in afks.keys():
            afks.pop(message.author.id)
            try:
                await message.author.edit(nick = remove(message.author.display_name))
            except:
                pass
            await message.channel.send(f'<a:verified:914545848648597524> Welcome Back {message.author.name}, I removed Your AFK')

        for id, reason in afks.items():
            member = discord.utils.get(self.client.get_all_members(), id = id)
            if (message.reference and member == (await message.channel.fetch_message(message.reference.message_id)).author) or member.id in message.raw_mentions:
                embed = discord.Embed(title = "Member is Afk", description = f"I'm Afk - {reason}", color = discord.Color.random())
                await message.reply(embed = embed)

def setup(client):
    client.add_cog(away(client))