import os
import random
import discord

import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision

token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == my_guild:
            break

    print(
        f"{client.user} is connected to the following guild:\n"
        f"{guild.name}(id: {guild.id})"
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
#    await message.channel.send('Noticed')
    if message.content.replace('!','').startswith(client.user.mention):
        response = "Hi, I am " + client.user.mention + "! Nice to meet you!"
        await message.channel.send(response)
    else:
        print(message.content)
        print(client.user.mention)

client.run(token)
