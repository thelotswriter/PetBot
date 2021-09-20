import discord
from discord.ext import commands


class Feed(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Give your pet some food')
    async def feed(self, context):
        await context.send('Oops! All out of food!')

def setup(client):
    client.add_cog(Feed(client))