import discord
from discord.ext import commands
import pet_manager
import the_pet


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet name] Check the status of your pet')
    async def status(self, context, *, message=None):
        player = context.author
        pid = player.id
        await pet_manager.status(pid, pet_name=message, context=context)


def setup(client):
    client.add_cog(Status(client))