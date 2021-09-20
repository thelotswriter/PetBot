import discord
from discord.ext import commands


class Lights(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Turn the lights on or off')
    async def lights(self, context, *, message):
        if 'on' in message:
            await context.send('The lights are on but nobody\'s home!')
        elif 'off' in message:
            await context.send('Saving power *is* good for the environment')


def setup(client):
    client.add_cog(Lights(client))