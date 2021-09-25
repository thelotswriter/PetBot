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
                pet_manager.add_pet(pid, len(pet_manager.pets), pet_name)
                await context.send(f'Your pet, {pet_name}, is ready!')
        else:
            await context.send('Sorry, you don\'t have room for more pets right now.')


def setup(client):
    client.add_cog(Add(client))