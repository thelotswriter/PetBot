import discord
from discord.ext import commands


class Clean(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Make your pet squeaky clean!')
    async def clean(self, context):
        await context.send('Yeah, that\'s not happening')


def setup(client):
    client.add_cog(Clean(client))