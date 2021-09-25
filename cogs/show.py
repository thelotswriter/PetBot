import discord
from discord.ext import commands


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Take a look at your pet')
    async def show(self, context, *, message=None):
        await context.send('Not quite ready.')


def setup(client):
    client.add_cog(Show(client))