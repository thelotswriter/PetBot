import asyncio
import os
from discord.ext import commands

import db_manager
import petbotengine as engine

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision


# Custom help command
class PetHelpCommand(commands.HelpCommand):

    def __init__(self):
        super().__init__()

    # Custom help command listing
    async def send_bot_help(self, mapping):
        command_list = []
        for cog in mapping:
            command_list.extend([command for command in mapping[cog]])
        command_str = ''
        for c in command_list:
            if c.brief is not None:
                command_str += c.name + ' - ' + c.brief
                command_str += '\n'
        await self.get_destination().send(command_str)

    async def send_cog_help(self, cog):
        return await super().send_cog_help(cog)

    async def send_group_help(self, group):
        return await super().send_cog_help(group)

    async def send_command_help(self, command):
        return await super().send_command_help(command)


token = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix=['<@!886644051829460992> ', '<@886644051829460992> ', '<@!888217121451044894> ', '<@888217121451044894> '], help_command=PetHelpCommand())


@client.event
async def on_ready():
    print(f"{client.user} is connected!")


@client.command()
async def printtest(context, *, message):
    print(message)


# Load cogs
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# Load cogs
path = os.path.dirname(os.path.abspath(__file__))
for filename in os.listdir(os.path.join(path, 'cogs')):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Load players, pets, and eggs from database
connection = db_manager.create_connection()
with connection:
    db_manager.create_tables(connection)
    db_manager.get_players(connection)
    db_manager.get_pets(connection)
    db_manager.get_eggs(connection)
asyncio.get_event_loop().create_task(engine.update())
client.run(token)
