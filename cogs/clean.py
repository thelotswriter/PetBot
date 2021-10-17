import discord
from discord.ext import commands
import pet_manager
import player_manager
import the_pet


class Clean(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Make your pet squeaky clean!')
    async def clean(self, context, *, message=None):
        player = context.author
        pid = player.id
        await pet_manager.clean(pid, pet_name=message, context=context)


def setup(client):
    client.add_cog(Clean(client))