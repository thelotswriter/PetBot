import discord
from discord.ext import commands


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Take a look at your pet')
    async def show(self, context):
        await context.send('Did you really expect to see something without a pet?')


def setup(client):
    client.add_cog(Show(client))