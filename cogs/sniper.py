import discord
from discord import colour
from discord import permissions
from discord import message
from discord.colour import Color
from discord.ext import commands
import json
import asyncio

class sniper(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("./databases/esniper.json", "r")as f:
            data = json.load(f)
        if str(before.guild.id) not in data:
            data[str(before.guild.id)] = {}
            data[str(before.guild.id)]["beforemsg"] = None
            data[str(before.guild.id)]["aftermsg"] = None
            data[str(before.guild.id)]["author"] = None
            with open("./databases/esniper.json", "w") as f:
                json.dump(data,f,indent = 4)
        
        data[str(before.guild.id)]["beforemsg"] = str(before.content)
        data[str(before.guild.id)]["aftermsg"] = str(after.content)
        data[str(before.guild.id)]["author"] = str(before.author)
        with open("./databases/esniper.json", "w") as f:
            json.dump(data,f,indent = 4)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("./databases/sniper.json", "r")as f:
            data = json.load(f)
        if str(message.guild.id) not in data:
            data[str(message.guild.id)] = {}
            data[str(message.guild.id)]["msg"] = None
            data[str(message.guild.id)]["author"] = None
            with open("./databases/sniper.json", "w") as f:
                json.dump(data,f,indent = 4)
        
        data[str(message.guild.id)]["msg"] = str(message.content)
        data[str(message.guild.id)]["author"] = str(message.author)
        with open("./databases/sniper.json", "w") as f:
            json.dump(data,f,indent = 4)
    
    @commands.command(aliases = ["esniper"])
    async def editsnipe(self ,ctx):
        with open("./databases/esniper.json", "r")as f:
            data = json.load(f)
        msgbefore = data[str(ctx.guild.id)]["beforemsg"]
        msgafter = data[str(ctx.guild.id)]["aftermsg"]
        author = data[str(ctx.guild.id)]["author"]
        esnipeem = discord.Embed(title = f"{author}\'s Edit Sniped Message",description=f"Original message : `{msgbefore}`\nEdited Message : `{msgafter}`")
        esnipeem.set_footer(text = f"The Person Who Requested This - {ctx.author}")
        await ctx.send(embed = esnipeem)
    
    @commands.command(aliases = ["sniper"])
    async def snipe(self ,ctx):
        with open("./databases/sniper.json", "r")as f:
            data = json.load(f)
        author = data[str(ctx.guild.id)]["author"]
        msg = data[str(ctx.guild.id)]["msg"]
        esnipeem = discord.Embed(title = f"{author}\'s Sniped Message",description=f"Original message : `{msg}`")
        esnipeem.set_footer(text = f"The Person Who Requested This - {ctx.author}")
        await ctx.send(embed = esnipeem)
    
    @commands.command()
    async def emojis(self, ctx, msg: str = None):
        """List all emojis in this server. Ex: [p]server emojis"""
        if msg:
            server, found = self.find_server(msg)
            if not found:
                return await ctx.send(server)
        else:
            server = ctx.message.guild
        emojis = [str(x) for x in server.emojis]
        await ctx.send("".join(emojis))
        await ctx.message.delete()

def setup(client):
    client.add_cog(sniper(client))