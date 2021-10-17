import discord
from discord.ext import commands
import os

import egg_manager
import pet_manager
import player_manager
import the_pet


class Hatch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Select an egg to hatch')
    async def hatch(self, context):
        player = context.author
        pid = player.id
        pleggs = egg_manager.get_player_eggs(pid)
        if len(pleggs) > 0:
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(path, 'images')
            x = 0
            for egg in pleggs:
                egg_path = os.path.join(path, str(egg.dna[0]))
                await context.send(f'Egg {egg.egg_id}:',
                                   file=discord.File(os.path.join(egg_path, 'expanded_egg.png')))
            await context.send('Which egg would you like? Enter the egg number *only* to choose.')
            selection = await self.client.wait_for('message',
                                                   check=lambda message: message.author == context.author)
            egg_selection = selection.content
            egg = None
            selected = False
            for an_egg in pleggs:
                if str(an_egg.egg_id) == egg_selection:
                    egg = an_egg
                    await context.send(f'What would you like to name the hatchling, <@{pid}>?')
                    name = await self.client.wait_for('message',
                                                           check=lambda message: message.author == context.author)
                    name = name.content
                    pet_manager.hatch_pet(pid, name, egg)
                    selected = True
                    break
            if selected:
                await context.send(f'Your pet, {name}, has been hatched!')
            else:
                await context.send('Sorry, that\'s not a valid selection.')
        else:
            await context.send(f'Looks like you don\'t have any eggs, <@{pid}>.')


def setup(client):
    client.add_cog(Hatch(client))