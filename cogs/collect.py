import discord
from discord.ext import commands

import egg_manager
import pet_manager
import player_manager
import the_pet


class Collect(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Collect an egg from your pet')
    async def collect(self, context, *, message=None):
        player = context.author
        pid = player.id
        if egg_manager.can_add(pid):
            if message is None:
                await context.send(f'Which pet would you like to collect from, <@{pid}>?')
                message = await self.client.wait_for('message',
                                                     check=lambda message: message.author == context.author)
                message = message.content
            pet = pet_manager.get_pet(pid, message)
            if pet is not None:
                egg_manager.add_egg(pid, pet)
                await context.send(f'Your egg has been collected, <@{pid}>.')
            else:
                await context.send(f'You don\'t have a pet named {message}, <@{pid}>')
        else:
            await context.send(f'Sorry, looks like you can\'t add any more eggs right now, <@{pid}>.')


def setup(client):
    client.add_cog(Collect(client))