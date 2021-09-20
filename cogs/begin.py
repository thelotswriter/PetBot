import discord
from discord.ext import commands


class Begin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Begin your pet adventure!')
    async def begin(self, context):
        await context.send('Sorry, we\'re all out of pets right now!')


def setup(client):
    client.add_cog(Begin(client))