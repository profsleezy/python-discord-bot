from gettext import find
from ssl import CERT_NONE
import discord
from discord.ext import commands
import random
from matplotlib.collections import Collection
import asyncio
from aiohttp import request
import motor.motor_asyncio
import motor
from urllib import parse, request
from discord.ext.commands import cooldown, BucketType
import re
import textwrap
import urllib
import aiohttp
import datetime
import requests

rate = [
    'way too gay','very gay','a hundred percent gay','definietely homosexual', 'super gay', 'watching gay porn', 'sucking cock','wondering where his dad is',
    'gay to the max', 'on tinder looking for big black men','in need of straightness','crazy gay','not straight','gay. just gay.','ultra gay','mega gay',
    'looking at big black co-','obsessed with people of the same gender','in love with someone of the same gender','GAY','G+A+Y','getting a blowjob from a man','searching for one night stands with men',
    'gay without a doubt','definitely gay','certainly','gay for sure','gay undoubtedly','in the closet but gay both anyways LOL','gay no cap','eating a mans ass',
    'making love with the same gender','definitely homo','homosexual for sure','homosexual undoubtedly','homosexual without a doubt','secretly filming gay por','just enjoying being gay',
    'obviously gay','gay without the e','straight from walmart','unstraight','searching for a father and a daddy','begging for co-','single. and gay.','depressed. but no one cares he gay anyways LOL',
    'trying to come out but is afraid to lose his father','HOMOSEXUAL','the gay friend','pounding a man from the back','disappointing god right now','unsurprisingly gay','simply gay','doing gay shit rn','gay in spanish'
    ]

rude = [
    'shut yo dum dum lookin ass up','stop pinging cockhead','nobody even cares bruh','your mom','ping again if gay','shut the fuck up','i feel bad for your parents','suck mi cock',
    'go look for a dad','gay','95.181.232.3 this you bitch??','you a ho if you ping again','bruh what','im watching good stuff dont mind me','why you gotta be so annoying',
    'dont you got friends to talk to???',]

slapping = [' destroyed the face of ', ' slapped the shit out of ', ' knocked out ', ' slaps ',' slaps the sense out of ', ' disrespectfully slaps ']

ball = ['yes','indeed','maybe','probably','i dont think so','no lol','ofc not LOL','real question is, why are you gay','no but are you gay??','big black men tho','jesus christ what']



cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://botmaker:54321abc@veryoriginalbot.6q8pj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl_cert_reqs=CERT_NONE")
db = cluster.discord
collection = db.bank


bot = commands.Bot(command_prefix = "!")

    
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.send("error")

# other slash commands

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230], description='slap someone for some reason')
async def slap(ctx, name: str):
    await ctx.respond(f'{ctx.author.mention}' + random.choice(slapping) + f'{name}')

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230], description='ask it anything')
async def eightball(ctx, question: str):
    await ctx.respond(f' {ctx.author.mention} asked "{question}". Answer: ' + random.choice(ball))

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230], description='totally not stolen from dank memer')
async def howgay(ctx, name: str):
    await ctx.respond(f'{name} is ' + random.choice(rate))

#@bot.listen()
#async def on_message(message):
#    if "gay" in message.content.lower():
        # in this case don't respond with the word "Tutorial" or you will call the on_message event recursively
#       await message.channel.send('no u lol')
#        await bot.process_commands(message)


# economy slash commands

@bot.slash_command(name="bank", description="check your balance!", guild_ids=[931679366365204600, 932716813580636230])
async def bank(ctx, member: discord.Member=None):
    if member == None:
        member = ctx.author

    findbank = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": member.id, "bank": 0, "wallet": 0})

    amt = findbank["bank"]
    wallet = findbank["wallet"]

    embed = discord.Embed(
        title=f"{member.name}'s balance.",
        colour = discord.Colour.random()
    ) 
    embed.add_field(name="bank", value=f"{str(amt)}", inline=True)
    embed.add_field(name="wallet", value=f"{str(wallet)}", inline=True)

    await ctx.respond(embed=embed)

	

