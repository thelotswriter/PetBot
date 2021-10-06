import os
import random

import discord
from discord.ext import commands

import pet_manager


class Add(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='Begin your pet adventure!')
    async def add(self, context, *, message=None):
        player = context.author
        pid = player.id
        can_add = True
        if pid in pet_manager.player_pets.keys():
            if len(pet_manager.player_pets[pid]) >= 3:
                can_add = False
        if can_add:
            valid_name = False
            if message is None:
                await context.send(f'What would you like to name your pet, <@{pid}>?!')
                pet_name_message = await self.client.wait_for('message',
                                                              check=lambda message: message.author == context.author)
                pet_name = pet_name_message.content
            else:
                pet_name = message
            if pid in pet_manager.player_pets.keys():
                if pet_name in pet_manager.player_pets[pid].keys():
                    await context.send('Sorry, no duplicate names!')
                else:
                    valid_name = True
            else:
                valid_name = True
            if valid_name:
                path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                path = os.path.join(path, 'images')
                for x in range(4):
                    y = x + 1
                    await context.send(f'Option {y}:',
                                       file=discord.File(os.path.join(os.path.join(path, str(y)), 'expanded_egg.png')))
                await context.send('Which egg would you like? Enter 1, 2, 3, 4 to choose. '
                                   'Otherwise, enter something else for a random choice.')
                selection = await self.client.wait_for('message',
                                                       check=lambda message: message.author == context.author)
                selection = selection.content
                if '1' in selection and len(selection) == 1:
                    dna = [1]
                elif '2' in selection and len(selection) == 1:
                    dna = [2]
                elif '3' in selection and len(selection) == 1:
                    dna = [3]
                elif '4' in selection and len(selection) == 1:
                    dna = [4]
                else:
                    dna = [random.randint(1, 4)]
                pet_manager.add_pet(pid, pet_name, dna)
                await context.send(f'Your pet, {pet_name}, is ready!')
            else:
                await context.send(f'Sorry, you already have a pet named {pet_name}. Please try a different name.')
        else:
            await context.send('Sorry, you don\'t have room for more pets right now.')


def setup(client):
    client.add_cog(Add(client))