import discord
from discord.ext import commands
import pet_manager
import the_pet


class Medicate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Give your sick pet medicine. Not for healthy pets!')
    async def medicate(self, context, *, message=None):
        player = context.author
        pid = player.id
        await pet_manager.medicate(pid, pet_name=message, context=context)


def setup(client):
    client.add_cog(Medicate(client))