@bot.slash_command(name="steal", description="earn money by picking from user's pockets.", guild_ids=[931679366365204600, 932716813580636230])
#@commands.cooldown(1,60, commands.BucketType.user)
async def steal(ctx, user: discord.Member):
    member = user
    findbank = await collection.find_one({"_id": ctx.author.id})
    findbankuser = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": ctx.author.id, "bank": 0, "wallet": 0})
    if not findbank:
        await collection.insert_one({"_id": member.id, "bank": 0, "wallet": 0})
	
    if user.id is ctx.author.id:
	ctx.send("Ong you make my job harder everyday")
     
    luck = random.randint(1,2)
    wallet = findbank["wallet"]
    wallet_user = findbankuser["wallet"]
    random_money = random.randrange(1, wallet_user)

    if wallet_user == 0:
        await ctx.send("You cannot steal imaginary money")

    if luck == 1:
        updated_money = wallet + random_money
        updated_money_user = wallet_user - random_money
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_money_user}})
        await collection.update_one({"_id": ctx.author.id}, {"$set": {"wallet": updated_money}})
        await ctx.respond(f"You successfuly pickpocket {user}! you now have {updated_money} while they have {updated_money_user}")
    if luck == 2:
        await ctx.respond(f"You failed to pickpocket {user}! mfs can't do shit right these days smh!")

@bot.slash_command(name="pickpocket", description="earn money by picking from people's pockets. cooldown = 2 seconds", guild_ids=[931679366365204600, 932716813580636230])
@commands.cooldown(1,5, commands.BucketType.user)
async def pickpocket(ctx):
    member = ctx.author
    findbank = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": member.id, "bank": 0, "wallet": 0})
	
    luck = random.randint(1,2)
    wallet = findbank["wallet"]
    random_money = random.randrange(1, 130)

    if random_money == 0:
        await ctx.respond(f"let's just say you failed")

    if luck == 1:
        updated_money = wallet + random_money
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_money}})
        await ctx.respond(f"You successfuly pickpocket someone! You now have {updated_money}.")
    if luck == 2:
        await ctx.respond(f"You failed to pickpocket someone! mfs can't do shit right these days smh!")
    


@bot.slash_command(name="deposit", description="depositing the money in your wallet to the bank.", guild_ids=[931679366365204600, 932716813580636230])
async def deposit(ctx, money):
    member = ctx.author
    findbank = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": member.id, "bank": 0, "wallet": 0})
    
    wallet = findbank["wallet"]
    bankamnt= findbank["bank"]

    updated_wallet = wallet - int(money)
    updated_bank = bankamnt + int(money)

    if int(money) > wallet:
        await ctx.respond("Let's face reality, you don't have that much money")
    
    if int(money) <= 0:
        await ctx.respond("wake up to reality, you can't deposit imaginary money")
    
    else:
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_wallet}})
        await collection.update_one({"_id": member.id}, {"$set": {"bank": updated_bank}})
        await ctx.respond("Money deposited successfully!")

@bot.slash_command(name="withdraw", description="withdrawing the money in the bank to your wallet.", guild_ids=[931679366365204600, 932716813580636230])
async def withdraw(ctx, money):
    member = ctx.author
    findbank = await collection.find_one({"_id": member.id})
    if not findbank:
        await collection.insert_one({"_id": member.id, "bank": 0, "wallet": 0})
    
    wallet = findbank["wallet"]
    bankamnt= findbank["bank"]

    updated_wallet = wallet + int(money)
    updated_bank = bankamnt - int(money)

    if int(money) > bankamnt:
        await ctx.respond("Let's face reality, you don't have that much money")
    
    if int(money) <= 0:
        await ctx.respond("wake up to reality, you can't deposit imaginary money")
    
    else:
        await collection.update_one({"_id": member.id}, {"$set": {"wallet": updated_wallet}})
        await collection.update_one({"_id": member.id}, {"$set": {"bank": updated_bank}})
        await ctx.respond("Money withdrawn successfully!")

