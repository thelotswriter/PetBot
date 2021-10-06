import discord
from discord.ext import commands

import egg_manager
import pet_manager
import the_pet


class Collect(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(brief='[pet] Collect an egg from your pet')
    async def collect(self, context, *, message=None):
        player = context.author
        pid = player.id
        if pid not in egg_manager.player_eggs or (pid in egg_manager.player_eggs and len(egg_manager.player_eggs[pid]) < 3):
            if pid in pet_manager.player_pets:
                if message is None:
                    await context.send(f'Which pet would you like to collect from, <@{pid}>?')
                    message = await self.client.wait_for('message',
                                                         check=lambda message: message.author == context.author)
                    message = message.content
                counter = 0
                for pet_name in pet_manager.player_pets[pid].keys():
                    if pet_name in message:
                        counter += 1
                        egg_manager.add_egg(pid, pet_manager.player_pets[pid][pet_name])
                        await context.send('Your egg has been collected!')
                        break
                if counter == 0:
                    await context.send('Sorry, no such pet found!')
            else:
                await context.send('Sorry, no pets to collect eggs from!')
        else:
            await context.send('Sorry, you don\'t have room for more eggs right now.')

def setup(client):
    client.add_cog(Collect(client))