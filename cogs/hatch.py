import discord
from discord.ext import commands
import os

import egg_manager
import pet_manager
import the_pet


class Hatch(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Select an egg to hatch')
    async def hatch(self, context):
        player = context.author
        pid = player.id
        if pid in pet_manager.player_pets and len(pet_manager.player_pets[pid]) >= 3:
            await context.send(f'Sorry, looks like you have too many pets right now, <@{pid}>.')
        elif pid not in egg_manager.player_eggs:
            await context.send(f'Sorry <@{pid}>, you don\'t have any eggs right now.')
        else:
            egg_ids = []
            path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            path = os.path.join(path, 'images')
            for egg in egg_manager.player_eggs[pid]:
                egg_ids.append(egg)
                egg_path = os.path.join(path, str(egg_manager.player_eggs[pid][egg].dna[0]))
                await context.send(f'Option {len(egg_ids)}:',
                                   file=discord.File(os.path.join(egg_path, 'expanded_egg.png')))
            await context.send('Which egg would you like? Enter the option number to choose (1, 2, 3, etc).')
            selection = await self.client.wait_for('message',
                                                   check=lambda message: message.author == context.author)
            selection = selection.content
            selected = False
            for x in range(len(egg_ids)):
                y = x + 1
                if str(y) == selection:
                    egg = egg_manager.retrieve_egg(pid, egg_ids[x])
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


def setup(client):
    client.add_cog(Hatch(client))