import discord
from discord.ext import commands


class Mute(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Stop any mentions')
    async def mute(self, context):
        await context.send('...')


def setup(client):
    client.add_cog(Mute(client))