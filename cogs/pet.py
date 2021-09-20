import discord
from discord.ext import commands


class Pet(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Give your pet some attention')
    async def pet(self, context):
        await context.send('That\'s very thoughtful, but you don\'t have a pet to pet yet')


def setup(client):
    client.add_cog(Pet(client))