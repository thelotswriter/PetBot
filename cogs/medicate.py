import discord
from discord.ext import commands
import pet_manager
import the_pet


class Medicate(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Give your sick pet medicine')
    async def medicate(self, context, *, message=None):
        player = context.author
        pid = player.id
        if pid in pet_manager.player_pets:
            if message is not None:
                counter = 0
                for pet_name in pet_manager.player_pets[pid].keys():
                    if pet_name in message:
                        counter += 1
                        pet_manager.player_pets[pid][pet_name].medicate()
                        await context.send(f'{pet_name} was medicated.')
                if counter == 0:
                    await context.send(f'No pets named {message} for you, <@{pid}>.')
            else:
                for pet_name in pet_manager.player_pets[pid].keys():
                    pet_manager.player_pets[pid][pet_name].medicate()
                await context.send(f'Your pets were medicated, <@{pid}>.')
        else:
            await context.send('Sorry, no pets to medicate!')


def setup(client):
    client.add_cog(Medicate(client))