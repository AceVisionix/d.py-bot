import discord
from discord.ext import commands
from cogs.eco import update_bank, open_account

class g(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def getguild(self, ctx):
        vision_id = 880846666624811088
        if ctx.author.id == vision_id: 
            messages = []   
            for guild in self.client.guilds:
                messages.append(f"{guild.name}")
                x = guild.members
                xp = len(x)
            #for member in x:
                #await ctx.send(">" + f" {member}")
                await ctx.send(f"**{guild.name}** has **{xp}** members and owner is **{guild.owner}**")

            await ctx.send("\n".join(messages))

    @commands.command()
    async def botstats(self, ctx):
        serverCount = len(self.client.guilds)
        memberCount = len(set(self.client.get_all_members()))
        embed = discord.Embed(title = "Bot Stats", description = f"**Server Count:** {serverCount}\n**Bot's Version:** 1.0.0\nHelping **{memberCount}** Members!\nCreated with **Pycord** Library!", color = discord.Color.random())
        await ctx.send(embed = embed)

    @commands.command(aliases = ["addm"])
    async def addmoney(self, ctx, member: discord.Member = None, *,amount):
        vision_id = 880846666624811088
        falcon_id = 881095807565172776
        a_id = 824384708300374117
        uprise_ID = 771310556014706688
        real_id = 785400711935557672
        shannu = 734388362214899763
        infe = 811519599598239745
        if ctx.author.id == vision_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == falcon_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == a_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == uprise_ID:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == real_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == shannu:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        if ctx.author.id == infe:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,1*amount,'wallet')
            await ctx.send(f'Done!, added {amount} to {member}')
        else:
            return
        
    @commands.command(aliases = ["removem"])
    async def removemoney(self, ctx, member: discord.Member = None, *,amount):
        vision_id = 880846666624811088
        falcon_id = 881095807565172776
        a_id = 824384708300374117
        uprise_ID = 771310556014706688
        real_id = 785400711935557672
        shann = 734388362214899763
        infe = 811519599598239745
        if ctx.author.id == vision_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == falcon_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == a_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == uprise_ID:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == real_id:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == shann:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        if ctx.author.id == infe:
            await open_account(member)
            amount = int(amount)
            await update_bank(member,-1*amount,'wallet')
            await ctx.send(f'Done!, removed {amount} to {member}')
        else:
            return
        
def setup(client):
    client.add_cog(g(client))