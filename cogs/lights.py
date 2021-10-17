import discord
from discord.ext import commands
import pet_manager
import the_pet


class Lights(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[on/off] [pet] Turn the lights on or off')
    async def lights(self, context, *, message=None):
        player = context.author
        pid = player.id
        if message is None:
            await context.send('Lights on or off?')
            message = await self.client.wait_for('message',
                                                       check=lambda message: message.author == context.author)
            message = message.content
        await pet_manager.lights(pid, message, context=context)


def setup(client):
    client.add_cog(Lights(client))