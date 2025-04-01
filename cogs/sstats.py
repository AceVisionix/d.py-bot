import discord
from discord import colour
from discord import permissions
from discord import message
from discord.colour import Color
from discord.ext import commands, tasks
import json
import asyncio
import time
class serverstats(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("./databases/serverstats.json", "r")as f:
            data = json.load(f)
        if str(member.guild.id) not in data:
            return
        try:
            guild = message.guild
            member_count = len(guild.members)
            true_member_count = len([m for m in guild.members if not m.bot])
            channelid1 = data[str(guild.id)]["tmembers"]  
            channelid2 = data[str(guild.id)]["bots"] 
            channelid3 = data[str(guild.id)]["members"]
            channelconv = await guild.get_channel(int(channelid1))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {member_count}")
            channelconv = await guild.get_channel(int(channelid2))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {member_count - true_member_count}")
            channelconv = await guild.get_channel(int(channelid3))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {true_member_count}")
        except:
            await asyncio.sleep(605)
            true_member_count = len([m for m in guild.members if not m.bot])
            channelid1 = data[str(guild.id)]["tmembers"]  
            channelid2 = data[str(guild.id)]["bots"] 
            channelid3 = data[str(guild.id)]["members"]
            channelconv = await guild.get_channel(int(channelid1))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {member_count}")
            channelconv = await guild.get_channel(int(channelid2))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {member_count - true_member_count}")
            channelconv = await guild.get_channel(int(channelid3))
            channelinter = channelconv.name
            channel = channelinter.split(":")
            await channel.edit(name=f"{channel[1]} : {true_member_count}")

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        with open("./databases/serverstats.json", "r")as f:
        	data = json.load(f)
        if str(member.guild.id) not in data:
        	return
        guild = member.guild
        try:
            member_count = len(guild.members)
            true_member_count = len([m for m in guild.members if not m.bot])
            channelid1 = data[str(guild.id)]["tmembers"]  
            channelid2 = data[str(guild.id)]["bots"] 
            channelid3 = data[str(guild.id)]["members"]
            channelconv = discord.utils.get(guild.voice_channels, id = channelid1)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {member_count}")
            channelconv = discord.utils.get(guild.voice_channels, id = channelid2)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {member_count - true_member_count}")
            channelconv = discord.utils.get(guild.voice_channels, id = channelid3)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {true_member_count}")
        except:
            await asyncio.sleep(605)
            true_member_count = len([m for m in guild.members if not m.bot])
            channelid1 = data[str(guild.id)]["tmembers"]  
            channelid2 = data[str(guild.id)]["bots"] 
            channelid3 = data[str(guild.id)]["members"]
            channelconv = discord.utils.get(guild.voice_channels, id = channelid1)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {member_count}")
            channelconv = discord.utils.get(guild.voice_channels, id = channelid2)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {member_count - true_member_count}")
            channelconv = discord.utils.get(guild.voice_channels, id = channelid3)
            channelinter = channelconv.name
            channel = channelinter.rstrip(":")
            await channel.edit(name=f"{channel} : {true_member_count}")

    @commands.command(aliases = ["serverstat"])
    @commands.has_permissions(manage_channels=True)
    async def serverstats(self ,ctx):
        with open("./databases/serverstats.json", "r")as f:
            data = json.load(f)
        guild = ctx.guild
        if str(guild.id) not in data:
            member_count = len(ctx.guild.members) # includes bots

            true_member_count = len([m for m in ctx.guild.members if not m.bot])
            checklister = discord.Embed(title = f"Checklist On Setting of Serverstats",description=f"<a:load:880367245417644032> | Creating Channel `Total Members : {member_count}` and Applying Overrides\n<:vetblank:867758570807099402>| Creating Channel `Bots : {int(member_count)-int(true_member_count)}` and Applying Overrides\n<:vetblank:867758570807099402>| Creating Channel `Members : {int(true_member_count)}` and Applying Overrides", color=discord.Colour.green())
            checklister.set_footer(text = f"The Person Who Requested This - {ctx.author}")
            checklist = await ctx.send(embed = checklister)
            guild = ctx.guild
            member = ctx.author

            overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False),
            guild.me: discord.PermissionOverwrite(manage_channels=True),
        
            }
            
            channel1 = await guild.create_voice_channel(f'Total Members : {member_count}', overwrites=overwrites)
            checklister2 = discord.Embed(title = f"Checklist On Setting of Serverstats",description=f"<a:checked:880263293195915274> | Creating Channel `Total Members : {member_count}` and Applying Overrides\n<a:load:880367245417644032> | Creating Channel `Bots : {int(member_count)-int(true_member_count)}` and Applying Overrides\n<:vetblank:867758570807099402>| Creating Channel `Members : {int(true_member_count)}` and Applying Overrides", color=discord.Colour.green())
            checklister2.set_footer(text = f"The Person Who Requested This - {ctx.author}")
            await checklist.edit(embed = checklister2)
            channel2 = await guild.create_voice_channel(f'Bots : {member_count - true_member_count}', overwrites=overwrites)
            checklister3 = discord.Embed(title = f"Checklist On Setting of Serverstats",description=f"<a:checked:880263293195915274> | Creating Channel `Total Members : {member_count}` and Applying Overrides\n<a:checked:880263293195915274> | Creating Channel `Bots : {int(member_count)-int(true_member_count)}` and Applying Overrides\n<a:load:880367245417644032>| Creating Channel `Members : {int(true_member_count)}` and Applying Overrides", color=discord.Colour.green())
            checklister3.set_footer(text = f"The Person Who Requested This - {ctx.author}")
            await checklist.edit(embed = checklister3)
            channel3 = await guild.create_voice_channel(f'Members : {true_member_count}', overwrites=overwrites)
            checklister4 = discord.Embed(title = f"Checklist On Setting of Serverstats",description=f"<a:checked:880263293195915274> | Creating Channel `Total Members : {member_count}` and Applying Overrides\n<a:checked:880263293195915274> | Creating Channel `Bots : {int(member_count)-int(true_member_count)}` and Applying Overrides\n<a:checked:880263293195915274>| Creating Channel `Members : {int(true_member_count)}` and Applying Overrides", color=discord.Colour.green())
            checklister4.set_footer(text = f"The Person Who Requested This - {ctx.author}")
            await checklist.edit(embed = checklister4)
            data[str(guild.id)] = {}
            data[str(guild.id)]["tmembers"] = str(channel1.id)
            data[str(guild.id)]["bots"] = str(channel2.id)
            data[str(guild.id)]["members"] = str(channel3.id)
            with open("./databases/serverstats.json", "w")as f:
                json.dump(data,f,indent = 4)
            
        else:
            return await ctx.send("Sorry. You can\'t Run This Command Because there is already a serverstats running in your server")


def setup(client):
    client.add_cog(serverstats(client))