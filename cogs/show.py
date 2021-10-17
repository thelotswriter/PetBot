import discord
from discord.ext import commands

import pet_manager


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Take a look at your pet')
    async def show(self, context, *, message=None):
        player = context.author
        pid = player.id
        await pet_manager.show(pid, pet_name=message, context=context)


def setup(client):
    client.add_cog(Show(client))