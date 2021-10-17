import discord
from discord.ext import commands
import pet_manager
import the_pet


class Level(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Hidden command to level up a pet. Currently defunct
    @commands.command()
    async def level(self, context, *, message=None):
        player = context.author


def setup(client):
    client.add_cog(Level(client))