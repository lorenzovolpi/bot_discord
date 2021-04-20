import os
import discord
from bs4 import BeautifulSoup
import lxml
import requests
import random
from discord.ext import commands

from dotenv import load_dotenv

import scraping

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
#intents.members = True
#intents.messages = True

bot = commands.Bot(command_prefix='!piccolo ', intents=intents)


@bot.command(name='mysphere', help='Return a random number in range 1-7')
async def mysphere(ctx):
    sphere_number = random.randint(1,7)
    await ctx.send("You have found the Dragonball N° {}!!".format(sphere_number))


@bot.command(name='hi', help='Return a random number in range 1-7')
async def hi(ctx):
    await ctx.send("Hi! I'm the bot!")


   
@bot.command(name='whois', help='Return a random number in range 1-7')
async def whois(ctx, *names):
    await scraping.fetch_and_reply(ctx, names)
    

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == GUILD:
            break

    members = '\n -'.join([member.name for member in guild.members])
    print(members)


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send("{} it's over 9000".format(member.name))
    print("Sent DM")


'''
@bot.event
async def on_message(message):
    if message.author.bot == False:
        await message.channel.send("{} kamehameha!!".format(message.content))
    print("Sent Message on Channel")
'''


bot.run(TOKEN)
