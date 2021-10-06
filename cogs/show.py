import discord
from discord.ext import commands

import pet_manager


class Show(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Take a look at your pet')
    async def show(self, context, *, message=None):
        player = context.author
        pid = player.id
        if pid in pet_manager.player_pets:
            if message is not None:
                counter = 0
                for pet_name in pet_manager.player_pets[pid].keys():
                    if pet_name in message:
                        counter += 1
                        await pet_manager.player_pets[pid][pet_name].show(context)
                if counter == 0:
                    await context.send(f'No pets named {message} for you, <@{pid}>.')
            else:
                for pet_name in pet_manager.player_pets[pid].keys():
                    await pet_manager.player_pets[pid][pet_name].show(context)
        else:
            await context.send('Sorry, no pets to show!')


def setup(client):
    client.add_cog(Show(client))