#test cmds

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def lyrics(ctx, *, search = str):
    """A command to find lyrics easily!"""
    if not search:
        embed = discord.Embed(
            title = "No search argument!",
            description = "You havent entered anything, so i couldnt find lyrics!"
        )
        return await ctx.send(embed = embed)
    
    song = urllib.parse.quote(search)
    
    async with aiohttp.ClientSession() as lyricsSession:
        async with lyricsSession.get(f'https://some-random-api.ml/lyrics?title={song}') as jsondata:
            if not 300 > jsondata.status >= 200:
                return await ctx.send(f'Recieved poor status code of {jsondata.status}')

            lyricsData = await jsondata.json()

    error = lyricsData.get('error')
    if error:
        return await ctx.send(f'Recieved unexpected error: {error}')

    songLyrics = lyricsData['lyrics']
    songArtist = lyricsData['author']
    songTitle = lyricsData['title']
    songThumbnail = lyricsData['thumbnail']['genius']

    for chunk in textwrap.wrap(songLyrics, 4096, replace_whitespace = False):
        embed = discord.Embed(
            title = songTitle,
            description = chunk,
            color = discord.Color.blurple(),
            timestamp = datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url = songThumbnail)
        await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def fox(ctx):

    resp = requests.get("https://some-random-api.ml/animal/fox")

    if 300 > resp.status_code >= 200:
        content = resp.json()
    else:
        content = f"Recieved a bad status code of {resp.status_code}."
    
    picture = content['image']
    fact = content['fact']

    embed = discord.Embed(
    title="fox image",
    description=fact,
    colour = discord.Colour.random()
    )
    embed.set_image(url=picture)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def cat(ctx):

    resp = requests.get("https://some-random-api.ml/animal/cat")

    if 300 > resp.status_code >= 200:
        content = resp.json()
    else:
        content = f"Recieved a bad status code of {resp.status_code}."
    
    picture = content['image']
    fact = content['fact']

    embed = discord.Embed(
    title="cat image",
    description=fact,
    colour = discord.Colour.random()
    )
    embed.set_image(url=picture)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def dog(ctx):
    resp = requests.get("https://some-random-api.ml/animal/dog")

    if 300 > resp.status_code >= 200:
        content = resp.json()
    else:
        content = f"Recieved a bad status code of {resp.status_code}."
    
    picture = content['image']
    fact = content['fact']

    embed = discord.Embed(
    title="dog image",
    description=fact,
    colour = discord.Colour.random()
    )
    embed.set_image(url=picture)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def panda(ctx):
    resp = requests.get("https://some-random-api.ml/animal/panda")

    if 300 > resp.status_code >= 200:
        content = resp.json() 
    else:
        content = f"Recieved a bad status code of {resp.status_code}."
    
    picture = content['image']
    fact = content['fact']

    embed = discord.Embed(
    title="panda image",
    description=fact,
    colour = discord.Colour.random()
    )
    embed.set_image(url=picture)
    await ctx.respond(embed = embed)

@bot.slash_command(guild_ids=[931679366365204600, 932716813580636230])
async def hug(ctx, person: str):
    resp = requests.get("https://some-random-api.ml/animu/hug")
    if 300 > resp.status_code >= 200:
        content = resp.json()
    else:
        content = f"Recieved a bad status code of {resp.status_code}."
    
    embed = discord.Embed(title=f"{ctx.author} hugged {person}.", colour = discord.Colour.red())
    gif = content['link']
    embed.set_image(url=gif)
    await ctx.respond(embed = embed)

#events
@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send(random.choice(rude))
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="ONLYFANS"))
    print(f"Logged in as {bot.user}")
    print("------")

@bot.event
async def on_message(message):
    if bot.user.mentioned_in(message):
        await message.channel.send(random.choice(rude))


bot.run("OTAzNDIzMDQyMzc2NTk3NTE1.YXswRg.-A-P4F-DCFGiAevU204e2uk-xP0") 
