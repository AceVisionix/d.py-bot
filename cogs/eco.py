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

mainshop = [{"name":"banknote","price":1000000}]

async def buy_this(user,item_name,amount):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0]<cost:
        return [False,2]


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            obj = {"item":item_name , "amount" : amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item":item_name , "amount" : amount}
        users[str(user.id)]["bag"] = [obj]        

    with open("./EDB/balance.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost*-1,"wallet")

    return [True,"Worked"]

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 10000
        users[str(user.id)]["Gems"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["bank_space"] = 25000

    with open('./EDB/balance.json','w') as f:
        json.dump(users,f)
    return True


async def get_bank_data():
    with open('./EDB/balance.json','r') as f:
        users = json.load(f)
    return users


async def update_bank(user,change=0,mode = 'wallet'):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open('./EDB/balance.json','w') as f:
        json.dump(users,f)
    bal = users[str(user.id)]['wallet'],users[str(user.id)]['bank']
    return bal

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.7* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["bag"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t = 1
                break
            index+=1 
        if t == None:
            return [False,3]
    except:
        return [False,3]    

    with open("./EDB/balance.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")

    return [True,"Worked"]

class eco(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(case_insensitive = True)
    async def bal(self, ctx, member:discord.User = None):
        if member == None:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
        else:
            await open_account(member)
            user = member
            users = await get_bank_data()

        users = await get_bank_data()

        wallet = users[str(user.id)]["wallet"]
        gems = users[str(user.id)]["Gems"]
        bank = users[str(user.id)]["bank"]
        bank_space = users[str(user.id)]["bank_space"]
        net_worth = wallet + bank + gems
        if net_worth > 150000:
            allfooter = ["Woww Nicee!", "Rich Boi"]
        if net_worth > 50000:
            allfooter = ["I want that Money","Soo Rich","A Fat Wallet","I wonder, How do you have so much"]
        elif net_worth > 25000:
            allfooter = ["Noice Earnings","Rich","Noice","OOH", "Not so much but ok.."]
        elif net_worth > 1000:
            allfooter = ["Imagine Yourself","Bruh",".......",":(", "sad boi less moooneyy", "Bruh go earn or diee"]
        elif net_worth > 0:
            allfooter = ["Imagine having no Money"]
        footertext = random.choice(allfooter)
        embed = discord.Embed(title = f"{user.name}\'s balance ", color = discord.Color.random())
        embed.add_field(name = "━━━━━━━━━━━━━━", value = f"<a:Rcoin:914691033261047858> **Wallet** = {wallet}<a:Rcoin:914691033261047858>\n :gem: **Gems** = {gems} :gem:\n :bank: **Bank** = {bank}/{bank_space}<a:Rcoin:914691033261047858>\n :moneybag: **Net Worth** = {net_worth}<a:Rcoin:914691033261047858>")
        embed.set_footer(icon_url = user.avatar_url, text = f"{footertext}")
        await ctx.send(embed = embed)





    @commands.command(aliases=['rb'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self,ctx,member : discord.Member):
        if member.bot:
            await ctx.send("Hmm u **sussy cheater!**")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank(member)

        r = random.randrange(2)

        if r == 1:
            if bal[0]<100:
                await ctx.send("It is useless to rob him :( he's too poor")
                return

            earning = random.randrange(0,bal[0])

            await update_bank(ctx.author,earning)
            await update_bank(member,-1*earning)
            await ctx.send(f'{ctx.author.mention} You robbed **{member}** and got **{earning}**<a:Rcoin:914691033261047858>')
        else:
            await ctx.send("That Kid has a really Strong lock and u couldn't pick it. :x:")

    @rob.error
    async def rob_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f':x: Yo BRO Relax you dont need to rob to make a living You can try Again in **{round(error.retry_after, 2)} seconds.**')
            




    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
        user = ctx.author

        r = random.randrange(2)

        if r == 1:
            users = await get_bank_data()
            earnings = random.randrange(9999)
            responses = [f"Alright Here you go Take **{earnings}**", f"Heyo Your poor huh? ok here **{earnings}**<a:Rcoin:914691033261047858>", f"Someone Gave You **{earnings}**, I wonder how it was :thinking:"]

            embed = discord.Embed(title = f"{user} is Begging for Money!", description = random.choice(responses), color = discord.Color.random())
            await ctx.send(embed = embed)

            users[str(user.id)]["wallet"] += earnings
            with open("./EDB/balance.json",'w') as f:
                json.dump(users,f)
        else:
            await ctx.send("nO mONEY FOR YOu lol")

    @beg.error
    async def beg_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f':x: Command "`Beg`" is on cooldown, you can us it in **{round(error.retry_after, 2)} seconds.**')





    @commands.command(aliases=['wd', 'with'])
    async def withdraw(self, ctx, amount = None):
        await open_account(ctx.author)
        if amount == None:
            await ctx.send("**:robot: Please enter the amount you noob :x:**")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[1]:
            await ctx.send(f'Your Bank is Dry You cannot Withdraw **{amount}**<a:Rcoin:914691033261047858> beacuse your dont have That Much noob!')
            return
        if amount < 0:
            await ctx.send(':robot: **Amount must be positive! nab!** :x:')
            return
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,'bank')
        embed = discord.Embed(title = "Withdrawing Cash!", description = f"**{ctx.author}** Withdrew **{amount}**<a:Rcoin:914691033261047858>", color = discord.Color.random())
        await ctx.send(embed = embed)





    @commands.command(aliases=['dp', 'dep'])
    async def deposit(self, ctx,amount = None):
        await open_account(ctx.author)
        users = await get_bank_data()
        if amount == None:
            await ctx.send("**:robot: Please enter the amount you noob :x:**")
            return

        bal = await update_bank(ctx.author)

        space = users[str(ctx.author.id)]["bank_space"]
        bank = users[str(ctx.author.id)]["bank"]
        wallet = users[str(ctx.author.id)]["wallet"]

        if amount > bal[0]:
            await ctx.send(f'Your wallet is too dry You cannot Deposit **{amount}**<a:Rcoin:914691033261047858> beacuse your dont have That Much noob!')
            return
        if amount < 0:
            await ctx.send(':robot: **Amount must be positive! nab!** :x:')
            return

        limit = int(space) - int(bank)
        if int(amount) > int(limit):
            return await ctx.send("Hey, You Cant Deposit more Than Your Bank Space nub")

        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount,'bank')
        embed = discord.Embed(title = "Depositing Cash!", description = f"**{ctx.author}** Deposited **{amount}**<a:Rcoin:914691033261047858>", color = discord.Color.random())
        await ctx.send(embed = embed)





    @commands.command(aliases=['send', 'snd'])
    async def give(self, ctx,member : discord.Member,amount = None):
        await open_account(ctx.author)
        await open_account(member)
        if amount == None:
            await ctx.send("**:robot: Please enter the amount you noob :x:**")
            return

        bal = await update_bank(ctx.author)

        amount = int(amount)

        if amount > bal[0]:
            await ctx.send(f'Your Bank is Dry You cannot Give **{amount}**<a:Rcoin:914691033261047858> beacuse your dont have That Much noob!')
            return
        if amount < 0:
            await ctx.send(':robot: **Amount must be positive! nab!** :x:')
            return

        await update_bank(ctx.author,-1*amount)
        await update_bank(member,amount,'wallet')
        embed = discord.Embed(title = "Giving Cash!", description = f"**{ctx.author.mention}** You Gave **{member}** **{amount}<a:Rcoin:914691033261047858> Coins!**", color = discord.Color.random())
        await ctx.send(embed = embed)





    @commands.command(aliases = ["bet", "Bet"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gamble(self, ctx, arg=None):
        await open_account(ctx.author)
        limit = 250000
        with open("EDB/balance.json", "r") as f:
            data = json.load(f)
        wallet = data[str(ctx.author.id)]["wallet"]
        if arg == None:
            return await ctx.send("**WHY the Hell** Do You Want Me To Gamble With **Nothing** LOL")
        elif arg == "max":    
            with open("EDB/balance.json", "r") as f:
                data = json.load(f)
            wallet = data[str(ctx.author.id)]["wallet"]
            jack_of_trades = max(wallet, limit)
            if jack_of_trades == limit:
                lol = wallet
            if jack_of_trades == wallet:
                lol = limit
           
            gamblechance = random.randrange(15)
            if gamblechance >= 10 and gamblechance<= 15:
                urroll =  random.randrange(6) 
                botroll = urroll - random.randrange(2)
                        
                chance_of_gambling = urroll
                moneyback = int(lol) * int(chance_of_gambling)
                with open("./EDB/balance.json", "r") as f:
                    data = json.load(f)
                wallet = data[str(ctx.author.id)]["wallet"]
                new_wallet = wallet + int(moneyback)
                data[str(ctx.author.id)]["wallet"] = new_wallet
                with open("./EDB/balance.json", "w") as f:
                    json.dump(data,f, indent = 4)
                embed = discord.Embed(title=f"{ctx.message.author} You Won", description=f"**You Win!! <a:checked:888703788012171264>**", color=discord.Colour.dark_green() )
                embed.add_field(name="{0.user}'s Roll <a:Dice:914700255008792626>".format(self.client), value = f"Rolled {botroll} <a:Dice:914700255008792626>", inline=True)
                embed.add_field(name=f"{ctx.message.author}'s Roll <a:Dice:914700255008792626>", value = f"Rolled {urroll} <a:Dice:914700255008792626>", inline=True)
                embed.add_field(name=f"You won <a:Rcoin:914691033261047858>{moneyback}. Now You Have <a:Rcoin:914691033261047858>{new_wallet} in your wallet", value="Good Game my friend <a:clapss:896359060276928542>", inline=False)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                embed.timestamp = datetime.utcnow()
                await ctx.send (embed=embed)

                
            elif gamblechance <= 10:
                botroll = random.randrange(6) 
                urroll = botroll - random.randrange(5) 
                with open("./EDB/balance.json", "r") as f:
                    data = json.load(f)
                    wallet = data[str(ctx.author.id)]["wallet"]
                
                    new_wallet = wallet - int(lol)
                    data[str(ctx.author.id)]["wallet"] = new_wallet
                    with open("./EDB/balance.json", "w") as f:
                        json.dump(data,f, indent = 4)
                        embed = discord.Embed(title=f"{ctx.message.author} You Lost", description = f"**You lost <a:Rcoin:914691033261047858>{arg}!!**", color=discord.Colour.red() )
                        embed.add_field(name="{0.user}'s Roll <a:Dice:914700255008792626>".format(self.client), value = f"Rolled {botroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f"{ctx.message.author}'s Roll <a:Dice:914700255008792626>", value = f"Rolled {urroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f" Now You Have <a:Rcoin:914691033261047858>{new_wallet}", value=f"Better Luck Next Time {ctx.author.name}", inline=False)
                        embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                        embed.timestamp = datetime.utcnow()
                        await ctx.send (embed=embed)
        else:
            if int(wallet) >= int(arg):
                if int(arg) < int(limit):
                    gamblechance = random.randrange(15)
                    if gamblechance >= 10 and gamblechance<= 15:
                        urroll =  random.randrange(6) 
                        botroll = urroll - random.randrange(2)
                        
                        chance_of_gambling = urroll
                        moneyback = int(arg) * int(chance_of_gambling)
                        with open("EDB/balance.json", "r") as f:
                            data = json.load(f)
                        wallet = data[str(ctx.author.id)]["wallet"]
                        new_wallet = wallet + int(moneyback)
                        data[str(ctx.author.id)]["wallet"] = new_wallet
                        with open("EDB/balance.json", "w") as f:
                            json.dump(data,f, indent = 4)
                        embed = discord.Embed(title=f"{ctx.message.author} You Won", description=f"🥳 **You Won <a:Rcoin:914691033261047858>{moneyback}!!**", color=discord.Colour.dark_green() )
                        embed.add_field(name="{0.user}'s Roll <a:Dice:914700255008792626>".format(self.client), value = f"Rolled {botroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f"{ctx.message.author}'s Roll <a:Dice:914700255008792626>", value = f"Rolled {urroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858>{new_wallet}", value="Good Game My Friend <a:clapss:896359060276928542>", inline=False)
                        embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                        embed.timestamp = datetime.utcnow()
                        await ctx.send (embed=embed)

                
                    elif gamblechance <= 10:
                        botroll = random.randrange(6) 
                        urroll = botroll - random.randrange(5) 
                        with open("EDB/balance.json", "r") as f:
                            data = json.load(f)
                        wallet = data[str(ctx.author.id)]["wallet"]
                
                        new_wallet = wallet - int(arg)
                        data[str(ctx.author.id)]["wallet"] = new_wallet
                        with open("EDB/balance.json", "w") as f:
                            json.dump(data,f, indent = 4)
                        embed = discord.Embed(title=f"{ctx.message.author} You Lost", description = f"**You lost <a:Rcoin:914691033261047858>{arg}**", color=discord.Colour.red() )
                        embed.add_field(name="{0.user}'s Roll <a:Dice:914700255008792626>".format(self.client), value = f"Rolled {botroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f"{ctx.message.author}'s Roll <a:Dice:914700255008792626>", value = f"Rolled {urroll} <a:Dice:914700255008792626>", inline=True)
                        embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858>{new_wallet}", value=f"Better Luck Next Time {ctx.author.name}", inline=False)
                        embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                        embed.timestamp = datetime.utcnow()
                        await ctx.send (embed=embed)
                    
                else:
                    return await ctx.send(f"You are going above the limit - 250000")
            else:
                return await ctx.send ("You dont have money")

    @gamble.error
    async def gamble_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f':x: YO BRO WO WO WO SLOWDOWN You\'re betting too fast go slower, try again after **{round(error.retry_after, 2)} seconds.**')





    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slots(self, ctx, arg=None):
        await open_account(ctx.author)
        with open("EDB/balance.json", "r") as f:
            data = json.load(f)
        wallet = data[str(ctx.author.id)]["wallet"]
        limit = 500001
        Slotsemote = [":bomb:", ":8ball:", ":military_medal:", ":rosette:", ":musical_score:", ":slot_machine:", ":helicopter:", ":crown:", ":gem"]
        if arg == None:
            return await ctx.send("Your Slot Machine Crashed Because It had No Money")


        shuffle1 = random.choice(Slotsemote)
        shuffle2 = random.choice(Slotsemote)
        shuffle3 = random.choice(Slotsemote)
        if int(arg) < int(wallet):
            if int(arg) < int(limit):
                if shuffle1 == shuffle2:
            
                    luck = random.randrange(20, 40)
                    with open("EDB/balance.json", "r") as f:
                        data = json.load(f)
                    wallet = data[str(ctx.author.id)]["wallet"]
                    wallet_with_luck = int(arg) + int(luck) 
                    new_wallet = int(wallet) + int(wallet_with_luck)
                    data[str(ctx.author.id)]["wallet"] = new_wallet
                    with open("EDB/balance.json", "w") as f:
                        json.dump(data,f, indent = 4)
                    embed = discord.Embed(title=f":slot_machine: {ctx.message.author} slot machine :slot_machine:", description = f"**You Won <a:Rcoin:914691033261047858> {wallet_with_luck}**", color=discord.Colour.green() )
                    embed.add_field(name ="Slot Machine Roll", value = f"{shuffle1}⠀┃⠀{shuffle2}⠀┃⠀{shuffle3}", inline=False)
                    embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858> {new_wallet}", value="Great Job!", inline=False)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                    embed.timestamp = datetime.utcnow()
                    await ctx.send (embed=embed)
                elif shuffle1 == shuffle2 == shuffle3:
                    luck = random.randrange(41, 69)
                    with open("EDB/balance.json", "r") as f:
                        data = json.load(f)
                    wallet = data[str(ctx.author.id)]["wallet"]
                    wallet_with_luck = int(arg) + int(luck) 
                    new_wallet = int(wallet) + int(wallet_with_luck)
                    data[str(ctx.author.id)]["wallet"] = new_wallet
                    with open("EDB/balance.json", "w") as f:
                        json.dump(data,f, indent = 4)
                    embed = discord.Embed(title=f":slot_machine: {ctx.message.author} slot machine :slot_machine:",description = f"**You Won <a:Rcoin:914691033261047858> {wallet_with_luck}**", color=discord.Colour.green() )
                    embed.add_field(name="Slot Machine Roll", value = f"{shuffle1}⠀┃⠀{shuffle2}⠀┃⠀{shuffle3}", inline=False)
                    embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858> {new_wallet} in your wallet", value="Great job!", inline=False)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                    embed.timestamp = datetime.utcnow()
                    await ctx.send (embed=embed)
                elif shuffle2 == shuffle3:
                    luck = random.randrange(20, 40)
                    with open("EDB/balance.json", "r") as f:
                        data = json.load(f)
                    wallet = data[str(ctx.author.id)]["wallet"]
                    wallet_with_luck = int(arg) + int(luck) 
                    new_wallet = int(wallet) + int(wallet_with_luck)
                    data[str(ctx.author.id)]["wallet"] = new_wallet
                    with open("EDB/balance.json", "w") as f:
                        json.dump(data,f, indent = 4)
                    embed = discord.Embed(title=f":slot_machine: {ctx.message.author} slot machine :slot_machine:", description = f"**You Won <a:Rcoin:914691033261047858> {wallet_with_luck}**", color=discord.Colour.green() )
                    embed.add_field(name="Slot Machine Roll", value = f"{shuffle1}⠀┃⠀{shuffle2}⠀┃⠀{shuffle3}", inline=False)
                    embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858> {new_wallet} in your wallet", value="Great job!", inline=False)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                    embed.timestamp = datetime.utcnow()
                    await ctx.send (embed=embed)
                else:
                    with open("EDB/balance.json", "r") as f:
                        data = json.load(f)
                    wallet = data[str(ctx.author.id)]["wallet"] 
                    new_wallet = int(wallet) - int(arg)
                    data[str(ctx.author.id)]["wallet"] = new_wallet
                    with open("EDB/balance.json", "w") as f:
                        json.dump(data,f, indent = 4)
                    embed = discord.Embed(title=f":slot_machine: {ctx.message.author}'s slot machine :slot_machine:", description = f"**You Lost <a:Rcoin:914691033261047858> {arg}**", color=discord.Colour.red() )
                    embed.add_field(name="Slot Machine Roll", value = f"{shuffle1}⠀┃⠀{shuffle2}⠀┃⠀{shuffle3}", inline=False)
                    embed.add_field(name=f"Now You Have <a:Rcoin:914691033261047858> {new_wallet} in your wallet", value= f"Better Luck Next time {ctx.author.name}", inline=False)
                    embed.set_footer(icon_url = ctx.author.avatar_url, text = ctx.author.name)
                    embed.timestamp = datetime.utcnow()
                    await ctx.send (embed=embed)
            else:
                await ctx.send(f"You are going above the limit - {limit}")
        else:
            await ctx.send ("You have less money than Your argument")

    @slots.error
    async def slots_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'YO BRO SLOWDOWN you\'re too fast for me to handle lmaaaooo try again after **{round(error.retry_after, 2)}**.')




    @commands.command()
    async def shop(self, ctx):
        embed = discord.Embed(title = "Razystic Shop!", description = "Run `.buy <item name>` to buy and `.sell <item name> to sell`")
        await ctx.send(embed = embed)




    @commands.command()
    async def buy(self, ctx, item, amount = 1):
        await open_account(ctx.author)

        res = await buy_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("**That Item doesnt exsist just like your brain!** :robot:")
                return
            if res[1]==2:
                await ctx.send(f"** :robot: You don't have enough money in your wallet to buy {amount} {item} :x:**")
                return
                
        embed = discord.Embed(title = "Item Purchased!", description = f"**{ctx.author}** Just Bought a **{amount} {item}**", color = discord.Color.random())
        await ctx.send(embed = embed)





    @commands.command()
    async def sell(self, ctx,item,amount = 1):
        await open_account(ctx.author)

        res = await sell_this(ctx.author,item,amount)

        if not res[0]:
            if res[1]==1:
                await ctx.send("Object doesnt exsist like yo brain")
                return
            if res[1]==2:
                await ctx.send(f"You don't have {amount} {item} in your Inventory.")
                return
            if res[1]==3:
                await ctx.send(f"You don't have {item} in your Inventory.")
                return

        await ctx.send(f"You just sold {amount} {item}.")





    @commands.command(aliases= ["inv", "INv", "Inv", "INV"])
    async def inventory(self, ctx, member: discord.Member = None):

        if member == None:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
        else:
            await open_account(member)
            user = member
            users = await get_bank_data()
        try:
            b = users[str(user.id)]["bag"]
        except:
            b = []

        embed = discord.Embed(title = f"{user.name}'s Inventory", color = discord.Color.random())
        for item in b:
            name = item["item"]
            if name.lower() == "banknote":
                name = "Bank Note"
                emojee = ":money:"
                iteminfo = "**ID** - `note`\n**Item Type** - Usable"
            amount = item["amount"]
            embed.add_field(name = f"{emojee}  {name} = {int(amount)}", value = f"{iteminfo}", inline = True)
        await ctx.reply(embed = embed)





    @commands.command()
    async def profile(self, ctx, member:discord.Member = None):
        await open_account(ctx.author)
        if member == None:
            await open_account(ctx.author)
            user = ctx.author
            users = await get_bank_data()
        else:
            await open_account(member)
            user = member
            users = await get_bank_data()
        with open("./EDB/profile.json", "r") as f:
            data = json.load(f)
        if str(user.id) not in data:
            data[str(user.id)] = {}
            data[str(user.id)]["house"] = None
            data[str(user.id)]["car"] = None
            with open("./EDB/profile.json", "w")as f:
                json.dump(data, f, indent = 4)
        h = data[str(user.id)]["house"]
        c = data[str(user.id)]["car"]
        embed = discord.Embed(title = f"{ctx.author.name}'s Profile", description = "<a:arroww:896351538635751465>Title: Coming Soon", color = discord.Color.random())
        users = await get_bank_data()
        wallet = users[str(user.id)]["wallet"]
        bank = users[str(user.id)]["bank"]
        bank_space = users[str(user.id)]["bank_space"]
        gems = users[str(user.id)]["Gems"]
        net_worth = bank + wallet + gems*1000000000
        try:
            b = users[str(user.id)]["bag"]
        except:
            b = []
        embed.add_field(name = ":white_small_square: Level", value="Coming soon", inline = True)
        embed.add_field(name = ":white_small_square: Experience", value="Coming soon", inline = True)
        embed.add_field(name = "⠀", value = "⠀")
        embed.add_field(name = ":white_small_square: Economy Money", value=f"**Wallet -** <a:Rcoin:914691033261047858> `{wallet}`\n **Bank Money -** <a:Rcoin:914691033261047858>`{bank}`\n **Bank Space -** <a:Rcoin:914691033261047858>`{bank_space}`\n **Gems -** :gem:`{gems}`\n **Net Worth -** <a:Rcoin:914691033261047858>`{net_worth}`", inline = True)
        embed.add_field(name = "⠀", value = "⠀")
        embed.add_field(name = "⠀", value = "⠀")
        embed.add_field(name = ":white_small_square: Inventory", value = "Coming Soon", inline = True)
        embed.add_field(name = "⠀", value = "⠀")
        embed.add_field(name = "⠀", value = "⠀")
        embed.add_field(name = ":white_small_square: House", value = f"**House:** {h}\n**Car:** {c}", inline = True)
        embed.add_field(name = ":white_small_square: Active Items", value = "Coming Soon", inline = True)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        await ctx.send(embed = embed)





    @commands.command()
    async def hack(self, ctx, member: discord.Member):
        msg = await ctx.send(f"Hacking {member} 1% Complete")
        await msg.edit(f"Hacking {member} 2% Complete")
        await msg.edit(f"Hacking {member} 6% Complete")
        await msg.edit(f"Hacking {member} 7% Complete")
        await msg.edit(f"Hacking {member} 8% Complete")
        await msg.edit(f"Hacking {member} 9% Complete")
        await msg.edit(f"Hacking {member} 10% Complete")
        await msg.edit(f"Hacking {member} 15% Complete")
        await msg.edit(f"Hacking {member} 19% Complete")
        await msg.edit(f"Hacking {member} 20% Complete")
        await msg.edit(f"Hacking {member} 25% Complete")
        await msg.edit(f"Hacking {member} 30% Complete")
        await msg.edit(f"Hacking {member} 35% Complete")
        await msg.edit(f"Hacking {member} 40% Complete")
        await msg.edit(f"Hacking {member} 50% Complete")
        await msg.edit(f"Hacking {member} 69% Complete")
        await msg.edit(f"Hacking {member} 70% Complete")
        await msg.edit(f"Hacking {member} 80% Complete")
        await msg.edit(f"Hacking {member} 100% Complete")
        await msg.edit(f"The Totally Dangerous Hack is complete")
        await msg.edit(f"His Password is ||{member}isabignab69420noob||")





    @commands.command(aliases = ["lb"])
    async def leaderboard(self, ctx,x = 10):
        users = await get_bank_data()
        leader_board = {}
        total = []
        for user in users:
            name = int(user)
            total_amount = users[user]["wallet"] + users[user]["bank"]
            leader_board[total_amount] = name
            total.append(total_amount)

        total = sorted(total,reverse=True)    

        em = discord.Embed(title = f"Top {x} Richest People" , description = "This is The **Leaderboard** of People with the **Highest** Amount of **Money!**",color = discord.Color(0xfa43ee))
        index = 1
        for amt in total:
            id_ = leader_board[amt]
            member = self.client.get_user(id_)
            name = member.name
            em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
            if index == x:
                break
            else:
                index += 1
        await ctx.send(embed = em)


def setup(client):
    client.add_cog(eco(client))