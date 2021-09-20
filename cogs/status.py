import discord
from discord.ext import commands


class Status(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Check the status of your pet')
    async def status(self, context):
        await context.send('Current status? There is no status.')


def setup(client):
    client.add_cog(Status(client))