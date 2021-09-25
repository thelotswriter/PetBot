import discord
from discord.ext import commands


class Leave(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Abandon your pet')
    async def leave(self, context, *, message=None):
        await context.send('Really? That\'s so heartless. Also, you don\t have a pet now anyways, so no.')
        player = context.author
        pid = player.id
        if message is not None:
            pass
        else:
            pass


def setup(client):
    client.add_cog(Leave(client))