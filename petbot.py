import os
import random
import discord
from discord.ext import commands

import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision

token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix=['<@!886644051829460992> ', '<@886644051829460992> ', '<@!888217121451044894> ', '<@888217121451044894> '], help_command=None) # '<@!886644051829460992> ')

@client.event
async def on_ready():
    print(f"{client.user} is connected!")

@client.command()
async def help(context):
    await context.send(
        'help - Show this list\n'
        'begin - Get your new pet\n'
        'show - Look at your pet\n'
        'status - Check your pet\'s status\n'
        'feed - Feed your pet\n'
        'clean - Give your pet a bath\n'
        'lights on/off - Turn the lights on or off\n'
        'mute - Disable notifications\n'
        'leave pet - Get rid of your current pet'
    )

@client.command()
async def begin(context):
    await context.send('Sorry, we\'re all out of pets right now!')

@client.command()
async def show(context):
    await context.send('Did you really expect to see something without a pet?')

@client.command()
async def status(context):
    await context.send('Current status? There is no status.')

@client.command()
async def feed(context):
    await context.send('Oops! All out of food!')

@client.command()
async def clean(context):
    await context.send('Yeah, that\'s not happening')

@client.command(aliases=['lights on'])
async def lights_on(context):
    await context.send('The lights are on but nobody\'s home!')

@client.command(aliases=['lights off'])
async def lights_off(context):
    await context.send('Saving power? Saving the planet!')

@client.command()
async def mute(context):
    await context.send('...')

@client.command(aliases=['leave pet'])
async def abandon(context):
    await context.send('Really? That\'s so heartless. Also, you don\t have a pet now anyways, so no.')

@client.command()
async def printtest(context, *, message):
    print(message)

client.run(token)
