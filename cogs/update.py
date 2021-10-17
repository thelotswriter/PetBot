import discord
from discord.ext import commands
import pet_manager
import the_pet


class Update(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Secret command to force pet update
    @commands.command()
    async def update(self, context):
        await pet_manager.update_pets(context)


def setup(client):
    client.add_cog(Update(client))