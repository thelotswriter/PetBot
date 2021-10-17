import discord
from discord.ext import commands
import pet_manager
import the_pet


class Feed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Give your pet some food')
    async def feed(self, context, *, message=None):
        player = context.author
        pid = player.id
        await pet_manager.feed(pid, pet_name=message, context=context)


def setup(client):
    client.add_cog(Feed(client))